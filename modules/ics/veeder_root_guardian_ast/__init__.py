#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import json
import binascii

from database.connector import insert_to_events_data_collection
from database.datatypes import EventData

LOGFILE = 'tmp/ics_veeder_root_guardian_ast.log'


class ModuleProcessor:
    """
    this is the processor to run after docker machine is up to grab the
    log files or do other needed process...
    """

    def __init__(self):
        self.kill_flag = False

    def processor(self):
        """
        processor function will be called as a new thread and will
        be die when kill_flag is True
        """
        while not self.kill_flag:
            if os.path.exists(LOGFILE) and os.path.getsize(LOGFILE) > 0:

                data_dump = open(LOGFILE).readlines()
                open(LOGFILE, 'w').write('')
                for data in data_dump:
                    data_json = json.loads(data)
                    ip = data_json["ip"]
                    time_of_insertion = data_json["date"]
                    recorded_data = {
                        "content": data_json["content"],
                        "valid_command": data_json["valid_command"]
                    }
                    insert_to_events_data_collection(
                        EventData(
                            ip=ip,
                            module_name="ics/veeder_root_guardian_ast",
                            date=time_of_insertion,
                            data=recorded_data
                        )
                    )
            time.sleep(0.1)


def module_configuration():
    """
    module configuration

    Returns:
        JSON/Dict module configuration
    """
    return {
        "virtual_machine_port_number": 10001,
        "real_machine_port_number": 10001,
        "company_name_address": binascii.b2a_base64(
            str(
                "3356234 SL OIL 433234\r\n9346 GLODEN AVE."
                "\r\nQUEEN SPRING, MD\r\n"
            ).encode()
        ).strip().decode(),
        "extra_docker_options": ["--volume {0}/tmp:/tmp/".format(os.getcwd())],
        "module_processor": ModuleProcessor()
    }
