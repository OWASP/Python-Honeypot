#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import threading
from core.exit_helper import terminate_thread
from core.file_monitor import FileMonitor


class ModuleProcessor:
    """
    this is the processor to run after docker machine is up to grab the log
    files or do other needed process...
    """

    def __init__(self):
        self.kill_flag = False
        self.log_filename = 'tmp/ohp_ftp_weak_password_logs.txt'
        self.log_filename_dump = 'tmp/ohp_ftp_weak_password_files_logs.json'
        self.stop_execution = False
        self.DIRECTORY_TO_WATCH = os.getcwd() + "/tmp/ohp_ftp_weak_container/"
        self.EXCLUDES = ['/dev']
        self.module_name = "ftp/weak_password"
        if not os.path.exists(self.DIRECTORY_TO_WATCH):
            os.makedirs(self.DIRECTORY_TO_WATCH)

    def processor(self):
        """
        processor function will be called as a new thread and will be die when
        kill_flag is True
        :return:
        """
        new_file_handler = FileMonitor()
        new_file_handler.log_filename = self.log_filename
        new_file_handler.log_filename_dump = self.log_filename_dump
        new_file_handler.DIRECTORY_TO_WATCH = self.DIRECTORY_TO_WATCH
        new_file_handler.EXCLUDES = self.EXCLUDES
        new_file_handler.module_name = self.module_name
        thread = threading.Thread(target=new_file_handler.run, args=(), name="ftp_weak_password_processor")
        if os.path.exists(self.log_filename):
            os.remove(self.log_filename)  # remove if exist from past
        thread.start()  # Start the execution
        while not self.kill_flag:
            try:
                time.sleep(0.1)
            except Exception:
                pass
        new_file_handler.stop()
        terminate_thread(thread)


def module_configuration():
    """
    module configuration

    Returns:
        JSON/Dict module configuration
    """
    return {
        "username": "admin",
        "password": "admin",
        "extra_docker_options": ["--volume {0}/tmp/ohp_ftp_weak_container/:/root:z".format(os.getcwd())],
        "module_processor": ModuleProcessor()
    }
