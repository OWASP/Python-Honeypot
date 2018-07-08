#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import inspect
import os

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
        True
    """
    for selected_module in configuration:
        # go to tmp folder to create Dockerfile
        tmp_dir_name = make_tmp_thread_dir()
        os.chdir(tmp_dir_name)

        # get the container name to start (organizing)
        # using pattern name will help us to remove/modify the images and modules
        container_name = virtual_machine_name_to_container_name(configuration[selected_module]["virtual_machine_name"],
                                                                selected_module)
        info("starting container {0}".format(container_name))

        # run the container
        os.popen("docker run --name={0} -d -t -p {1}:{2} {3}"
                 .format(container_name, configuration[selected_module]["real_machine_port_number"],
                         configuration[selected_module]["virtual_machine_port_number"],
                         configuration[selected_module]["virtual_machine_name"])).read()

        info("container {0} started".format(container_name))

        # go back to home directory
        os.chdir("../..")

        # submit tmp dir name
        tmp_directories.append(tmp_dir_name)

    return True


def wait_until_interrupt():
    """
    wait for opened threads/honeypots modules

    Returns:
        True
    """
    while True:
        # while True sleep until user send ctrl + c
        try:
            time.sleep(0.3)
        except KeyboardInterrupt:
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
        module_configuration = getattr(
            __import__("lib.modules.{0}".format(module.replace("/", ".")), fromlist=["module_configuration"]),
            "module_configuration")

        # combine category + module configuration into one Dict/JSON
        combined_module_configuration = module_configuration()
        combined_module_configuration.update(category_configuration())

        # based on your configuration, the variables/values will be set into your Dockerfile
        # e.g. username will be replaced by {username} in Dockerfile
        combined_module_configuration["dockerfile"] = open(
            os.path.dirname(inspect.getfile(module_configuration)) +
            "/Dockerfile").read().format(**combined_module_configuration)
        # combine Dockerfile configuration with module and category configuration
        honeypot_configuration[module] = combined_module_configuration
    return honeypot_configuration


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
                           dest="virtual_machine_container_reset_factory_time", type=int,
                           default=docker_configuration()["virtual_machine_container_reset_factory_time"],
                           help=messages("en", "vm_reset_factory_time"))
    # enable verbose mode (debug mode)
    engineOpt.add_argument("--verbose", action="store_true", dest="verbose_mode", default=False,
                           help="enable verbose mode")
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
        finish()
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
    global verbose_mode
    verbose_mode = argv_options.verbose_mode
    #########################################
    # argv rules apply
    #########################################

    info(messages("en", "honeypot_started"))
    info(messages("en", "loading_modules").format(", ".join(selected_modules)))
    # build configuration based on selected modules
    configuration = honeypot_configuration_builder(selected_modules)

    # stop old containers (in case they are not stopped)
    stop_containers(configuration)
    # remove old containers (in case they are not updated)
    remove_old_containers(configuration)
    # remove old images (in case they are not updated)
    remove_old_images(configuration)
    # create new images based on selected modules
    create_new_images(configuration)
    # start containers based on selected modules
    start_containers(configuration)
    info("all selected modules started: {0}".format(", ".join(selected_modules)))
    # wait forever! in case user can send ctrl + c to interrupt
    wait_until_interrupt()
    info("interrupted by user, please wait to stop the containers and remove the containers and images")
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
