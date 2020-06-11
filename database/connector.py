#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect
import os
import time

import pymongo

from config import api_configuration, network_configuration
from core.alert import verbose_info
from core.compatible import byte_to_str, is_verbose_mode
from core.time_helper import now
from database.datatypes import (CredentialEvent, HoneypotEvent,
                                ICSHoneypotEvent, NetworkEvent)
from lib.ip2location import IP2Location

api_config = api_configuration()
network_config = network_configuration()

# MongoDB Client
client = pymongo.MongoClient(
    api_config["api_database"],
    serverSelectionTimeoutMS=
                api_config["api_database_connection_timeout"]
)
database = client[api_config["api_database_name"]]

# Event Collections connections
credential_events = database.credential_events
honeypot_events = database.honeypot_events
network_events = database.network_events
ics_honeypot_events = database.ics_honeypot_events

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

def insert_to_honeypot_events_queue(honeypot_event: HoneypotEvent):
    """
    insert selected modules event to honeypot_events collection

    Args:
        honeypot_event: Object of HoneypotEvent class with event parameters

    Returns:
        ObjectId(inserted_id)
    """
    if is_verbose_mode():
        verbose_info(
            "Received honeypot event, ip_dest:{0}, port_dest:{1}, "
            "ip_src:{2}, port_src:{3}, module_name:{4}, machine_name:{5}"
            .format(
                honeypot_event["ip_dest"],
                honeypot_event["port_dest"],
                honeypot_event["ip_src"],
                honeypot_event["port_src"],
                honeypot_event["module_name"],
                honeypot_event["machine_name"]
            )
        )

    # Get country of the source IP Address    
    honeypot_event["country_ip_src"] = \
            byte_to_str(
                IP2Location.get_country_short(
                    honeypot_event["ip_src"]    
                ))
    
    # Get country of the destination IP Address
    honeypot_event["country_ip_dest"] = \
            byte_to_str(
                IP2Location.get_country_short(
                    honeypot_event["ip_dest"]
                ))

    honeypot_events_queue.append(honeypot_event)

    return


def insert_to_network_events_queue(network_event: NetworkEvent):
    """
    insert other network events (port scan, etc..) to network_events
    collection

    Args:
        network_event: Object of NetworkEvent Class with event parameters

    Returns:
        ObjectId(inserted_id)
    """
    if is_verbose_mode():
        verbose_info(
            "Received network event, ip_dest:{0}, port_dest:{1}, "
            "ip_src:{2}, port_src:{3}, machine_name:{4}"
            .format(
                network_event["ip_dest"],
                network_event["port_dest"],
                network_event["ip_src"],
                network_event["port_src"],
                network_event["machine_name"]
            )
        )

    # Get country of the source IP Address 
    network_event["country_ip_src"] = \
            byte_to_str(
                IP2Location.get_country_short(
                    network_event["ip_src"]
                ))
    
    # Get country of the destination IP Address
    network_event["country_ip_dest"] = \
            byte_to_str(
                IP2Location.get_country_short(
                    network_event["ip_dest"]
                ))

    network_events_queue.append(network_event)

    return


def push_events_queues_to_database():
    """
    Pushes all honeypot and network events collected in the 
    honeypot_events_queue and network_events_queue to honeypot_events
    and network_events collection respectively
    """

    if is_verbose_mode() and (honeypot_events_queue or network_events_queue):
        verbose_info("Submitting new events to database")
    
    # Insert all honeypot events to database (honeypot_events collection)
    if honeypot_events_queue:
        new_events = honeypot_events_queue[:]
        honeypot_events_queue.clear()
        honeypot_events.insert_many(new_events)

    # Insert all network events to database (network_events collection)
    if network_events_queue:
        new_events = network_events_queue[:]
        network_events_queue.clear()
        network_events.insert_many(new_events)
    return


def push_events_to_database_from_thread():
    """
    Thread function for inserting bulk events in a thread

    Returns:
        True/None
    """
    while True:
        push_events_queues_to_database()
        time.sleep(3)
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
    credential_event["country"] = \
            byte_to_str(
                IP2Location.get_country_short(
                        credential_event["ip"]
                    ))
    
    credential_event["machine_name"] = \
                network_config["real_machine_identifier_name"]

    if is_verbose_mode():
        verbose_info(
            "Received honeypot credential event, ip_dest:{0}, username:{1}, "
            "password:{2}, module_name:{3}, machine_name:{4}"
            .format(
                credential_event["ip"],
                credential_event["username"],
                credential_event["password"],
                credential_event["module_name"],
                credential_event["machine_name"]
            )
        )
    
    return credential_events.insert_one(credential_event).inserted_id


def insert_to_ics_honeypot_events_collection(ics_honeypot_event: ICSHoneypotEvent):
    """
    Insert data received from the ICS module processor to the
    ics_honeypot_data collection

    Args:
        ip : client ip used for putting the data
        module_name : on which module client accessed
        date : datetime of the events
        data : Data which is obtained from the client

    Returns:
        inserted_id
    """
    ics_honeypot_event["machine_name"] = \
                network_config["real_machine_identifier_name"]

    ics_honeypot_event["country"] = \
            byte_to_str(
                IP2Location.get_country_short(
                    ics_honeypot_event["ip"]
                ))

    if is_verbose_mode():
        verbose_info(
            "Received honeypot data event, ip_dest:{0}, module_name:{1}, "
            "machine_name:{2}, data:{3}"
            .format(
                ics_honeypot_event["ip"], 
                ics_honeypot_event["module_name"],
                ics_honeypot_event["machine_name"],
                ics_honeypot_event["data"]
            )
        )

    return ics_honeypot_events.insert_one(ics_honeypot_event).inserted_id