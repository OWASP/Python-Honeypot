#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from core.compatible import generate_token
import os
import json
from database.connector import insert_to_credential_events_collection
from database.datatypes import CredentialEvent

LOGFILE = 'tmp/ohp_ftp_strong_password_creds_logs.txt'
LOGFILE_DUMP = 'tmp/ohp_ftp_strong_password_creds_logs.json'


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
        if os.path.exists(LOGFILE):
            os.remove(LOGFILE)  # remove if exist from past
        while not self.kill_flag:
            if os.path.exists(LOGFILE):
                os.rename(LOGFILE, LOGFILE_DUMP)
                data_dump = open(LOGFILE_DUMP).readlines()
                for data in data_dump:
                    data = json.loads(data)
                    insert_to_credential_events_collection(
                        CredentialEvent(
                            ip_src=data['ip'],
                            username=data['username'],
                            password=data['password'],
                            module_name=data['module_name'],
                            date=data['date']
                        )
                    )
                os.remove(LOGFILE_DUMP)
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
            ["--volume {0}/tmp:/root/logs/".format(os.getcwd())],
        "module_processor": ModuleProcessor()
    }
