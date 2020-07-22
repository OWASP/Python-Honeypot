#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import select
import subprocess
import time

import netaddr

from config import network_configuration
from core.alert import info, warn
from core.compatible import byte_to_str
from core.exit_helper import exit_failure
from core.get_modules import virtual_machine_name_to_container_name
from database.connector import (insert_to_network_events_queue,
                                insert_to_honeypot_events_queue)
from database.datatypes import HoneypotEvent, NetworkEvent


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
        try:
            gateway_ip = os.popen(
                "docker inspect -f '{{{{range.NetworkSettings.Networks}}}}"
                "{{{{.Gateway}}}}{{{{end}}}}' {0}".format(container_name)
            ).read().rsplit()[0].replace("\'", "")
            gateway_ips.append(gateway_ip)
        except IndexError:
            warn("unable to get container {0} IP address".format(container_name))
    return list(set(gateway_ips))


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
        rules.append("-Y ip.dst!={0}".format(ip_address))
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
    # honeypot ports
    honeypot_ports = []
    virtual_machine_ip_addresses = []
    network_config = network_configuration()
    for selected_module in configuration:
        port_number = configuration[selected_module]["real_machine_port_number"]
        ip_address = configuration[selected_module]["ip_address"]
        honeypot_ports.append(port_number)
        # get ip addresses
        virtual_machine_ip_addresses.append(ip_address)
    # set machine name
    machine_name = network_config["real_machine_identifier_name"]
    # ignore vm ips + ips in config.py
    # vm = virtual machine, rm = real machine
    ignore_rm_ip_addresses = network_config["ignore_real_machine_ip_address"]
    ignore_vm_ip_addresses = network_config["ignore_virtual_machine_ip_addresses"]
    ignore_ip_addresses = network_config["ignore_real_machine_ip_addresses"] \
        if ignore_rm_ip_addresses else [] + virtual_machine_ip_addresses \
        if ignore_vm_ip_addresses else []
    ignore_ip_addresses.extend(get_gateway_ip_addresses(configuration))
    # ign
    # ore ports
    ignore_ports = network_config["ignore_real_machine_ports"]
    # start tshark to capture network
    # tshark -Y "ip.dst != 192.168.1.1" -T fields -e ip.dst -e tcp.srcport
    run_tshark = ["tshark", "-l", "-V"]
    run_tshark.extend(ignore_ip_addresses_rule_generator(ignore_ip_addresses))
    run_tshark.extend(
        [
            "-T", "fields", "-e", "ip.dst", "-e", "ip.src",
            "-e", "tcp.dstport", "-e", "tcp.srcport", "-ni", "any"
        ]
    )
    process = subprocess.Popen(
        run_tshark,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    # wait 3 seconds if process terminated?
    time.sleep(3)
    if process.poll() is not None:
        exit_failure("tshark couldn't capture network, maybe run as root!")
    # todo: replace tshark with python port sniffing -
    # e.g https://www.binarytides.com/python-packet-sniffer-code-linux/
    # it will be easier to apply filters and analysis packets with python
    # if it requires to be run as root,
    # please add a uid checker in framework startup

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
                        line = line.rsplit()
                        ip_dest = byte_to_str(line[0])
                        ip_src = byte_to_str(line[1])
                        port_dest = int(line[2])
                        port_src = int(line[3])
                        if (netaddr.valid_ipv4(ip_dest) or
                            netaddr.valid_ipv6(ip_dest)) \
                                and ip_dest not in ignore_ip_addresses \
                                and ip_src not in ignore_ip_addresses \
                                and port_dest not in ignore_ports \
                                and port_src not in ignore_ports:
                            # ignored ip addresses and ports in python -fix later
                            # check if the port is in selected module

                            if (port_dest in honeypot_ports or
                                    port_src in honeypot_ports):
                                if port_dest in honeypot_ports:
                                    insert_to_honeypot_events_queue(
                                        HoneypotEvent(
                                            ip_dest=ip_dest,
                                            port_dest=port_dest,
                                            ip_src=ip_src,
                                            port_src=port_src,
                                            module_name=selected_module,
                                            machine_name=machine_name
                                        )
                                    )
                            else:
                                insert_to_network_events_queue(
                                    NetworkEvent(
                                        ip_dest=ip_dest,
                                        port_dest=port_dest,
                                        ip_src=ip_src,
                                        port_src=port_src,
                                        machine_name=machine_name
                                    )
                                )
                    except Exception:
                        pass
                    # check if event shows an IP
            time.sleep(0.001)
            # todo: is sleep(0.001) fastest/best?
            # it means it could get 1000 packets per second(maximum) from
            # tshark
            # how could we prevent the DDoS attacks in here
            # and avoid submitting in MongoDB? should we?
    except Exception as _:
        del _
    return True
