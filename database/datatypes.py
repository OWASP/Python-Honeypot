#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from dataclasses import dataclass

@dataclass
class HoneypotEvent:
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
    ip_dest: str
    port_dest: int
    ip_src: str
    port_src: int
    module_name: str
    machine_name: str
    date: datetime = datetime.now()
    event_type: str = "honeypot_event"
    country_ip_src: str = None
    country_ip_dest: str = None
    

@dataclass
class NetworkEvent:
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
    ip_dest: str
    port_dest: int
    ip_src: str
    port_src: int
    machine_name: str
    date: datetime = datetime.now()
    country_ip_src: str = None
    country_ip_dest: str = None


@dataclass
class CredentialEvent:
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
    ip: str
    module_name: str
    date: datetime
    username: str
    password: str
    machine_name: str = None
    country: str = None


@dataclass
class ICSHoneypotEvent:
    """
    Object to store ICS Honeypot Event Parameters received from
    the ICS Module Processor

    Attributes:
        ip: Client IP used for putting the data
        date: Date and time of the event
        module_name: Module client accessed by the client
        data: Data which is obtained from the client
    """
    ip: str
    module_name: str
    date: datetime
    data: str
    machine_name: str = None
    country: str = None