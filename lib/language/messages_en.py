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
            "available_modules": "list of available modules",
            "module_not_available": "module {0} is not available",
            "docker_error": "cannot communicate with docker, please install and start the docker service!",
            "engine": "OHP Engine",
            "engine_input": "OHP Engine input options",
            "select_module": "select module(s) {0}",
            "exclude_module": "select modules(s) to exclude {0}",
            "vm_storage_limit": "virtual machine storage limit",
            "vm_reset_factory_time": "virtual machine reset factory time",


        }
