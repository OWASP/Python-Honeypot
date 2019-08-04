#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from core.compatible import generate_token
import os
import json
from database.connector import insert_honeypot_events_from_module_processor,\
    insert_honeypot_events_data_from_module_processor

class ModuleProcessor:
    """
    this is the processor to run after docker machine is up to grab the log files or do other needed process...
    """
    def __init__(self):
        self.kill_flag = False
        self.log_creds_filename = 'tmp/ohp_http_strong_password_creds_logs.log'
        self.log_access_filename = 'tmp/ohp_http_strong_password_access_logs.log'
        self.log_filename_creds_dump = 'tmp/ohp_http_strong_password_creds_logs.json'
        self.log_filename_access_dump = 'tmp/ohp_http_strong_password_access_logs.json'

    def processor(self):
        """
        processor function will be called as a new thread and will be die when kill_flag is True
        :return:
        """
        if os.path.exists(self.log_creds_filename):
            os.remove(self.log_creds_filename)  # remove if exist from past
        if os.path.exists(self.log_access_filename):
            os.remove(self.log_access_filename)  # remove if exist from past
        while not self.kill_flag:
            if os.path.exists(self.log_creds_filename):
                os.rename(self.log_creds_filename, self.log_filename_creds_dump)
                data_dump = open(self.log_filename_creds_dump).readlines()
                for data in data_dump:
                    data = json.loads(data)
                    insert_honeypot_events_from_module_processor(
                        data['IP'],
                        data['username'],
                        data['password'],
                        data['module_name'],
                        data['date'],
                    )
                os.remove(self.log_filename_creds_dump)

            if os.path.exists(self.log_access_filename):
                os.rename(self.log_access_filename, self.log_filename_access_dump)
                data_dump = open(self.log_filename_access_dump).readlines()
                for data in data_dump:
                    data = json.loads(data)
                    insert_honeypot_events_data_from_module_processor(
                        data['IP'],
                        data['module_name'],
                        data['date'],
                        data['DATA']
                    )
                os.remove(self.log_filename_access_dump)
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
        "extra_docker_options": ["--volume {0}/tmp:/root/logs/".format(os.getcwd())],
        "module_processor": ModuleProcessor()
    }
