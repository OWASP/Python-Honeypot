#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import netaddr
import select
import time

from database.connector import insert_selected_modules_network_event
from database.connector import insert_other_network_event
from core.alert import info
from config import network_configuration


def new_network_events(configuration):
    """
    get and submit new network events

    Args:
        configuration: user final configuration

    Returns:
        True
    """
    info("new_network_events thread started")
    # start tshark to capture network
    # tshark -Y "ip.dst != 192.168.1.1" -T fields -e ip.dst -e tcp.srcport
    process = subprocess.Popen(
        ["tshark", "-Y", "ip.dst != {0}".format(network_configuration()["real_machine_ip_address"]), "-T",
         "fields", "-e", "ip.dst", "-e", "tcp.srcport", "-ni", "any"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
                            and ip not in network_configuration()["ignore_real_machine_ip_addresses"] \
                            and port not in network_configuration()["ignore_real_machine_ports"]:
                        # check if the port is in selected module
                        inserted_flag = True
                        for selected_module in configuration:
                            if port is configuration[selected_module]["real_machine_port_number"]:
                                # insert honeypot event (selected module)
                                insert_selected_modules_network_event(ip, port, selected_module)
                                inserted_flag = False
                                break
                        if inserted_flag:
                            # insert common network event
                            insert_other_network_event(ip, port)
            time.sleep(0.2)
    except Exception as _:
        del _
    return True
