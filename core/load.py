#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import multiprocessing as mp
import os
import socket
import time
import argparse

from terminable_thread import Thread, threading

from api.server import start_api_server
from config import (docker_configuration, network_configuration,
                    user_configuration)
from core.alert import error, info
from core.color import reset_cmd_color
from core.compatible import (check_for_requirements, copy_dir_tree,
                             get_module_dir_path, is_verbose_mode,
                             logo, make_tmp_thread_dir, mkdir)
from core.exit_helper import exit_failure, exit_success, terminate_thread
from core.get_modules import (load_all_modules,
                              virtual_machine_name_to_container_name,
                              virtual_machine_names_to_container_names)
from core.network import network_traffic_capture
from database.connector import (push_events_queues_to_database,
                                push_events_to_database_from_thread,
                                create_indices)
from core.messages import load_messages

# tmp dirs
tmp_directories = []
processor_threads = []
messages = load_messages().message_contents


def all_existing_networks():
    """
    list of all existing networks

    Returns:
        an array with list of all existing networks name
    """
    return [network_name.rsplit()[1] for network_name in
            os.popen("docker network ls").read().rsplit("\n")[1:-1]]


def create_ohp_networks():
    """
    create docker internet and internal network for OWASP Honeypot

    Returns:
        True
    """
    if "ohp_internet" not in all_existing_networks():
        info(messages["creating_ohp_internet"])
        os.popen("docker network create ohp_internet  --opt com.docker.network.bridge.enable_icc=true "
                 "--opt com.docker.network.bridge.enable_ip_masquerade=true "
                 "--opt com.docker.network.bridge.host_binding_ipv4=0.0.0.0 --opt "
                 "com.docker.network.driver.mtu=1500").read()
        network_json = json.loads(os.popen("docker network inspect ohp_internet").read())[
            0]["IPAM"]["Config"][0]
        info(messages["ohp_internet_network"].format(network_json["Subnet"],
                                                     network_json["Gateway"]))
    if "ohp_no_internet" not in all_existing_networks():
        info(messages["creating_ohp_no_internet"])
        os.popen("docker network create --attachable --internal ohp_no_internet  "
                 "--opt com.docker.network.bridge.enable_icc=true "
                 "--opt com.docker.network.bridge.enable_ip_masquerade=true "
                 "--opt com.docker.network.bridge.host_binding_ipv4=0.0.0.0 "
                 "--opt com.docker.network.driver.mtu=1500").read()
        network_json = json.loads(os.popen("docker network inspect ohp_no_internet").read())[
            0]["IPAM"]["Config"][0]
        info(messages["ohp_no_internet_network"].format(network_json["Subnet"],
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
    return [container.rsplit()[-1] for container in
            os.popen("docker ps").read().rsplit("\n")[1:-1]]


def all_existing_containers():
    """
    list of all existing containers

    Returns:
        an array with list of all existing containers name
    """
    return [container.rsplit()[-1] for container in
            os.popen("docker ps -a").read().rsplit("\n")[1:-1]]


def all_existing_images():
    """
    list of all existing images

    Returns:
        a array with list of all existing images name
    """
    return [
        container.rsplit()[0] for container in
        os.popen("docker images").read().rsplit("\n")[1:-1]
    ]


def stop_containers(configuration):
    """
    stop old containers based on images

    Args:
        configuration: user final configuration

    Returns:
        True
    """
    containers_list = running_containers()
    container_names = virtual_machine_names_to_container_names(configuration)
    if containers_list:
        for container in container_names:
            if container in containers_list:
                info(
                    "killing container {0}".format(
                        os.popen(
                            "docker kill {0}".format(
                                container
                            )
                        ).read().rsplit()[0]
                    )
                )
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
            info(
                "removing container {0}".format(
                    os.popen(
                        "docker rm {0}".format(container)
                    ).read().rsplit()[0]
                )
            )
    return True


def get_image_name_of_selected_modules(configuration):
    """
    get list of image name using user final configuration

    Args:
        configuration: user final configuration

    Returns:
        list of virtual machine image name
    """
    return virtual_machine_names_to_container_names(configuration)


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
            info(messages["removing_image"].format(image))
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
        # go to tmp folder to create Dockerfile and files dir
        tmp_dir_name = make_tmp_thread_dir()
        os.chdir(tmp_dir_name)
        # create files dir
        mkdir("files")

        # create Dockerfile
        dockerfile = open("Dockerfile", "w")
        dockerfile.write(configuration[selected_module]["dockerfile"])
        dockerfile.close()

        # copy files
        copy_dir_tree(configuration[selected_module]["files"], "files")

        # create docker image
        image_name = virtual_machine_name_to_container_name(
            configuration[selected_module]["virtual_machine_name"],
            selected_module
        )

        info(messages["creating_image"].format(image_name))

        # in case if verbose mode is enabled, we will be use os.system
        # instead of os.popen to show the outputs in case
        # of anyone want to be aware what's happening or what's the error,
        # it's a good feature for developers as well
        # to create new modules
        if is_verbose_mode():
            os.system("docker build . -t {0}".format(image_name))
        else:
            os.popen("docker build . -t {0}".format(image_name)).read()

        # created
        info(messages["image_created"].format(image_name))

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
        # using pattern name will help us to remove/modify the images and
        # modules
        container_name = virtual_machine_name_to_container_name(
            configuration[selected_module]["virtual_machine_name"],
            selected_module
        )
        configuration[selected_module]['container_name'] = container_name
        real_machine_port = configuration[selected_module]["real_machine_port_number"]
        virtual_machine_port = configuration[selected_module]["virtual_machine_port_number"]
        # connect to owasp honeypot networks!
        # run the container with internet access
        os.popen(
            "docker run {0} --net {4} --name={1} -d -t -p {2}:{3} {1}".format(
                " ".join(
                    configuration[selected_module]["extra_docker_options"]
                ),
                container_name,
                real_machine_port,
                virtual_machine_port,
                'ohp_internet' if configuration[selected_module]["virtual_machine_internet_access"]
                else 'ohp_no_internet'
            )
        ).read()
        try:
            virtual_machine_ip_address = os.popen(
                "docker inspect -f '{{{{range.NetworkSettings.Networks}}}}"
                "{{{{.IPAddress}}}}{{{{end}}}}' {0}".format(
                    container_name
                )
            ).read().rsplit()[0].replace("\'", "")  # single quotes needs to be removed in windows
        except Exception:
            virtual_machine_ip_address = "CANNOT_FIND_IP_ADDRESS"
        # add virtual machine IP Address to configuration
        configuration[selected_module]["ip_address"] = virtual_machine_ip_address
        # print started container information
        info(
            "container {0} started, forwarding 0.0.0.0:{1} to {2}:{3}".format(
                container_name,
                real_machine_port,
                virtual_machine_ip_address,
                virtual_machine_port
            )
        )
    return configuration


def containers_are_unhealthy(configuration):
    """
    check if all selected module containers are up and running!

    :param configuration: JSON container configuration
    :return: []/[containters]
    """
    unhealthy_containers = []
    for selected_module in configuration:
        container_name = configuration[selected_module]['container_name']
        unhealthy_containers.append(container_name)
    current_running_containers = running_containers()
    return [containter for containter in unhealthy_containers
            if containter not in current_running_containers]


def wait_until_interrupt(virtual_machine_container_reset_factory_time_seconds, configuration,
                         new_network_events_thread, run_as_test):
    """
    wait for opened threads/honeypots modules

    Returns:
        True
    """
    # running_time variable will be use to check
    # if its need to reset the container after a while
    # if virtual_machine_container_reset_factory_time_seconds < 0,
    # it will keep containers until user interruption
    running_time = 0
    while True:
        # while True sleep until user send ctrl + c
        try:
            time.sleep(1)
            running_time += 1
            # check if running_time is equal to reset factory time
            if running_time == virtual_machine_container_reset_factory_time_seconds:
                # reset the run time
                running_time = 0
                # stop old containers (in case they are not stopped)
                stop_containers(configuration)
                # remove old containers (in case they are not updated)
                remove_old_containers(configuration)
                # start containers based on selected modules
                start_containers(configuration)
            if not new_network_events_thread.is_alive():
                return error(messages["interrupt_application"])
            if containers_are_unhealthy(configuration):
                return error(
                    "Interrupting the application because \"{0}\" container(s) is(are) not alive!".format(
                        ", ".join(containers_are_unhealthy(configuration))
                    )
                )
            if run_as_test:
                break
        except KeyboardInterrupt:
            # break and return for stopping and removing containers/images
            info(messages["interrupted_by_user"])
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
    # the modules are available in lib/modules/category_name/module_name
    # (e.g. lib/modules/ftp/weak_password
    # they will be listed based on the folder names and if "Dockerfile" exist!
    # the Dockerfile will be read and add into JSON configuration (dockerfile)
    honeypot_configuration = {}
    for module in selected_modules:
        # read category configuration (e.g. ftp, ssh, http, etc..), they are
        # located in lib/modules/category/__init__.py
        # in the __init__.py every category has same function as below!
        # def category_configuration():
        #     return {
        #          "virtual_machine_name": "ohp_sshserver",
        #          "virtual_machine_port_number": 22,
        #          "virtual_machine_internet_access": False,
        #          "real_machine_port_number": 22
        #     }

        category_configuration = getattr(
            __import__(
                "modules.{0}".format(
                    module.rsplit("/")[0]),
                fromlist=["category_configuration"]
            ),
            "category_configuration"
        )
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
            __import__(
                "modules.{0}".format(
                    module.replace("/", ".")
                ), fromlist=["module_configuration"]
            ),
            "module_configuration"
        )

        # combine category + module configuration into one Dict/JSON
        combined_module_configuration = category_configuration()
        combined_module_configuration.update(module_configuration())
        # dockerfile
        dockerfile = open(
            os.path.join(
                get_module_dir_path(module_configuration),
                "Dockerfile"
            )
        ).read()
        # based on your configuration, the variables/values will be set into your Dockerfile
        # e.g. username will be replaced by {username} in Dockerfile
        combined_module_configuration["dockerfile"] = dockerfile.format(
            **combined_module_configuration
        )
        # add module files
        combined_module_configuration["files"] = os.path.join(
            get_module_dir_path(
                module_configuration
            ),
            "files"
        )
        # combine Dockerfile configuration with module and category
        # configuration
        honeypot_configuration[module] = combined_module_configuration
    return honeypot_configuration


def port_is_free(real_machine_port):
    """
    check if port is free

    Args:
        real_machine_port: port number

    Returns:
        True or False
    """
    try:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.bind(
            (
                "0.0.0.0",
                real_machine_port
            )
        )
        tcp.close()
        return True
    except Exception:
        return False


def reserve_tcp_port(real_machine_port, module_name, configuration):
    """
    pick a free port

    Args:
        real_machine_port: port number
        module_name: selected module
        configuration: fixed configuration

    Returns:
        port number
    """
    while True:
        try:
            if port_is_free(real_machine_port):
                # unique_port = True
                configuration[module_name]["real_machine_port_number"] = real_machine_port
                duplicated_ports = []
                for selected_module in configuration:
                    duplicated_ports.append(
                        configuration[selected_module]["real_machine_port_number"])
                if duplicated_ports.count(real_machine_port) == 1:
                    info(messages["port_selected"].format(real_machine_port, module_name))
                    return real_machine_port
        except Exception:
            pass
        real_machine_port += 1


def conflict_ports(configuration):
    """
    check conflict ports in configuration

    Args:
        configuration: user final configuration

    Returns:
        new fixed configuration
    """
    # todo: write documentation
    fixed_configuration = configuration.copy()
    for selected_module in configuration:
        port = reserve_tcp_port(
            configuration[selected_module]["real_machine_port_number"],
            selected_module,
            fixed_configuration
        )
        fixed_configuration[selected_module]["real_machine_port_number"] = port
    return fixed_configuration


def run_modules_processors(configuration):
    """
    run ModuleProcessor for each modules

    :param configuration: user final configuration
    :return:
    """
    for module in configuration:
        module_processor_thread = Thread(
            target=configuration[module]["module_processor"].processor,
            name=virtual_machine_name_to_container_name(
                configuration[module]["virtual_machine_name"],
                module
            )
        )
        module_processor_thread.start()
        processor_threads.append(module_processor_thread)
    return


def stop_modules_processors(configuration):
    """
    run ModuleProcessor for each modules

    :param configuration: user final configuration
    :return:
    """
    for module in configuration:
        configuration[module]["module_processor"].kill_flag = True

    while True:
        if True not in [
            module_processor_thread.is_alive() for module_processor_thread in processor_threads
        ]:
            break
        time.sleep(0.1)
    return


def set_network_configuration(argv_options):
    """
    Set network configuration based on user selections

    Args:
        argv_options

    Returns:
        network_config
    """
    network_config = network_configuration()
    # Set the values of the network configuration based on CLI input
    network_config["store_network_captured_files"] = argv_options.store_pcap
    network_config["split_pcap_file_timeout"] = argv_options.timeout_value

    return network_config


def update_language(argv_options):
    """
    Update language for messages

    Args:
        argv_options
    """
    if argv_options.language not in load_messages().languages_list:
        exit_failure("Invalid language code. Available options are " + ", ".join(load_messages().languages_list))


def argv_parser():
    """
    parse ARGVs using argparse

    Returns:
        parser, parsed ARGVs
    """
    # create parser
    parser = argparse.ArgumentParser(prog="OWASP Honeypot", add_help=False)
    # create menu
    docker_config = docker_configuration()
    user_config = user_configuration()
    engineOpt = parser.add_argument_group(
        "OHP Engine",
        "OHP Engine input options"
    )
    # add select module options + list of available modules
    engineOpt.add_argument(
        "-m", "--select-module",
        action="store",
        dest="selected_modules",
        default=user_config["default_selected_modules"],
        help="select module(s) {0}".format(
            load_all_modules() + ["all"]
        )
    )
    # by default all modules are selected, in case users can exclude one or
    # some (separated with comma)
    engineOpt.add_argument(
        "-x",
        "--exclude-module",
        action="store",
        dest="excluded_modules",
        default=user_config["default_excluded_modules"],
        help="select modules(s) to exclude {0}".format(
            load_all_modules()
        )
    )
    # limit the virtual machine storage to avoid related abuse
    engineOpt.add_argument(
        "-s",
        "--vm-storage-limit",
        action="store",
        dest="virtual_machine_storage_limit",
        type=float,
        default=docker_config["virtual_machine_storage_limit"],
        help="virtual machine storage limit"
    )
    # reset the containers once in a time to prevent being continues botnet
    # zombie
    engineOpt.add_argument(
        "-r",
        "--vm-reset-factory-time",
        action="store",
        dest="virtual_machine_container_reset_factory_time_seconds",
        type=int,
        default=docker_config["virtual_machine_container_reset_factory_time_seconds"],
        help="virtual machine reset factory time"
    )
    # start API
    engineOpt.add_argument(
        "--start-api-server",
        action="store_true",
        dest="start_api_server",
        default=False,
        help="start API server"
    )
    # Store Network captured files
    engineOpt.add_argument(
        "--store-pcap",
        action="store_true",
        dest="store_pcap",
        default=False,
        help="store network traffic as pcap files"
    )
    # Set Timeout value for splitting network captured files
    engineOpt.add_argument(
        "-t",
        "--split-pcap-file-timeout",
        type=int,
        dest="timeout_value",
        default=3600,
        help="timeout value used to split network captured files"
    )
    # enable verbose mode (debug mode)
    engineOpt.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose_mode",
        default=False,
        help="enable verbose mode"
    )
    # disable color CLI
    engineOpt.add_argument(
        "--disable-colors",
        action="store_true",
        dest="disable_colors",
        default=False,
        help="disable colors in CLI"
    )
    # set language
    engineOpt.add_argument(
        "--language",
        type=str,
        dest="language",
        default="en_US",
        help="Set the default language. {languages}".format(languages=load_messages().languages_list)
    )
    # test CI/ETC
    engineOpt.add_argument(
        "--test",
        action="store_true",
        dest="run_as_test",
        default=False,
        help="run a test and exit"
    )
    # help menu
    engineOpt.add_argument(
        "-h",
        "--help",
        action="store_true",
        default=False,
        dest="show_help_menu",
        help="print this help menu"
    )

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

    # check the language
    if argv_options.language:
        update_language(argv_options)
    #########################################
    # argv rules apply
    #########################################
    # check help menu
    if argv_options.show_help_menu:
        parser.print_help()
        exit_success()
    # check for requirements before start
    check_for_requirements(argv_options.start_api_server)
    # create indices before server start
    create_indices()
    # check api server flag
    if argv_options.start_api_server:
        start_api_server()
        exit_success()

    # Check if the script is running with sudo
    if not os.geteuid() == 0:
        exit_failure(messages['script_must_run_as_root'])
    # Check timeout value if provided
    if argv_options.timeout_value < 1:
        exit_failure(messages["timeout_error"])

    # check selected modules
    if argv_options.selected_modules:
        selected_modules = list(set(argv_options.selected_modules.rsplit(",")))
        if "all" in selected_modules:
            selected_modules = load_all_modules()
        if "" in selected_modules:
            selected_modules.remove("")
        # if selected modules are zero
        if not len(selected_modules):
            exit_failure(messages["no_module_selected_error"])
        # if module not found
        for module in selected_modules:
            if module not in load_all_modules():
                exit_failure("module {0} not found!".format(module))
    # check excluded modules
    if argv_options.excluded_modules:
        excluded_modules = list(set(argv_options.excluded_modules.rsplit(",")))
        if "all" in excluded_modules:
            exit_failure(messages["all_modules_excluded_error"])
        if "" in excluded_modules:
            excluded_modules.remove("")
        # remove excluded modules
        for module in excluded_modules:
            if module not in load_all_modules():
                exit_failure("module {0} not found!".format(module))
            # ignore if module not selected, it will remove anyway
            try:
                selected_modules.remove(module)
            except Exception:
                pass
        # if selected modules are zero
        if not len(selected_modules):
            exit_failure(messages["no_module_selected_error"])
    virtual_machine_container_reset_factory_time_seconds = argv_options. \
        virtual_machine_container_reset_factory_time_seconds
    run_as_test = argv_options.run_as_test
    #########################################
    # argv rules apply
    #########################################
    # build configuration based on selected modules
    configuration = honeypot_configuration_builder(selected_modules)
    # Set network configuration
    network_config = set_network_configuration(argv_options)
    info(messages["start_message"])
    info(messages["loading_modules"].format(", ".join(selected_modules)))
    # check for conflict in real machine ports and pick new ports
    info(messages["check_for_port_conflicts"])
    configuration = conflict_ports(configuration)
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
    # network capture process
    mp.set_start_method('spawn')
    # Event queues
    honeypot_events_queue = mp.Queue()
    network_events_queue = mp.Queue()
    # start a new process for network capture
    network_traffic_capture_process = mp.Process(
        target=network_traffic_capture,
        args=(
            configuration,
            honeypot_events_queue,
            network_events_queue,
            network_config,
        ),
        name="network_traffic_capture_process"
    )
    network_traffic_capture_process.start()
    info(
        messages["selected_modules_started"].format(
            ", ".join(
                selected_modules
            )
        )
    )
    # start a thread to push events to database regularly
    bulk_events_thread = Thread(
        target=push_events_to_database_from_thread,
        args=(honeypot_events_queue, network_events_queue,),
        name="insert_events_in_bulk_thread"
    )
    bulk_events_thread.start()

    # run module processors
    run_modules_processors(configuration)

    # wait forever! in case user can send ctrl + c to interrupt
    exit_flag = wait_until_interrupt(
        virtual_machine_container_reset_factory_time_seconds,
        configuration,
        network_traffic_capture_process,
        run_as_test
    )
    # killed the network traffic capture process by ctrl + c... waiting to end.
    info(messages["killing_capture_process"])
    if run_as_test:
        network_traffic_capture_process.terminate()
    # without ci it will be terminate after a few seconds, it needs to kill the tshark and update pcap file collection
    network_traffic_capture_process.join()
    # if in case any events that were not inserted from thread
    push_events_queues_to_database(honeypot_events_queue, network_events_queue)
    # Kill bulk events thread
    terminate_thread(bulk_events_thread)
    # stop created containers
    stop_containers(configuration)
    # stop module processor
    stop_modules_processors(configuration)
    # remove created containers
    remove_old_containers(configuration)
    # remove created images
    remove_old_images(configuration)
    # remove_tmp_directories() error: access denied!
    # kill all missed threads
    for thread in threading.enumerate()[1:]:
        terminate_thread(thread, False)
    info(messages["finished"])
    # reset cmd/terminal color
    reset_cmd_color()
    return exit_flag
