#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import json
from core.compatible import generate_token
from database.connector import insert_honeypot_events_from_module_processor
from config import network_configuration


class ModuleProcessor:
    """
    this is the processor to run after docker machine is up to grab the log files or do other needed process...
    """

    def __init__(self):
        self.kill_flag = False
        self.log_filename = 'tmp/ohp_ssh_strong_password_creds_logs.txt'
        self.log_filename_dump = 'tmp/ohp_ssh_strong_password_creds_logs.json'

    def processor(self):
        """
        processor function will be called as a new thread and will be die when kill_flag is True
        :return:
        """
        if os.path.exists(self.log_filename):
            os.remove(self.log_filename)  # remove if exist from past
        while not self.kill_flag:
            if os.path.exists(self.log_filename):
                os.rename(self.log_filename, self.log_filename_dump)
                data_dump = open(self.log_filename_dump).readlines()
                for data in data_dump:
                    data = json.loads(data)
                    insert_honeypot_events_from_module_processor(
                        data['ip'],
                        data['username'],
                        data['password'],
                        data['module_name'],
                        data['date']
                    )
                os.remove(self.log_filename_dump)
            time.sleep(0.1)


def module_configuration():
    """
    module configuration

    Returns:
        JSON/Dict module configuration
    """
    return {
        "username": "root",
        "password": generate_token(16),
        "extra_docker_options": ["--volume {0}/tmp:/root/logs/".format(os.getcwd())],
        "module_processor": ModuleProcessor()
    }
