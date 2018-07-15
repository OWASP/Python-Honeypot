#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import socket

from core._time import hours


def api_configuration():
    """
    API Config (could be modify by user)

    Returns:
        a JSON with API configuration
    """
    return {  # OWASP Honeypot API Default Configuration
        "api_host": "127.0.0.1",
        "api_port": 5000,
        "api_debug_mode": False,
        "api_access_key": "".join(random.choice("0123456789abcdef") for x in range(32)),
        "api_client_white_list": {
            "enabled": False,
            "ips": ["127.0.0.1", "10.0.0.0/24", "192.168.1.1-192.168.1.255"]
        },
        "api_access_log": {
            "enabled": False,
            "filename": "ohp_api_access.log"
        },
        "api_database": "mongodb://127.0.0.1:27017/",  # mongodb://user:password@127.0.0.1:27017/
        "api_database_connection_timeout": 2000,  # miliseconds
        "api_database_name": "ohp_events"
    }


def network_configuration():
    """
    network configuration

    Returns:
        JSON/Dict network configuration
    """
    return {
        "store_network_captured_files": False,
        "real_machine_ip_address": socket.gethostbyname(socket.gethostname())
    }


def docker_configuration():
    """
    docker configuration

    Returns:
        JSON/Dict docker configuration
    """
    return {
        "virtual_machine_storage_limit": 0.5,  # Gigabyte
        "virtual_machine_container_reset_factory_time_seconds": hours(-1),  # -1 is equals to never reset!

    }


def user_configuration():
    """
        user configuration

    Returns:
        JSON/Dict user configuration
    """
    return {
        "language": "en",
        "default_selected_modules": "ftp/weak_password,ssh/weak_password,http/basic_auth_weak_password",
        "default_excluded_modules": None,
    }
