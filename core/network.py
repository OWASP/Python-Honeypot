#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import netaddr
import select
import time
import os

from database.connector import insert_selected_modules_network_event
from database.connector import insert_other_network_event
from core.alert import info
from config import network_configuration
from core.get_modules import virtual_machine_name_to_container_name


def get_gateway_ip_addresses(configuration):
    """
    get gateway ip addresses

    Args:
        configuration: user final configuration

    Returns:
        list of gateway's IPs
    """
    gateway_ips = []
    for selected_module in configuration:
        container_name = virtual_machine_name_to_container_name(
            configuration[selected_module]["virtual_machine_name"],
            selected_module
        )
        gateway_ip = os.popen(
            "docker inspect -f '{{{{range.NetworkSettings.Networks}}}}"
            "{{{{.Gateway}}}}{{{{end}}}}' {0}".format(container_name)
        ).read().rsplit()[0].replace("\'", "")
        gateway_ips.append(gateway_ip)
    return gateway_ips


def ignore_ip_addresses_rule_generator(ignore_ip_addresses):
    """
    generate tshark rule to ignore ip addresses

    Args:
        ignore_ip_addresses: list of ip addresses

    Returns:
        rule string
    """
    rules = []
    for ip_address in ignore_ip_addresses:
        rules.append("-Y ip.dst != {0}".format(ip_address))
    return rules


def new_network_events(configuration):
    """
    get and submit new network events

    Args:
        configuration: user final configuration

    Returns:
        True
    """
    info("new_network_events thread started")
    # get ip addresses
    virtual_machine_ip_addresses = [configuration[selected_module]["ip_address"] for selected_module in configuration]
    # ignore vm ips + ips in config.py
    ignore_ip_addresses = network_configuration()["ignore_real_machine_ip_addresses"] + virtual_machine_ip_addresses
    ignore_ip_addresses.append(network_configuration()["real_machine_ip_address"])
    ignore_ip_addresses.append(get_gateway_ip_addresses(configuration))
    # ignore ports
    ignore_ports = network_configuration()["ignore_real_machine_ports"]
    # start tshark to capture network
    # tshark -Y "ip.dst != 192.168.1.1" -T fields -e ip.dst -e tcp.srcport
    run_tshark = ["tshark"]
    run_tshark.extend(ignore_ip_addresses_rule_generator(ignore_ip_addresses))
    run_tshark.extend(
        [
            "-T", "fields", "-e", "ip.dst", "-e", "tcp.srcport", "-ni", "any"
        ]
    )
    process = subprocess.Popen(
        run_tshark,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    # todo: replace tshark with python port forwarding
    # readline timeout bug fix: https://stackoverflow.com/a/10759061
    pull_object = select.poll()
    pull_object.register(process.stdout, select.POLLIN)
    # while True, read tshark output
    try:
        while True:
            if pull_object.poll(0):
                line = process.stdout.readline()
                # check if new IP and Port printed
                if len(line) > 0:
                    # split the IP and Port
                    try:
                        ip, port = line.rsplit()[0], int(line.rsplit()[1])
                    except Exception as _:
                        ip, port = None, None
                    # check if event shows an IP
                    if (netaddr.valid_ipv4(ip) or netaddr.valid_ipv6(ip)) \
                            and ip not in ignore_ip_addresses \
                            and port not in ignore_ports:  # ignored ip addresses and ports in python - fix later
                        # check if the port is in selected module
                        inserted_flag = True
                        for selected_module in configuration:
                            if port == configuration[selected_module]["real_machine_port_number"]:
                                # insert honeypot event (selected module)
                                insert_selected_modules_network_event(ip, port, selected_module)
                                inserted_flag = False
                                break
                        if inserted_flag:
                            # insert common network event
                            insert_other_network_event(ip, port)
            time.sleep(0.001)
            # todo: is sleep(0.001) fastest/best?
    except Exception as _:
        del _
    return True
