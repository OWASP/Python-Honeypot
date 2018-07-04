#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.get_modules import load_all_modules
from core.alert import info
from core.color import finish
from core.alert import messages
from core.compatible import logo
from core.compatible import version
from core.compatible import os_name
from config import user_configuration

# temporary use fixed version of argparse
if os_name() == "win32" or os_name() == "win64":
    if version() is 2:
        from lib.argparse.v2 import argparse
    else:
        from lib.argparse.v3 import argparse
else:
    import argparse


def argv_parser():
    parser = argparse.ArgumentParser(prog="Nettacker", add_help=False)
    engineOpt = parser.add_argument_group(messages("en", "engine"), messages("en", "engine_input"))
    engineOpt.add_argument("-m", "--select-module", action="store",
                           dest="selected_modules", default=user_configuration()["default_selected_modules"],
                           help=messages("en", "select_module").format(load_all_modules()))
    engineOpt.add_argument("-x", "--exclude-module", action="store",
                           dest="selected_modules", default=user_configuration()["default_excluded_modules"],
                           help=messages("en", "exclude_module").format(load_all_modules()))
    engineOpt.add_argument("-s", "--vm-storage-limit", action="store",
                           dest="virtual_machine_storage_limit", type=float,
                           default=user_configuration()["virtual_machine_storage_limit"],
                           help=messages("en", "vm_storage_limit"))
    engineOpt.add_argument("-r", "--vm-reset-factory-time", action="store",
                           dest="virtual_machine_storage_limit", type=float,
                           default=user_configuration()["virtual_machine_container_reset_factory_time"],
                           help=messages("en", "vm_reset_factory_time"))
    

def load_honeypot_engine():
    logo()
    info(messages("en", "honeypot_started"))
    info(messages("en", "available_modules"))
    for module in load_all_modules():
        info(module)

    finish()
    return True
