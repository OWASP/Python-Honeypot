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

    def processor(self):
        """
        processor function will be called as a new thread and will be die when kill_flag is True
        :return:
        """
        while not self.kill_flag:
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
