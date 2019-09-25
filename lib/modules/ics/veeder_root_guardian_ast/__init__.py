#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time


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
        "virtual_machine_port_number": 10001,
        "real_machine_port_number": 10001,
        "company_name_address": "3356234 SL OIL 433234\r\n9346 GLODEN AVE.\r\nQUEEN SPRING, MD\r\n",
         "extra_docker_options": [],
        "module_processor": ModuleProcessor()
    }
