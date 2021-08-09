#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

elastic_search_types = {
    "honeypot": {
        'mappings': {
            'properties': {
                'ip_dest': {'type': 'ip'},
                'port_dest': {'type': 'integer'},
                'ip_src': {'type': 'ip'},
                'port_src': {'type': 'integer'},
                'protocol': {'type': 'keyword'},
                'module_name': {'type': 'keyword'},
                'machine_name': {'type': 'keyword'},
                'date': {
                    'type': 'date',
                    'format': 'yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis'
                },
                'country_ip_src': {'type': 'keyword'},
                'country_ip_dest': {'type': 'keyword'}
            }
        }
    },
    "network": {
        'mappings': {
            'properties': {
                'ip_dest': {'type': 'ip'},
                'port_dest': {'type': 'integer'},
                'ip_src': {'type': 'ip'},
                'port_src': {'type': 'integer'},
                'protocol': {'type': 'keyword'},
                'machine_name': {'type': 'keyword'},
                'date': {
                    'type': 'date',
                    'format': 'yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis'
                },
                'country_ip_src': {'type': 'keyword'},
                'country_ip_dest': {'type': 'keyword'}
            }
        }
    },
    "credential": {
        'mappings': {
            'properties': {
                'ip_src': {'type': 'ip'},
                'module_name': {'type': 'keyword'},
                'date': {
                    'type': 'date',
                    'format': 'yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis'
                },
                'username': {'type': 'keyword'},
                'password': {'type': 'keyword'},
                'machine_name': {'type': 'keyword'},
                'country_ip_src': {'type': 'keyword'}
            }
        }
    },
    "data": {
        'mappings': {
            'properties': {
                'ip_src': {'type': 'ip'},
                'module_name': {'type': 'keyword'},
                'date': {
                    'type': 'date',
                    'format': 'yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis'
                },
                'data': {'type': 'nested'},
                'machine_name': {'type': 'keyword'},
                'country_ip_src': {'type': 'keyword'}
            }
        }
    },
    "file": {
        'mappings': {
            'properties': {
                'file_path': {'type': 'text'},
                'module_name': {'type': 'keyword'},
                'date': {
                    'type': 'date',
                    'format': 'yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis'
                },
                'status': {'type': 'keyword'},
                'is_directory': {'type': 'boolean'},
                'machine_name': {'type': 'keyword'},
                'file_content': {'type': 'binary'}
            }
        }
    },
    "pcap": {
        'mappings': {
            'properties': {
                'file_path': {'type': 'text'},
                'date': {
                    'type': 'date',
                    'format': 'yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis'
                },
                'split_timeout': {'type': 'long'},
                'md5': {'type': 'keyword'},
                'file_content': {'type': 'binary'}
            }
        }
    }
}


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
        country_ip_src: Country of source IP Address
        country_ip_dest: Country of destination IP Address

    """

    def __init__(self, ip_dest, port_dest, ip_src,
                 port_src, protocol, module_name, machine_name):
        self.ip_dest = ip_dest
        self.port_dest = port_dest
        self.ip_src = ip_src
        self.port_src = port_src
        self.protocol = protocol
        self.module_name = module_name
        self.machine_name = machine_name
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.country_ip_src = None
        self.country_ip_dest = None


class NetworkEvent:
    """
    Object to store Network Event Parameters

    Attributes:
        ip_dest: Destination IP address (machine)
        port_dest: Destination port (machine)
        ip_src: Source IP address
        port_src: Source port
        date: Date and time of the event
        protocol: Protocol type of the packet
        machine_name: Real machine name
        country_ip_src: Country of source IP Address
        country_ip_dest: Country of destination IP Address
    """

    def __init__(
            self, ip_dest, port_dest,
            ip_src, port_src, protocol, machine_name):
        self.ip_dest = ip_dest
        self.port_dest = port_dest
        self.ip_src = ip_src
        self.port_src = port_src
        self.protocol = protocol
        self.machine_name = machine_name
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.country_ip_src = None
        self.country_ip_dest = None


class CredentialEvent:
    """
    Object to store Credential Event Parameters

    Attributes:
        ip_src: Client ip used for connecting to the module
        module_name: Which module was accessed
        date: Date and time of the event
        username: Username tried for connecting to modules
        password: Password tried for connecting to modules
        machine_name: Real machine name
        country_ip_src: Country corresponding to the IP Address
    """

    def __init__(self, ip_src, module_name, date, username, password):
        self.ip_src = ip_src
        self.module_name = module_name
        self.date = date
        self.username = username
        self.password = password
        self.machine_name = None
        self.country_ip_src = None


class EventData:
    """
    Object to store Honeypot Event Data collected from
    modules such as ICS Module.

    Attributes:
        ip: Client IP used for putting the data
        date: Date and time of the event
        module_name: Module client accessed by the client
        data: Data which is obtained from the client
        country_ip_src: Country corresponding to the IP Address
    """

    def __init__(self, ip, module_name, date, data):
        self.ip_src = ip
        self.module_name = module_name
        self.date = date
        self.data = data
        self.machine_name = None
        self.country_ip_src = None


class FileEventsData:
    """
    Object to store file changes events data collected from
    modules such as ftp/ssh weak_password module.

    Attributes:
        file_path : the path of the file which is changed
        status: status of the file would be added/modified/deleted
        module_name : on which module client accessed
        date : datetime of the event
        is_directory: is directory?
    """

    def __init__(self, file_path, status, module_name, date, is_directory):
        self.file_path = file_path
        self.module_name = module_name
        self.date = date
        self.status = status
        self.is_directory = is_directory
        self.machine_name = None
        self.file_content = None


class FileArchive:
    """
    Object to store details about captured network traffic files
    to be stored in the File Archive

    Attributes:
        file_path: the path of the PCAP file
        date: generation date and time of the file
        split_timeout: timeout value to be used to split PCAP files
    """

    def __init__(self, file_path, date, split_timeout):
        self.file_path = file_path
        self.date = date
        self.split_timeout = split_timeout
        self.md5 = None
        self.file_content = None
