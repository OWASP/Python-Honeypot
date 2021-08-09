#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import netaddr
import pyshark

from datetime import datetime
from config import (network_configuration,
                    protocol_table)
from core.alert import (error,
                        info,
                        warn)
from core.compatible import (is_verbose_mode,
                             get_timeout_error)
from core.get_modules import virtual_machine_name_to_container_name
from database.connector import (insert_to_honeypot_events_queue,
                                insert_to_network_events_queue,
                                insert_pcap_files_to_collection)
from database.datatypes import (HoneypotEvent,
                                NetworkEvent,
                                FileArchive)
from core.messages import load_messages

# honeypot ports
honeypot_ports = dict()
messages = load_messages().message_contents


def get_gateway_ip_addresses(configuration):
    """
    Get gateway ip addresses

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
            warn(
                messages["unable_to_get_ip"].format(
                    container_name
                )
            )
    return list(set(gateway_ips))


def force_kill_tshark():
    pid = os.popen('ps aux | grep tshark').readline().split()[1]
    os.popen('kill -9 {} &> /dev/null'.format(pid)).read()
    # wait to make sure tshark is gone!
    time.sleep(1)
    return


def process_packet(packet, honeypot_events_queue, network_events_queue):
    """
    Callback function called from the apply_on_packets function.

    Args:
        packet: Packet live captured by pyshark
        honeypot_events_queue: multiprocessing queue for storing honeypot events
        network_events_queue: multiprocessing queue for storing network events
    """
    # set machine name
    machine_name = network_configuration()["real_machine_identifier_name"]

    try:
        # Check if packet contains IP layer
        if "IP" in packet:
            ip_dest = packet.ip.dst
            ip_src = packet.ip.src
            protocol = protocol_table[int(packet.ip.proto)]
            port_dest = int()
            port_src = int()

            # Check packet protocol and if it contains a layer with the same
            # name
            if protocol == "TCP" and "TCP" in packet:
                port_dest = int(packet.tcp.dstport)
                port_src = int(packet.tcp.srcport)

            elif protocol == "UDP" and "UDP" in packet:
                port_dest = int(packet.udp.dstport)
                port_src = int(packet.udp.srcport)
            if netaddr.valid_ipv4(ip_dest) or netaddr.valid_ipv6(ip_dest):
                # ignored ip addresses and ports in python - fix later
                # check if the port is in selected module
                insert_to_honeypot_events_queue(
                    HoneypotEvent(
                        ip_dest,
                        port_dest,
                        ip_src,
                        port_src,
                        protocol,
                        honeypot_ports[port_dest if port_dest in honeypot_ports.keys() else port_src],
                        machine_name
                    ),
                    honeypot_events_queue
                ) if port_dest in honeypot_ports.keys() or port_src in honeypot_ports \
                    else insert_to_network_events_queue(
                    NetworkEvent(
                        ip_dest,
                        port_dest,
                        ip_src,
                        port_src,
                        protocol,
                        machine_name
                    ),
                    network_events_queue
                )

    except Exception as _e:
        del _e


def network_traffic_capture(configuration, honeypot_events_queue, network_events_queue, network_config):
    """
    Capture network traffic and submit new network and honeypot events to the database

    Args:
        configuration: user final configuration
        honeypot_events_queue: multiprocessing queue for storing honeypot events
        network_events_queue: multiprocessing queue for storing network events
        network_config: network configuration

    Returns:
        True
    """
    info(messages["network_traffic_capture_start"])

    for selected_module in configuration:
        port_number = configuration[selected_module]["real_machine_port_number"]

        honeypot_ports[port_number] = selected_module

    # get ip addresses
    virtual_machine_ip_addresses = [
        configuration[selected_module]["ip_address"]
        for selected_module in configuration
    ]

    # Ignore VM IPs + IPs in config.py
    # VM = virtual machine, RM = real machine
    ignore_rm_ip_addresses = network_config["ignore_real_machine_ip_address"]
    ignore_vm_ip_addresses = network_config["ignore_virtual_machine_ip_addresses"]

    # Ignore real machine IPs
    ignore_ip_addresses = network_config["ignore_real_machine_ip_addresses"] \
        if ignore_rm_ip_addresses else [] + virtual_machine_ip_addresses \
        if ignore_vm_ip_addresses else []

    ignore_ip_addresses.extend(get_gateway_ip_addresses(configuration))

    # Ignore ports
    ignore_ports = network_config["ignore_real_machine_ports"]

    # Display filter to be applied to the Live Captured network traffic
    display_filter = ' and '.join(['ip.src!={0} and ip.dst!={0}'.format(_) for _ in ignore_ip_addresses])
    display_filter += ' and ' if ignore_ip_addresses and ignore_ports else ""
    display_filter += ' and '.join(['tcp.srcport!={0} and tcp.dstport!={0}'.format(_) for _ in ignore_ports])

    store_pcap = network_config["store_network_captured_files"]
    timeout = network_config["split_pcap_file_timeout"]

    # Make the pcapfiles directory for storing the Network captured files
    base_dir_path = os.path.join(sys.path[0], "pcapfiles")

    def packet_callback(packet):
        """
        Callback function, called by apply_on_packets
        Args:
            packet
        """
        process_packet(
            packet,
            honeypot_events_queue,
            network_events_queue
        )

    # Run infinite loop and split the capture in multiple files using the timeout set
    # in the network configuration
    while True:
        # Timestamp to be used in file name
        file_timestamp = int(time.time())
        generation_time = datetime.fromtimestamp(file_timestamp).strftime("%Y-%m-%d %H:%M:%S")
        # File path of the network capture file with the timestamp
        output_file_path = os.path.join(
            base_dir_path,
            "captured-traffic-" + str(file_timestamp) + ".pcap"
        )

        if store_pcap:
            info(
                messages["network_capture_getting_stored"].format(
                    output_file_path
                )
            )

        try:
            capture = pyshark.LiveCapture(
                interface='any',
                display_filter=display_filter,
                output_file=output_file_path if store_pcap else None
            )

            # Debug option for pyshark capture
            if is_verbose_mode():
                capture.set_debug()

            # Applied on every packet captured by pyshark LiveCapture
            capture.apply_on_packets(packet_callback, timeout=timeout)

        except get_timeout_error() as e:
            force_kill_tshark()
            # Catches the timeout error thrown by apply_on_packets
            insert_pcap_files_to_collection(
                FileArchive(
                    output_file_path,
                    generation_time,
                    timeout
                )
            ) if store_pcap else e

        except KeyboardInterrupt as e:
            force_kill_tshark()
            insert_pcap_files_to_collection(
                FileArchive(
                    output_file_path,
                    generation_time,
                    timeout
                )
            ) if store_pcap else e
            break

        except Exception as e:
            force_kill_tshark()
            insert_pcap_files_to_collection(
                FileArchive(
                    output_file_path,
                    generation_time,
                    timeout
                )
            ) if store_pcap else e
            error(str(e))
            break

    return True
