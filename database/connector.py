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
from core.compatible import byte_to_str
from core.alert import verbose_info
from core.compatible import is_verbose_mode

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

def insert_selected_modules_network_event(ip_dest, port_dest, ip_src, port_src, module_name, machine_name):
    """
    insert selected modules event to honeypot_events collection

    Args:
        ip_dest: dest ip (machine)
        port_dest: dest port (machine)
        ip_src: src ip
        port_src: src port
        module_name: module name ran on the port
        machine_name: real machine name

    Returns:
        ObjectId(inserted_id)
    """
    if is_verbose_mode():
        verbose_info(
            "Received honeypot event, ip_dest:{0}, port_dest:{1}, "
            "ip_src:{2}, port_src:{3}, module_name:{4}, machine_name:{5}".format(
                ip_dest, port_dest, ip_src, port_src, module_name, machine_name
            )
        )

    global honeypot_events_queue
    honeypot_events_queue.append(
        {
            "ip_dest": byte_to_str(ip_dest),
            "port_dest": int(port_dest),
            "ip_src": byte_to_str(ip_src),
            "port_src": int(port_src),
            "module_name": module_name,
            "date": now(),
            "machine_name": machine_name,
            "event_type": "honeypot_event",
            "country_ip_src": byte_to_str(IP2Location.get_country_short(byte_to_str(ip_src))),
            "country_ip_dest": byte_to_str(IP2Location.get_country_short(byte_to_str(ip_dest)))
        }
    )
    return


def insert_other_network_event(ip_dest, port_dest, ip_src, port_src, machine_name):
    """
    insert other network events (port scan, etc..) to network_events collection

    Args:
        ip_dest: dest ip (machine)
        port_dest: dest port (machine)
        ip_src: src ip
        port_src: src port
        machine_name: real machine name

    Returns:
        ObjectId(inserted_id)
    """
    if is_verbose_mode():
        verbose_info(
            "Received network event, ip_dest:{0}, port_dest:{1}, "
            "ip_src:{2}, port_src:{3}, machine_name:{4}".format(
                ip_dest, port_dest, ip_src, port_src, machine_name
            )
        )
    global network_events_queue
    network_events_queue.append(
        {
            "ip_dest": byte_to_str(ip_dest),
            "port_dest": int(port_dest),
            "ip_src": byte_to_str(ip_src),
            "port_src": int(port_src),
            "date": now(),
            "machine_name": machine_name,
            "country_ip_src": byte_to_str(IP2Location.get_country_short(byte_to_str(ip_src))),
            "country_ip_dest": byte_to_str(IP2Location.get_country_short(byte_to_str(ip_dest)))
        }
    )
    return


def insert_events_in_bulk():
    """
    inserts all honeypot and network events in bulk to honeypot_events and network_events collection respectively
    """
    global honeypot_events_queue
    global network_events_queue
    if is_verbose_mode() and (honeypot_events_queue or network_events_queue):
        verbose_info("Submitting new events to database")
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


def insert_honeypot_events_credential_from_module_processor(ip, username, password, module_name, date):
    """
    insert honeypot events which are obtained from the modules
    args:
    ip : client ip used for connecting to the module
    username : username tried for connecting to modules
    password : password tried for connecting to modules
    module_name : on which module client accessed
    date : datetime of the event

    :return: inserted_id
    """
    if is_verbose_mode():
        verbose_info(
            "Received honeypot credential event, ip_dest:{0}, username:{1}, "
            "password:{2}, module_name:{3}, machine_name:{4}".format(
                ip, username, password, module_name, network_configuration()["real_machine_identifier_name"]
            )
        )
    return credential_events.insert_one(
        {
            "ip_dest": byte_to_str(ip),
            "module_name": module_name,
            "date": date,
            "username": username,
            "password": password,
            "country": byte_to_str(IP2Location.get_country_short(byte_to_str(ip))),
            "machine_name": network_configuration()["real_machine_identifier_name"]
        }
    ).inserted_id


def insert_honeypot_events_data_from_module_processor(ip, module_name, date, data):
    """
    insert data which is received from honeypot modules
    args:
    ip : client ip used for putting the data
    module_name : on which module client accessed
    date : datetime of the events
    data : Data which is obtained from the client

    :return: inserted_id
    """
    if is_verbose_mode():
        verbose_info(
            "Received honeypot data event, ip_dest:{0}, module_name:{1}, "
            "machine_name:{2}, data:{3}".format(
                ip, module_name, network_configuration()["real_machine_identifier_name"], data
            )
        )
    return honeypot_events_data.insert_one(
        {
            "ip_dest": byte_to_str(ip),
            "module_name": module_name,
            "date": date,
            "data": data,
            "country": byte_to_str(IP2Location.get_country_short(byte_to_str(ip))),
            "machine_name": network_configuration()["real_machine_identifier_name"]
        }
    ).inserted_id
