#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime


class HoneypotEvent(object):
    """
    Object to store Honeypot Event Parameters.

    Attributes:
        ip_dest: Destination IP address (machine)
        port_dest: Destination port (machine)
        ip_src: Source IP address
        port_src: Source port
        date: Date and time of the event
        module_name: Module name ran on the port
        machine_name: Real machine name
        event_type: Type of event
        country_ip_src: Country of source IP Address
        country_ip_dest: Country of destination IP Address

    """
    def __init__(
                self, ip_dest, port_dest, ip_src,
                port_src, module_name, machine_name):

        self.ip_dest = ip_dest
        self.port_dest = port_dest
        self.ip_src = ip_src
        self.port_src = port_src
        self.module_name = module_name
        self.machine_name = machine_name
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.event_type = "honeypot_event"
        self.country_ip_src = None
        self.country_ip_dest = None


class NetworkEvent(object):
    """
    Object to store Network Event Parameters

    Attributes:
        ip_dest: Destination IP address (machine)
        port_dest: Destination port (machine)
        ip_src: Source IP address
        port_src: Source port
        date: Date and time of the event
        machine_name: Real machine name
        country_ip_src: Country of source IP Address
        country_ip_dest: Country of destination IP Address
    """

    def __init__(
                self, ip_dest, port_dest,
                ip_src, port_src, machine_name):

        self.ip_dest = ip_dest
        self.port_dest = port_dest
        self.ip_src = ip_src
        self.port_src = port_src
        self.machine_name = machine_name
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.country_ip_src = None
        self.country_ip_dest = None


class CredentialEvent(object):
    """
    Object to store Credential Event Parameters

    Attributes:
        ip: Client ip used for connecting to the module
        module_name: Which module was accessed
        date: Date and time of the event
        username: Username tried for connecting to modules
        password: Password tried for connecting to modules
        machine_name: Real machine name
        country: Country corresponding to the IP Address
    """

    def __init__(self, ip, module_name, date, username, password):
        self.ip = ip
        self.module_name = module_name
        self.date = date
        self.username = username
        self.password = password
        self.machine_name = None
        self.country = None


class EventData(object):
    """
    Object to store Honeypot Event Data collected from
    modules such as ICS Module.

    Attributes:
        ip: Client IP used for putting the data
        date: Date and time of the event
        module_name: Module client accessed by the client
        data: Data which is obtained from the client
    """

    def __init__(self, ip, module_name, date, data):
        self.ip = ip
        self.module_name = module_name
        self.date = date
        self.data = data
        self.machine_name = None
        self.country = None
