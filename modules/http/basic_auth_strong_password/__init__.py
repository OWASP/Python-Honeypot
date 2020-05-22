#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from core.compatible import generate_token
import os
import binascii
import json
from database.connector import insert_honeypot_events_credential_from_module_processor


class ModuleProcessor:
    """
    this is the processor to run after docker machine is up to grab the log files or do other needed process...
    """

    def __init__(self):
        self.log_filename = 'tmp/access.log'
        self.log_filename_dump = 'tmp/ohp_http_strong_password_creds_logs.json'
        self.kill_flag = False

    def processor(self):
        """
        processor function will be called as a new thread and will be die when kill_flag is True
        :return:
        """
        while not self.kill_flag:
            if os.path.exists(self.log_filename) and os.path.getsize(self.log_filename) > 0:
                # os.rename(self.log_filename, self.log_filename_dump)
                data_dump = open(self.log_filename).readlines()
                open(self.log_filename, 'w').write('')
                # data_dump = open(self.log_filename_dump).readlines()
                for data in data_dump:
                    data_json = json.loads(data)
                    ip = data_json["ip"]
                    time_of_insertion = data_json["time"]
                    if data_json["authorization"] != "-":
                        authorization = data_json["authorization"].split(' ')[1]
                        authorization = binascii.a2b_base64(
                            authorization
                        ).decode('utf-8')  # binascii is returning bytes
                        username = authorization.split(":")[0]
                        password = ":".join(authorization.split(":")[1:])
                        insert_honeypot_events_credential_from_module_processor(
                            ip,
                            username,
                            password,
                            "http/basic_auth_strong_password",
                            time_of_insertion
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
        "extra_docker_options": [],
        "extra_docker_options": ["--volume {0}/tmp:/var/log/apache2/".format(os.getcwd())],
        "module_processor": ModuleProcessor()
    }
