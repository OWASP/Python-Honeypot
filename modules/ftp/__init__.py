#!/usr/bin/env python
# -*- coding: utf-8 -*-


def category_configuration():
    """
    category configuration

    Returns:
        JSON/Dict category configuration
    """
    return {
        "virtual_machine_name": "ohp_ftpserver",
        "virtual_machine_port_number": 21,
        "virtual_machine_internet_access": True,
        "real_machine_port_number": 21
    }
