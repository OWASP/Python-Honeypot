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

# temporary use fixed version of argparse
if os_name() == "win32" or os_name() == "win64":
    if version() is 2:
        from lib.argparse.v2 import argparse
    else:
        from lib.argparse.v3 import argparse
else:
    import argparse


def wait_until_interrupt():
    """
    wait for opened threads/honeypots modules

    Returns:
        True
    """
    while True:
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
    honeypot_configuration = {}
    for module in selected_modules:
        category_configuration = getattr(
            __import__("lib.modules.{0}".format(module.rsplit("/")[0]), fromlist=["category_configuration"]),
            "category_configuration")
        module_configuration = getattr(
            __import__("lib.modules.{0}".format(module.replace("/", ".")), fromlist=["module_configuration"]),
            "module_configuration")
        combined_module_configuration = module_configuration()
        combined_module_configuration.update(category_configuration())
        combined_module_configuration["dockerfile"] = open(
            os.path.dirname(inspect.getfile(module_configuration)) + '/Dockerfile').read()
        combined_module_configuration["docker_compose"] = open(
            os.path.dirname(inspect.getfile(module_configuration)) + '/docker-compose.yml').read()
        honeypot_configuration[module] = combined_module_configuration
    return honeypot_configuration


def argv_parser():
    """
    parse ARGVs using argparse

    Returns:
        parser, parsed ARGVs
    """
    parser = argparse.ArgumentParser(prog="Nettacker", add_help=False)
    engineOpt = parser.add_argument_group(messages("en", "engine"), messages("en", "engine_input"))
    engineOpt.add_argument("-m", "--select-module", action="store",
                           dest="selected_modules", default=user_configuration()["default_selected_modules"],
                           help=messages("en", "select_module").format(load_all_modules()))
    engineOpt.add_argument("-x", "--exclude-module", action="store",
                           dest="excluded_modules", default=user_configuration()["default_excluded_modules"],
                           help=messages("en", "exclude_module").format(load_all_modules()))
    engineOpt.add_argument("-s", "--vm-storage-limit", action="store",
                           dest="virtual_machine_storage_limit", type=float,
                           default=docker_configuration()["virtual_machine_storage_limit"],
                           help=messages("en", "vm_storage_limit"))
    engineOpt.add_argument("-r", "--vm-reset-factory-time", action="store",
                           dest="virtual_machine_container_reset_factory_time", type=int,
                           default=docker_configuration()["virtual_machine_container_reset_factory_time"],
                           help=messages("en", "vm_reset_factory_time"))
    engineOpt.add_argument("-h", "--help", action="store_true", default=False, dest="show_help_menu",
                           help=messages("en", "show_help_menu"))
    return parser, parser.parse_args()


def load_honeypot_engine():
    """
    load OHP Engine

    Returns:
        True
    """
    logo()
    parser, argv_options = argv_parser()
    # check help menu
    if argv_options.show_help_menu:
        parser.print_help()
        finish()
        __die_success()
    # check selected modules
    if argv_options.selected_modules:
        selected_modules = list(set(argv_options.selected_modules.rsplit(',')))
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
        excluded_modules = list(set(argv_options.excluded_modules.rsplit(',')))
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
                _
        # if selected modules are zero
        if not len(selected_modules):
            __die_failure(messages("en", "zero_module_selected"))

    info(messages("en", "honeypot_started"))
    info(messages("en", "loading_modules").format(", ".join(selected_modules)))
    print(json.dumps(honeypot_configuration_builder(selected_modules), indent=4, sort_keys=True))
    # wait for honeypots modules and threads to keep them open
    # wait_until_interrupt()
    finish()
    return True
