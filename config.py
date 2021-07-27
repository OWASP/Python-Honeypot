#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import socket

from core.time_helper import hours
from core.compatible import generate_token

# Protocol number to protocol string table
protocol_table = {
    num: name[8:]
    for name, num in vars(socket).items()
    if name.startswith("IPPROTO")
}
real_machine_ip_address = socket.gethostbyname(socket.gethostname())


def api_configuration():
    """
    API Config (could be modify by user)

    Returns:
        a JSON with API configuration
    """
    # DOCKER_ENV variable is set in the docker-compose file.
    if os.environ.get('ELASTICSEARCH_DOCKER_ENV') == "true":
        db_url = "elasticsearch:9200"
    else:
        db_url = "127.0.0.1:9200"

    return {  # OWASP Honeypot API Default Configuration
        "api_host": "0.0.0.0",
        "api_port": 5000,
        "api_debug_mode": False,
        "api_access_without_key": True,
        "api_access_key": generate_token(),  # or any string, or None
        "api_client_white_list": {
            "enabled": False,
            "ips": [
                "127.0.0.1",
                "10.0.0.1",
                "192.168.1.1"
            ]
        },
        "api_access_log": {
            "enabled": False,
            "filename": "ohp_api_access.log"
        },
        # http://127.0.0.1:9200/ # todo: add SSL support later
        "api_database": db_url,
        "api_database_http_auth": ('elastic', 'changeme')
    }


def network_configuration():
    """
    network configuration

    Returns:
        JSON/Dict network configuration
    """
    return {
        "store_network_captured_files": False,
        "real_machine_ip_address": real_machine_ip_address,
        "ignore_real_machine_ip_address": True,  # or if you want to simulate from local network, save as False
        "ignore_virtual_machine_ip_addresses": True,  # or if you want simulate from local network, save as False
        "real_machine_identifier_name": "stockholm_server_1",  # can be anything e.g. real_machine_ip_address, name, etc
        "ignore_real_machine_ip_addresses": list(
            {
                real_machine_ip_address,
                "127.0.0.1"
            }
        ),
        # e.g. ["10.0.0.1", "192.168.1.1"]
        "ignore_real_machine_ports": [],  # e.g. [22, 80, 5000]
        "split_pcap_file_timeout": 3600  # Default value
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
        "language": "en_US",
        "events_log_file": "tmp/ohp.log",
        "default_selected_modules": "all",  # or select one or multiple (e.g. ftp/strong_password,ssh/strong_password)
        "default_excluded_modules": None  # or any module name separated with comma
    }
