#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
import os
import inspect
import time

from core.time_helper import now
from config import api_configuration
from config import network_configuration
from lib.ip2location import IP2Location

client = pymongo.MongoClient(
    api_configuration()["api_database"],
    serverSelectionTimeoutMS=api_configuration()["api_database_connection_timeout"]
)
database = client[api_configuration()["api_database_name"]]
honeypot_events = database.honeypot_events
network_events = database.network_events
global honeypot_events_queue, network_events_queue
honeypot_events_queue = []
network_events_queue = []
credential_events = database.credential_events
honeypot_events_data = database.honeypot_events_data
IP2Location = IP2Location.IP2Location(
    os.path.join(
        os.path.dirname(
            inspect.getfile(IP2Location)
        ),
        "IP2LOCATION-LITE-DB1.BIN")
)


# todo: write documentation about machine_name

def insert_selected_modules_network_event(ip, port, module_name, machine_name):
    """
    insert selected modules event to honeypot_events collection

    Args:
        ip: connected ip
        port: connected port
        module_name: module name ran on the port
        machine_name: real machine name

    Returns:
        ObjectId(inserted_id)
    """
    global honeypot_events_queue
    honeypot_events_queue.append(
        {
            "ip": ip,
            "port": int(port),
            "module_name": module_name,
            "date": now(),
            "machine_name": machine_name,
            "event_type": "honeypot_event",
            "country": str(IP2Location.get_country_short(ip).decode())
        }
    )
    return


def insert_other_network_event(ip, port, machine_name):
    """
    insert other network events (port scan, etc..) to network_events collection

    Args:
        ip: connected ip
        port: connected port
        machine_name: real machine name

    Returns:
        ObjectId(inserted_id)
    """
    global network_events_queue
    network_events_queue.append(
        {
            "ip": ip,
            "port": int(port),
            "date": now(),
            "machine_name": machine_name,
            "country": str(IP2Location.get_country_short(ip).decode())
        }
    )
    return


def insert_events_in_bulk():
    """
    inserts all honeypot and network events in bulk to honeypot_events and network_events collection respectively
    """
    global honeypot_events_queue
    global network_events_queue
    if honeypot_events_queue:
        new_events = honeypot_events_queue[:]
        honeypot_events_queue = []
        honeypot_events.insert_many(new_events)
    if network_events_queue:
        new_events = network_events_queue[:]
        network_events_queue = []
        network_events.insert_many(new_events)
    return


def insert_bulk_events_from_thread():
    """
    Thread function for inserting bulk events in a thread
    :return: True/None
    """
    while True:
        insert_events_in_bulk()
        time.sleep(3)
    return True


def insert_honeypot_events_from_module_processor(ip, username, password, module_name, date):
    """
    insert honeypot events which are obtained from the modules
    args:
    ip : client ip used for connecting to the module
    username : username tried for connecting to modules
    password : password tried for connecting to modules
    module_name : on which module client accessed
    date : datetime of the event
    """
    return credential_events.insert_one(
        {
            "ip": ip,
            "module_name": module_name,
            "date": date,
            "username": username,
            "password": password,
            "country": str(IP2Location.get_country_short(ip).decode()),
            "machine_name": network_configuration()["real_machine_identifier_name"]
        }
    ).inserted_id


def insert_honeypot_events_data_from_module_processor(ip,module_name,date,data):
    """
    insert data which is recieved from honeypot modules
    args:
    ip : client ip used for putting the data
    module_name : on which module client accessed
    date : datetime of the events
    data : Data which is obtained from the client
    """
    return honeypot_events_data.insert_one(
        {
            "ip": ip,
            "module_name": module_name,
            "date": date,
            "data" : data,
            "country": str(IP2Location.get_country_short(ip).decode()),
            "machine_name": network_configuration()["real_machine_identifier_name"]
        }
    ).inserted_id
