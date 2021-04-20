#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect
import os
import time
import elasticsearch
import hashlib
import binascii

from multiprocessing import Queue

from config import api_configuration, network_configuration
from core.alert import verbose_info
from core.compatible import byte_to_str, is_verbose_mode
from database.datatypes import (CredentialEvent,
                                HoneypotEvent,
                                EventData,
                                NetworkEvent,
                                FileEventsData,
                                FileArchive,
                                elastic_search_types)
from lib.ip2location import IP2Location
from api.database_queries import event_types

api_config = api_configuration()
network_config = network_configuration()

# Event index connections
elasticsearch_events = elasticsearch.Elasticsearch(
    api_config["api_database"],
    http_auth=api_config["api_database_http_auth"],
)

event_types_elastic = event_types.copy()
del event_types_elastic['all']

for event_type in event_types_elastic:
    elasticsearch_events.indices.create(
        index=event_types_elastic[event_type],
        body=elastic_search_types[event_type],
        ignore=400
    )

# Event queues
honeypot_events_queue = list()
network_events_queue = list()

IP2Location = IP2Location.IP2Location(
    os.path.join(
        os.path.dirname(
            inspect.getfile(IP2Location)
        ),
        "IP2LOCATION-LITE-DB1.BIN")
)


# todo: write documentation about machine_name

def insert_to_honeypot_events_queue(honeypot_event: HoneypotEvent, honeypot_events_queue: Queue):
    """
    insert selected modules event to honeypot_events_queue

    Args:
        honeypot_event: Object of HoneypotEvent class with event parameters
        honeypot_events_queue: Multiprocessing queue which stores the list of
                               honeypot_events in _dict_ format

    Returns:
        ObjectId(inserted_id)
    """
    if is_verbose_mode():
        verbose_info(
            "Received honeypot event, ip_dest:{0}, port_dest:{1}, "
            "ip_src:{2}, port_src:{3}, module_name:{4}, machine_name:{5}".format(
                honeypot_event.ip_dest,
                honeypot_event.port_dest,
                honeypot_event.ip_src,
                honeypot_event.port_src,
                honeypot_event.module_name,
                honeypot_event.machine_name
            )
        )

    # Get country of the source IP Address
    honeypot_event.country_ip_src = byte_to_str(
        IP2Location.get_country_short(
            honeypot_event.ip_src
        ))

    # Get country of the destination IP Address
    honeypot_event.country_ip_dest = byte_to_str(
        IP2Location.get_country_short(
            honeypot_event.ip_dest
        ))

    honeypot_events_queue.put(honeypot_event.__dict__)

    return


def insert_to_network_events_queue(network_event: NetworkEvent, network_events_queue: Queue):
    """
    insert other network events (port scan, etc..) to network_events_queue

    Args:
        network_event: Object of NetworkEvent Class with event parameters
        network_events_queue: Multiprocessing queue which stores the list of
                              network_events in _dict_ format

    Returns:
        ObjectId(inserted_id)
    """
    if is_verbose_mode():
        verbose_info(
            "Received network event, ip_dest:{0}, port_dest:{1}, "
            "ip_src:{2}, port_src:{3}, machine_name:{4}".format(
                network_event.ip_dest,
                network_event.port_dest,
                network_event.ip_src,
                network_event.port_src,
                network_event.machine_name
            )
        )

    # Get country of the source IP Address
    network_event.country_ip_src = byte_to_str(
        IP2Location.get_country_short(
            network_event.ip_src
        )
    )

    # Get country of the destination IP Address
    network_event.country_ip_dest = byte_to_str(
        IP2Location.get_country_short(
            network_event.ip_dest
        )
    )

    network_events_queue.put(network_event.__dict__)

    return


def push_events_queues_to_database(honeypot_events_queue, network_events_queue):
    """
    Pushes all honeypot and network events collected in the
    honeypot_events_queue and network_events_queue to honeypot_events
    and network_events collection respectively
    """

    if is_verbose_mode() and (honeypot_events_queue or network_events_queue) \
            and (honeypot_events_queue or network_events_queue):
        verbose_info("Submitting new events to database")

    # Insert all honeypot events to database (honeypot_events collection)
    while not honeypot_events_queue.empty():
        new_event = honeypot_events_queue.get()
        elasticsearch_events.index(index='honeypot_events', body=new_event)

    # Insert all network events to database (network_events collection)
    while not network_events_queue.empty():
        new_event = network_events_queue.get()
        elasticsearch_events.index(index='network_events', body=new_event)

    return


def push_events_to_database_from_thread(honeypot_events_queue, network_events_queue):
    """
    Thread function for inserting bulk events in a thread

    Returns:
        True/None
    """
    while True:
        push_events_queues_to_database(honeypot_events_queue, network_events_queue)
        time.sleep(1)
    return True


def insert_to_credential_events_collection(credential_event: CredentialEvent):
    """
    insert credentials from honeypot events which are obtained
    from the module processor to credential_event collection

    Args:
        credential_event: Object of CredentialEvent Class with honeypot
                          event credentials

    Returns:
        inserted_id
    """
    credential_event.country_ip_src = byte_to_str(
        IP2Location.get_country_short(
            credential_event.ip_src
        )
    )

    credential_event.machine_name = network_config["real_machine_identifier_name"]

    if is_verbose_mode():
        verbose_info(
            "Received honeypot credential event, ip_dest:{0}, username:{1}, "
            "password:{2}, module_name:{3}, machine_name:{4}".format(
                credential_event.ip_src,
                credential_event.username,
                credential_event.password,
                credential_event.module_name,
                credential_event.machine_name
            )
        )
    return elasticsearch_events.index(index='credential_events', body=credential_event.__dict__)


def insert_to_file_change_events_collection(file_change_event_data: FileEventsData):
    """
    insert file change events which are obtained from ftp/ssh weak_password
    module

    Args:
        file_change_event_data: Object of FileEventsData Class with file change
                                parameters

    Returns:
        inserted_id
    """
    file_change_event_data.machine_name = network_config["real_machine_identifier_name"]
    file_change_event_data.file_content = binascii.b2a_base64(open(
        file_change_event_data.file_path,
        'rb'
    ).read()).decode() if not file_change_event_data.is_directory and file_change_event_data.status != "deleted" else ""

    if is_verbose_mode():
        verbose_info(
            "Received honeypot file change event, file_path:{0}, status:{1}, "
            "module_name:{2}, module_name:{3}, machine_name:{3}".format(
                file_change_event_data.file_path,
                file_change_event_data.status,
                file_change_event_data.module_name,
                file_change_event_data.machine_name,
            )
        )
    return elasticsearch_events.index(index='file_change_events', body=file_change_event_data.__dict__)


def insert_to_events_data_collection(event_data: EventData):
    """
    Insert data collected from module processors of modules such as-
    ICS module

    Args:
        event_data: contain ip, module_name, machine_name, date, data

    Returns:
        inserted_id
    """
    event_data.machine_name = network_config["real_machine_identifier_name"]

    event_data.country_ip_src = byte_to_str(
        IP2Location.get_country_short(
            event_data.ip_src
        )
    )

    if is_verbose_mode():
        verbose_info(
            "Received honeypot data event, ip_dest:{0}, module_name:{1}, "
            "machine_name:{2}, data:{3}".format(
                event_data.ip_src,
                event_data.module_name,
                event_data.machine_name,
                event_data.data
            )
        )

    return elasticsearch_events.index(index='data_events', body=event_data.__dict__)


def insert_pcap_files_to_collection(file_archive: FileArchive):
    """
    Insert the pcap files containing the captured network traffic to
    mongodb collection

    Args:
        file_archive: path of the file

    Returns:
        file_id
    """
    if is_verbose_mode():
        verbose_info(
            "Received network traffic file:{0}, date:{1}. "
            "Inserting it in the File Archive".format(
                file_archive.file_path,
                file_archive.date
            )
        )
    file_content = binascii.b2a_base64(open(file_archive.file_path, "rb").read()).decode()
    file_md5 = hashlib.md5(file_content.encode()).hexdigest()
    return elasticsearch_events.index(
        index='ohp_file_archive',
        body={
            "md5": file_md5,
            "content": file_content,
            "filename": os.path.split(file_archive.file_path)[1],
            "machine_name": network_configuration()["real_machine_identifier_name"],
            "date": file_archive.date,
            "splitTimeout": file_archive.split_timeout
        }
    )
