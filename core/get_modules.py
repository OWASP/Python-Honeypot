#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import inspect
import lib
from glob import glob
from core.compatible import is_windows
from core.alert import (warn,messages)


def virtual_machine_names_to_container_names(configuration):
    """
    convert virtual machine names to container names using configuration
    Args:
        configuration: user final configuration

    Returns:
        list of container name in array
    """
    return [
        "{0}_{1}".format(configuration[selected_module]["virtual_machine_name"],
                         selected_module.rsplit("/")[1])
        for selected_module in configuration
    ]


def virtual_machine_name_to_container_name(virtual_machine_name, module_name):
    """
    virtual machine name to container name

    Args:
        module_name: select module name
        virtual_machine_name: virtual machine name

    Returns:
        string(container name)
    """
    return "{0}_{1}".format(virtual_machine_name, module_name.rsplit("/")[1])


def load_all_modules():
    """
    load all available modules

    Returns:
        an array of all module names
    """
    # Search for Modules
    # the modules are available in lib/modules/category_name/module_name
    # (e.g. lib/modules/ftp/weak_password)
    # they will be listed based on the folder names and if "Dockerfile" exist!
    # structure of module name:
    # module_name = lib/modules/(category_name/module_name)/__init.py
    # for example:
    # module_name = lib/modules/ftp/weak_password/__init.py = ftp/weak_password
    module_names = []
    module_directory = os.path.dirname(inspect.getfile(lib)) + \
                       '/modules/*/*/__init__.py'
    for module in glob(module_directory):
        module_name = module.rsplit('\\' if is_windows() else '/')[-3] + '/' + \
                      module.rsplit('\\' if is_windows() else '/')[-2]
        if os.path.exists(module.rsplit('__init__.py')[0] + '/' + 'Dockerfile'):
            if module_name not in module_names:
                module_names.append(module_name)
        else:
            warn(messages("en", "module_not_available").format(module_name))
    return module_names
