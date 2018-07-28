#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import inspect
import os
import json
import threading
import binascii

from core.get_modules import load_all_modules
from core.alert import info
from core.color import finish
from core.alert import messages
from core.compatible import logo
from core.compatible import version
from core.compatible import os_name
from config import user_configuration
from config import docker_configuration
from core._die import __die_success
from core._die import __die_failure
from core.compatible import make_tmp_thread_dir
from core.get_modules import virtual_machine_names_to_container_names
from core.get_modules import virtual_machine_name_to_container_name
from core.network import new_network_events
from core._die import terminate_thread
from api.server import start_api_server
from core.compatible import check_for_requirements

# temporary use fixed version of argparse
if os_name() == "win32" or os_name() == "win64":
    if version() is 2:
        from lib.argparse.v2 import argparse
    else:
        from lib.argparse.v3 import argparse
else:
    import argparse

# tmp dirs
tmp_directories = []
verbose_mode = None


def all_existing_networks():
    """
    list of all existing networks

    Returns:
        an array with list of all existing networks name
    """
    return [network_name.rsplit()[1] for network_name in os.popen("docker network ls").read().rsplit("\n")[1:-1]]


def write_file_by_dockerfile(module_configuration, file_to_read, file_to_write):
    """
    write a file to by Dockerfile using command: echo -e "content" > /path/filename

    Args:
        module_configuration: module configuration (imported __init__)
        file_to_read: filename (files must be stored in category/module/files/filename
        file_to_write: path/filename to write in image

    Returns:
        command (string) if success otherwise return the error
    """
    try:
        # hex the file first
        hex_content_file = binascii.b2a_hex(
            open(
                "{0}".format(
                    os.path.join(
                        os.path.dirname(
                            inspect.getfile(module_configuration)
                        ), file_to_read
                    )
                ), "rb"
            ).read()
        )
        # convert file to c-style (e.g. \x41\x41)
        c_style_file = "\\x{0}".format(
            "\\x".join(
                "{0}{1}".format(
                    char1,
                    char2
                ) for char1, char2 in zip(
                    hex_content_file[::2].decode(), hex_content_file[1::2].decode()
                )
            )
        )
        # return command (e.g. echo "\x41\x41" > /tmp/file
        return "echo -e \"{0}\" > {1}".format(c_style_file, file_to_write)
    except Exception as _:
        return _


def create_ohp_networks():
    """
    create docker internet and internal network for OWASP Honeypot

    Returns:
        True
    """
    if "ohp_internet" not in all_existing_networks():
        info("creating ohp_internet network")
        os.popen("docker network create ohp_internet  --opt com.docker.network.bridge.enable_icc=true "
                 "--opt com.docker.network.bridge.enable_ip_masquerade=true "
                 "--opt com.docker.network.bridge.host_binding_ipv4=0.0.0.0 --opt "
                 "com.docker.network.driver.mtu=1500").read()
        network_json = json.loads(os.popen("docker network inspect ohp_internet").read())[0]["IPAM"]["Config"][0]
        info("ohp_internet network created subnet:{0} gateway:{1}".format(network_json["Subnet"],
                                                                          network_json["Gateway"]))
    if "ohp_no_internet" not in all_existing_networks():
        info("creating ohp_no_internet network")
        os.popen("docker network create --attachable --internal ohp_no_internet  "
                 "--opt com.docker.network.bridge.enable_icc=true "
                 "--opt com.docker.network.bridge.enable_ip_masquerade=true "
                 "--opt com.docker.network.bridge.host_binding_ipv4=0.0.0.0 "
                 "--opt com.docker.network.driver.mtu=1500").read()
        network_json = json.loads(os.popen("docker network inspect ohp_no_internet").read())[0]["IPAM"]["Config"][0]
        info("ohp_no_internet network created subnet:{0} gateway:{1}".format(network_json["Subnet"],
                                                                             network_json["Gateway"]))
    return True


def remove_tmp_directories():
    """
    remove tmp directories submitted in tmp_directories

    Returns:
        True
    """
    for tmp_dir in tmp_directories:
        os.remove(tmp_dir)
    return True


def running_containers():
    """
    list of running containers

    Returns:
        an array with list of running containers name
    """
    return [container.rsplit()[-1] for container in os.popen("docker ps").read().rsplit("\n")[1:-1]]


def all_existing_containers():
    """
    list of all existing containers

    Returns:
        an array with list of all existing containers name
    """
    return [container.rsplit()[-1] for container in os.popen("docker ps -a").read().rsplit("\n")[1:-1]]


def all_existing_images():
    """
    list of all existing images

    Returns:
        a array with list of all existing images name
    """
    return [container.rsplit()[0] for container in os.popen("docker images").read().rsplit("\n")[1:-1]]


def stop_containers(configuration):
    """
    stop old containers based on images

    Args:
        configuration: user final configuration

    Returns:
        True
    """
    containers_list = running_containers()
    if containers_list:
        for container in virtual_machine_names_to_container_names(configuration):
            if container in containers_list:
                info("stopping container {0}".format(os.popen("docker stop {0}".format(container)).read().rsplit()[0]))
    return True


def remove_old_containers(configuration):
    """
    remove old containers based on images

    Args:
        configuration: user final configuration

    Returns:
        True
    """

    containers_list = all_existing_containers()
    for container in virtual_machine_names_to_container_names(configuration):
        if container in containers_list:
            info("removing container {0}".format(os.popen("docker rm {0}".format(container)).read().rsplit()[0]))
    return True


def get_image_name_of_selected_modules(configuration):
    """
    get list of image name using user final configuration

    Args:
        configuration: user final configuration

    Returns:
        list of virtual machine image name
    """
    return [configuration[selected_module]["virtual_machine_name"] for selected_module in configuration]


def remove_old_images(configuration):
    """
    remove old images based on user configuration

    Args:
        configuration: user final configuration

    Returns:
        True
    """
    for image in all_existing_images():
        if image in get_image_name_of_selected_modules(configuration):
            info("removing image {0}".format(image))
            os.popen("docker rmi {0}".format(image)).read()
    return True


def create_new_images(configuration):
    """
    start new images based on configuration and dockerfile

    Args:
        configuration: user final configuration

    Returns:
        True
    """
    for selected_module in configuration:
        # go to tmp folder to create Dockerfile
        tmp_dir_name = make_tmp_thread_dir()
        os.chdir(tmp_dir_name)

        # create Dockerfile
        dockerfile = open("Dockerfile", "w")
        dockerfile.write(configuration[selected_module]["dockerfile"])
        dockerfile.close()

        # create docker image
        info("creating image {0}".format(configuration[selected_module]["virtual_machine_name"]))

        # in case if verbose mode is enabled, we will be use os.system instead of os.popen to show the outputs in case
        # of anyone want to be aware what's happening or what's the error, it's a good feature for developers as well
        # to create new modules
        if verbose_mode:
            os.system("docker build . -t {0}".format(configuration[selected_module]["virtual_machine_name"]))
        else:
            os.popen("docker build . -t {0}".format(configuration[selected_module]["virtual_machine_name"])).read()

        # created
        info("image {0} created".format(configuration[selected_module]["virtual_machine_name"]))

        # go back to home directory
        os.chdir("../..")

        # submit tmp dir name
        tmp_directories.append(tmp_dir_name)

    return True


def start_containers(configuration):
    """
    start containers based on configuration and dockerfile

    Args:
        configuration: JSON container configuration

    Returns:
        configuration containing IP Addresses
    """
    for selected_module in configuration:
        # get the container name to start (organizing)
        # using pattern name will help us to remove/modify the images and modules
        container_name = virtual_machine_name_to_container_name(configuration[selected_module]["virtual_machine_name"],
                                                                selected_module)
        real_machine_port = configuration[selected_module]["real_machine_port_number"]
        virtual_machine_port = configuration[selected_module]["virtual_machine_port_number"]
        # connect to owasp nettacker networks!
        if configuration[selected_module]["virtual_machine_internet_access"]:
            # run the container with internet access
            os.popen("docker run --net ohp_internet --name={0} -d -t -p {1}:{2} {3}"
                     .format(container_name, real_machine_port, virtual_machine_port,
                             configuration[selected_module]["virtual_machine_name"])).read()
        else:
            # run the container without internet access
            os.popen("docker run --net ohp_no_internet --name={0} -d -t -p {1}:{2} {3}"
                     .format(container_name, real_machine_port, virtual_machine_port,
                             configuration[selected_module]["virtual_machine_name"])).read()
        try:
            virtual_machine_ip_address = os.popen("docker inspect -f '{{range.NetworkSettings.Networks}}"
                                                  "{{.IPAddress}}{{end}}' %s" % container_name).read().rsplit()[0][1:-1]
        except Exception as _:
            virtual_machine_ip_address = "127.0.0.1"
        # add virtual machine IP Address to configuration
        configuration[selected_module]["ip_address"] = virtual_machine_ip_address
        # print started container information
        info("container {0} started,"
             " forwarding 0.0.0.0:{1} to {2}:{3}".format(container_name, real_machine_port, virtual_machine_ip_address,
                                                         virtual_machine_port))
    return configuration


def wait_until_interrupt(virtual_machine_container_reset_factory_time_seconds, configuration):
    """
    wait for opened threads/honeypots modules

    Returns:
        True
    """
    # running_time variable will be use to check if its need to reset the container after a while
    # if virtual_machine_container_reset_factory_time_seconds < 0, it will keep containers until user interruption
    running_time = 0
    while True:
        # while True sleep until user send ctrl + c
        try:
            time.sleep(1)
            running_time += 1
            # check if running_time is equal to reset factory time
            if running_time is virtual_machine_container_reset_factory_time_seconds:
                # reset the run time
                running_time = 0
                # stop old containers (in case they are not stopped)
                stop_containers(configuration)
                # remove old containers (in case they are not updated)
                remove_old_containers(configuration)
                # start containers based on selected modules
                start_containers(configuration)
        except KeyboardInterrupt:
            # break and return for stopping and removing containers/images
            info("interrupted by user, please wait to stop the containers and remove the containers and images")
            break
    return True


def honeypot_configuration_builder(selected_modules):
    """
    honeypot configuration builder

    Args:
        selected_modules: list of selected modules

    Returns:
        JSON/Dict OHP configuration
    """
    # the modules are available in lib/modules/category_name/module_name (e.g. lib/modules/ftp/weak_password
    # they will be listed based on the folder names and if "Dockerfile" exist!
    # the Dockerfile will be read and add into JSON configuration (dockerfile)
    honeypot_configuration = {}
    for module in selected_modules:
        # read category configuration (e.g. ftp, ssh, http, etc..), they are located in lib/modules/category/__init__.py
        # in the __init__.py every category has same function as below!
        # def category_configuration():
        #     return {
        #          "virtual_machine_name": "ohp_sshserver",
        #          "virtual_machine_port_number": 22,
        #          "virtual_machine_internet_access": False,
        #          "real_machine_port_number": 22
        #     }

        category_configuration = getattr(
            __import__("lib.modules.{0}".format(module.rsplit("/")[0]), fromlist=["category_configuration"]),
            "category_configuration")
        # reading each module configuration (e.g. ftp/weak_password, etc..)
        # they are located in lib/modules/category/module_name/__init__.py
        # each module must have such a function (in case you can return {} if you don't have any configuration)
        # def module_configuration():
        #     return {
        #         "username": "admin",
        #         "password": "123456"
        #      }
        # to replace the category default port for individual modules, you have to add "real_machine_port_number"
        # key to module configuration to replace it.
        #
        # for instance:
        # def module_configuration():
        #     return {
        #         "username": "admin",
        #         "password": "123456"
        #         "real_machine_port_number": 2121
        #      }
        module_configuration = getattr(
            __import__("lib.modules.{0}".format(module.replace("/", ".")), fromlist=["module_configuration"]),
            "module_configuration")

        # combine category + module configuration into one Dict/JSON
        combined_module_configuration = category_configuration()
        combined_module_configuration.update(module_configuration())

        # based on your configuration, the variables/values will be set into your Dockerfile
        # e.g. username will be replaced by {username} in Dockerfile
        combined_module_configuration["dockerfile"] = open(
            os.path.dirname(
                inspect.getfile(module_configuration)
            ) + "/Dockerfile"
        ).read().format(
            **combined_module_configuration
        )
        # write file to docker image check
        json_find_writefile_tags = {}
        # explore the dockerfile to find something like {write_file_by_to_docker_image(filename,path/file)}
        # I used echo -e "content" > /path/file to create files in Docker images, to automate this we need to create
        # a function to implement and add it easy
        for word in combined_module_configuration["dockerfile"].rsplit():
            if word.startswith("{write_file_by_to_docker_image("):
                json_find_writefile_tags[word] = write_file_by_dockerfile(
                    module_configuration,
                    word.rsplit("{write_file_by_to_docker_image(")[1].rsplit(",")[0],
                    word.rsplit("{write_file_by_to_docker_image(")[1].rsplit(",")[1].rsplit(")")[0]
                )
        # apply the tags
        combined_module_configuration["dockerfile"] = combined_module_configuration["dockerfile"].format(
            **json_find_writefile_tags
        )
        # combine Dockerfile configuration with module and category configuration
        honeypot_configuration[module] = combined_module_configuration
    return honeypot_configuration


def conflict_ports(configuration):
    """
    check conflict ports in configuration

    Args:
        configuration: user final configuration

    Returns:
        an array with conflicted module [module_name1, module_name2] or []
    """
    for selected_module in configuration:
        port = configuration[selected_module]["real_machine_port_number"]
        for find_module in configuration:
            find_port = configuration[find_module]["real_machine_port_number"]
            if port is find_port and find_module != selected_module:
                return [find_module, selected_module]
    return []


def argv_parser():
    """
    parse ARGVs using argparse

    Returns:
        parser, parsed ARGVs
    """
    # create parser
    parser = argparse.ArgumentParser(prog="Nettacker", add_help=False)
    # create menu
    engineOpt = parser.add_argument_group(messages("en", "engine"), messages("en", "engine_input"))
    # add select module options + list of available modules
    engineOpt.add_argument("-m", "--select-module", action="store",
                           dest="selected_modules", default=user_configuration()["default_selected_modules"],
                           help=messages("en", "select_module").format(load_all_modules()))
    # by default all modules are selected, in case users can exclude one or some (separated with comma)
    engineOpt.add_argument("-x", "--exclude-module", action="store",
                           dest="excluded_modules", default=user_configuration()["default_excluded_modules"],
                           help=messages("en", "exclude_module").format(load_all_modules()))
    # limit the virtual machine storage to avoid related abuse
    engineOpt.add_argument("-s", "--vm-storage-limit", action="store",
                           dest="virtual_machine_storage_limit", type=float,
                           default=docker_configuration()["virtual_machine_storage_limit"],
                           help=messages("en", "vm_storage_limit"))
    # reset the containers once in a time to prevent being continues botnet zombie
    engineOpt.add_argument("-r", "--vm-reset-factory-time", action="store",
                           dest="virtual_machine_container_reset_factory_time_seconds", type=int,
                           default=docker_configuration()["virtual_machine_container_reset_factory_time_seconds"],
                           help=messages("en", "vm_reset_factory_time"))
    # start api
    engineOpt.add_argument("--start-api-server", action="store_true", dest="start_api_server", default=False,
                           help="start API server")
    # enable verbose mode (debug mode)
    engineOpt.add_argument("--verbose", action="store_true", dest="verbose_mode", default=False,
                           help="enable verbose mode")
    # disable color CLI
    engineOpt.add_argument("--disable-colors", action="store_true", dest="disable_colors", default=False,
                           help="disable colors in CLI")
    # help menu
    engineOpt.add_argument("-h", "--help", action="store_true", default=False, dest="show_help_menu",
                           help=messages("en", "show_help_menu"))
    return parser, parser.parse_args()


def load_honeypot_engine():
    """
    load OHP Engine

    Returns:
        True
    """
    # print logo
    logo()

    # parse argv
    parser, argv_options = argv_parser()

    #########################################
    # argv rules apply
    #########################################
    # check help menu
    if argv_options.show_help_menu:
        parser.print_help()
        __die_success()
    # check for requirements before start
    check_for_requirements(argv_options.start_api_server)
    # check api server flag
    if argv_options.start_api_server:
        start_api_server()
        __die_success()
    # check selected modules
    if argv_options.selected_modules:
        selected_modules = list(set(argv_options.selected_modules.rsplit(",")))
        if "" in selected_modules:
            selected_modules.remove("")
        # if selected modules are zero
        if not len(selected_modules):
            __die_failure(messages("en", "zero_module_selected"))
        # if module not found
        for module in selected_modules:
            if module not in load_all_modules():
                __die_failure(messages("en", "module_not_found").format(module))
    # check excluded modules
    if argv_options.excluded_modules:
        excluded_modules = list(set(argv_options.excluded_modules.rsplit(",")))
        if "" in excluded_modules:
            excluded_modules.remove("")
        # remove excluded modules
        for module in excluded_modules:
            if module not in load_all_modules():
                __die_failure(messages("en", "module_not_found").format(module))
            # ignore if module not selected, it will remove anyway
            try:
                selected_modules.remove(module)
            except Exception as _:
                del _
        # if selected modules are zero
        if not len(selected_modules):
            __die_failure(messages("en", "zero_module_selected"))
    virtual_machine_container_reset_factory_time_seconds = argv_options. \
        virtual_machine_container_reset_factory_time_seconds
    global verbose_mode
    verbose_mode = argv_options.verbose_mode
    #########################################
    # argv rules apply
    #########################################
    # build configuration based on selected modules
    configuration = honeypot_configuration_builder(selected_modules)

    # check for conflict in real machine ports
    conflict = conflict_ports(configuration)
    if conflict:
        __die_failure("conflict ports between {0}, {1}".format(conflict[0], conflict[1]))

    info(messages("en", "honeypot_started"))
    info(messages("en", "loading_modules").format(", ".join(selected_modules)))

    # stop old containers (in case they are not stopped)
    stop_containers(configuration)
    # remove old containers (in case they are not updated)
    remove_old_containers(configuration)
    # remove old images (in case they are not updated)
    remove_old_images(configuration)
    # create new images based on selected modules
    create_new_images(configuration)
    # create OWASP Honeypot networks in case not exist
    create_ohp_networks()
    # start containers based on selected modules
    configuration = start_containers(configuration)
    # start network monitoring thread
    new_network_events_thread = threading.Thread(target=new_network_events, args=(configuration,),
                                                 name="new_network_events_thread")
    new_network_events_thread.start()
    info("all selected modules started: {0}".format(", ".join(selected_modules)))
    # wait forever! in case user can send ctrl + c to interrupt
    wait_until_interrupt(virtual_machine_container_reset_factory_time_seconds, configuration)
    # kill the network events thread
    terminate_thread(new_network_events_thread)
    # stop created containers
    stop_containers(configuration)
    # remove created containers
    remove_old_containers(configuration)
    # remove created images
    remove_old_images(configuration)
    # remove_tmp_directories() error: access denied!
    info("finished.")
    # reset cmd/terminal color
    finish()
    return True
