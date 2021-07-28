#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from core.compatible import generate_token
import os
import binascii
import json
from database.connector import insert_to_credential_events_collection
from database.datatypes import CredentialEvent

LOGFILE = 'tmp/access.log'
LOGFILE_DUMP = 'tmp/ohp_http_strong_password_creds_logs.json'


class ModuleProcessor:
    """
    this is the processor to run after docker machine is up to grab the
    log files or do other needed process...
    """

    def __init__(self):
        self.kill_flag = False

    def processor(self):
        """
        processor function will be called as a new thread and will be
        die when kill_flag is True
        """
        while not self.kill_flag:
            if os.path.exists(LOGFILE) and os.path.getsize(LOGFILE) > 0:

                # os.rename(self.log_filename, self.log_filename_dump)
                data_dump = open(LOGFILE).readlines()
                open(LOGFILE, 'w').write('')
                # data_dump = open(self.log_filename_dump).readlines()
                for data in data_dump:
                    data_json = json.loads(data)
                    ip = data_json["ip"]
                    time_of_insertion = data_json["time"]
                    if data_json["authorization"] != "-":
                        authorization = \
                            data_json["authorization"].split(' ')[1]
                        # binascii is returning bytes
                        authorization = binascii.a2b_base64(authorization).decode('utf-8')
                        username = authorization.split(":")[0]
                        password = ":".join(authorization.split(":")[1:])
                        insert_to_credential_events_collection(
                            CredentialEvent(
                                ip_src=ip,
                                username=username,
                                password=password,
                                module_name="http/basic_auth_strong_password",
                                date=time_of_insertion
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
        "username": "admin",
        "password": generate_token(16),
        "extra_docker_options":
            ["--volume {0}/tmp:/var/log/apache2/".format(os.getcwd())],
        "module_processor": ModuleProcessor()
    }
