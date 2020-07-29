#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is the new version of GasPot Developed by OWASP Honeypot Team
# more commands supported
# output text fixed

import socket
import select
import datetime
import time
import random
import json

# import all commands
from commands import *

# import configuration
from config import module_configuration

# bind socket use configuration
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setblocking(0)
server_socket.bind((
                "0.0.0.0",
                module_configuration()["virtual_machine_port_number"]))
server_socket.listen(10)

logs_filename = "/tmp/ics_veeder_root_guardian_ast.log"


def save_log(log_data):
    log_connections = open(logs_filename, "ab")
    log_connections.write(json.dumps(log_data) + "\n")
    log_connections.close()


# list of all commands
commands = {
    "I10100": I10100,
    "I10200": I10200,
    "I11100": I11100,
    "I11200": I11200,
    "I11300": I11300,
    "I11400": I11400,
    "I20100": I20100,
    "I20200": I20200,
    "I20300": I20300,
    "I20400": I20400,
    "I20500": I20500,
    "I20600": I20600,
    "I20700": I20700,
    "I20800": I20800,
    "I20900": I20900,
    "I20C00": I20C00,
    "I20D00": I20D00,
    "I25100": I25100,
    "I30100": I30100,
    "I30200": I30200,
    "I50100": I50100,
    "I50A00": I50A00,
    "I50B00": I50B00,
    "I50C00": I50C00,
    "I50E00": I50E00,
    "I50F00": I50F00,
    "I51400": I51400,
    "I51700": I51700,
    "I51A00": I51A00,
    "I51B00": I51B00,
    "I51C00": I51C00,
    "I51F00": I51F00,
    "I53100": I53100,
    "I60100": I60100,
    "I60200": I60200,
    "I60300": I60300,
    "I60400": I60400,
    "I60500": I60500,
    "I60600": I60600,
    "I60700": I60700,
    "I60800": I60800,
    "I60900": I60900,
    "I60A00": I60A00,
    "I60B00": I60B00,
    "I60C00": I60C00,
    "I61000": I61000,
    "I61100": I61100,
    "I61200": I61200,
    "I61300": I61300,
    "I61400": I61400,
    "I61500": I61500,
    "I61600": I61600,
    "I61700": I61700,
    "I61800": I61800,
    "I61900": I61900,
    "I61A00": I61A00,
    "I61B00": I61B00,
    "I61C00": I61C00,
    "I61D00": I61D00,
    "I62100": I62100,
    "I62200": I62200,
    "I62300": I62300,
    "I62400": I62400,
    "I62500": I62500,
    "I62600": I62600,
    "I62700": I62700,
    "I62800": I62800,
    "I62900": I62900,
    "I62A00": I62A00,
    "I62B00": I62B00,
    "I62D00": I62D00,
    "I62E00": I62E00,
    "I62F00": I62F00,
    "I63100": I63100,
    "I63200": I63200,
    "I63300": I63300,
    "I63400": I63400,
    "I63500": I63500,
    "I63600": I63600,
    "I77100": I77100,
    "I85100": I85100,
    "I62C00": I62C00,
    "I85200": I85200,
    "I85300": I85300,
    "I88100": I88100,
    "I88200": I88200,
    "I90100": I90100,
    "I90200": I90200,
    "I90300": I90300,
    "I90400": I90400,
    "I90500": I90500,
    "IA0100": IA0100,
    "IA0200": IA0200,
    "IA0300": IA0300,
    "IA0400": IA0400,
    "IA0500": IA0500,
    "IA0600": IA0600,
    "IA0700": IA0700,
    "IA1000": IA1000,
    "IA1100": IA1100,
    "IA1200": IA1200,
    "IA1300": IA1300,
    "IA1400": IA1400,
    "IA1500": IA1500,
    "IA2000": IA2000,
    "IA2100": IA2100,
    "IA2200": IA2200,
    "IA5100": IA5100,
    "IA5200": IA5200,
    "IA5300": IA5300,
    "IA5400": IA5400,
    "IA5500": IA5500,
    "IA9100": IA9100,
    "S00100": S00100,
    "S00200": S00200,
    "S00300": S00300,
    "S01000": S01000,
    "S05100": S05100,
    "S05200": S05200,
    "S05300": S05300

}

# while True, keep accepting connections
while True:
    active_sockets = [server_socket]
    while True:
        readable, writeable, errored = select.select(active_sockets, [], [], 5)
        for conn in readable:
            if conn is server_socket:
                new_con, addr = server_socket.accept()
                log_data = {
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "ip": addr[0],
                    "module_name": "ics/veeder_root_guardian_ast",
                    "content": "",
                    "valid_command": False
                }
                new_con.settimeout(30.0)
                active_sockets.append(new_con)
            else:
                addr = conn.getpeername()
                print(addr[0], "connected")
                try:
                    TIME = datetime.datetime.utcnow()
                    response = conn.recv(4096)
                    if not response:
                        active_sockets.remove(conn)
                        conn.close()
                        continue
                    while not ("\n" in response or "00" in response):
                        response += conn.recv(4096)
                    if response[0] != "\x01":
                        conn.close()
                        active_sockets.remove(conn)
                        log_data["content"] = response
                        save_log(log_data)
                        continue
                    if len(response) < 6:
                        conn.close()
                        active_sockets.remove(conn)
                        log_data["content"] = response
                        save_log(log_data)
                        continue
                    cmd = response[1:7]
                    if cmd in commands:
                        log_data["valid_command"] = True
                        for data in commands[cmd]().rsplit("\r\n"):
                            data += "\r\n"
                            conn.send(data)
                            time.sleep(random.choice(([0.01] * 10) + ([0.1] * 10) + ([1] * 3)))
                        print(addr[0], cmd, "responded")
                    log_data["content"] = response
                    save_log(log_data)
                except Exception as e:
                    print("Unknown Error: {}".format(str(e)))
                    try:
                        log_data["content"] = response
                    except:
                        pass
                    save_log(log_data)
                    raise
                except KeyboardInterrupt:
                    try:
                        log_data["content"] = response
                    except:
                        pass
                    save_log(log_data)
                    conn.close()
                except select.error:
                    try:
                        log_data["content"] = response
                    except:
                        pass
                    save_log(log_data)
                    conn.close()
