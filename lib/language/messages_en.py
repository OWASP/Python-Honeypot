#!/usr/bin/env python
# -*- coding: utf-8 -*-


def all_messages():
    """
    keep all messages in en

    Returns:
        all messages in JSON
    """
    return \
        {
            "honeypot_started": "OWASP Honeypot started ...",
            "loading_modules": "loading modules {0}",
            "module_not_available": "module {0} is not available",
            "docker_error": "cannot communicate with docker, please install and start the docker service!",
            "engine": "OHP Engine",
            "engine_input": "OHP Engine input options",
            "select_module": "select module(s) {0}",
            "exclude_module": "select modules(s) to exclude {0}",
            "vm_storage_limit": "virtual machine storage limit",
            "vm_reset_factory_time": "virtual machine reset factory time",
            "show_help_menu": "print this help menu",
            "zero_module_selected": "no module selected, please select one at least!",
            "module_not_found": "module {0} not found!",
            "python_docker_not_installed": "python docker library not installed, please run pip install "
                                           "docker (docker==2.7.0 for python 2.7.x and docker for python 3.x)"
        }
