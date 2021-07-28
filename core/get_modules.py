#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import inspect
import modules

from glob import glob
from core.alert import warn
from core.messages import load_messages

messages = load_messages().message_contents


def virtual_machine_names_to_container_names(configuration):
    """
    convert virtual machine names to container names using configuration
    Args:
        configuration: user final configuration

    Returns:
        list of container name in array
    """
    return [
        "{0}_{1}".format(
            configuration[selected_module]["virtual_machine_name"],
            selected_module.rsplit("/")[1]
        )
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
    # the modules are available in
    # modules/category_name/module_name (e.g. modules/ftp/weak_password
    # they will be listed based on the folder names and if "Dockerfile" exist!
    # structure of module name:
    # module_name = modules/(category_name/module_name)/__init.py
    # example: module_name = modules/(ftp/weak_password)/__init.py
    #                      = ftp/weak_password
    module_names = []
    module_basepath = os.path.dirname(inspect.getfile(modules))
    path_pattern = module_basepath + '/*/*/__init__.py'

    for module in glob(path_pattern):

        module_dir = os.path.split(module)[0]
        sub_module_name = os.path.split(module_dir)[1]
        category_name = os.path.split(os.path.split(module_dir)[0])[1]
        module_name = category_name + '/' + sub_module_name
        dockerfile_path = os.path.join(module_dir, "Dockerfile")

        if os.path.exists(dockerfile_path):
            if module_name not in module_names:
                module_names.append(module_name)
        else:
            warn(messages["module_not_available"].format(module_name))
    return module_names
