#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import json
import datetime
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core._die import terminate_thread
from database.connector import insert_file_change_events

EXCLUDES = ['/dev']
LOGFILE = 'tmp/ohp_ftp_weak_password_logs.txt'


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if not (event.event_type == 'modified' and event.is_directory) and \
                '/' + event.src_path.rsplit('/')[1] not in EXCLUDES:
            logfile_handle = open(LOGFILE, "a")
            logfile_handle.write(
                json.dumps(
                    {
                        'status': event.event_type,
                        'path': event.src_path,
                        'module_name': 'ftp/weak_password',
                        'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                )
                + '\n')
            logfile_handle.close()


class ModuleProcessor:
    """
    this is the processor to run after docker machine is up to grab the log files or do other needed process...
    """

    def __init__(self):
        self.kill_flag = False
        self.log_filename = 'tmp/ohp_ftp_weak_password_logs.txt'
        self.log_filename_dump = 'tmp/ohp_ftp_weak_password_files_logs.json'
        self.observer = Observer()
        self.stop_execution = False
        self.DIRECTORY_TO_WATCH = os.getcwd() + "/tmp/ohp_ftp_weak_container/"

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while not self.stop_execution:
                time.sleep(1)
        except Exception as _:
            self.observer.stop()
        self.observer.join()

    def stop(self):
        self.self_execution = True
        self.observer.stop()

    def processor(self):
        """
        processor function will be called as a new thread and will be die when kill_flag is True
        :return:
        """
        thread = threading.Thread(target=self.run, args=())
        thread.start()  # Start the execution
        if os.path.exists(self.log_filename):
            os.remove(self.log_filename)  # remove if exist from past
        while not self.kill_flag:
            if os.path.exists(self.log_filename):
                os.rename(self.log_filename, self.log_filename_dump)
                data_dump = open(self.log_filename_dump).readlines()
                for data in data_dump:
                    data = json.loads(data)
                    insert_file_change_events(
                        data['path'],
                        data['status'],
                        data['module_name'],
                        data['date']
                    )
                os.remove(self.log_filename_dump)
            time.sleep(0.1)
        self.stop()
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
        "extra_docker_options": ["--volume {0}/tmp/ohp_ftp_weak_container/:/root".format(os.getcwd())],
        "module_processor": ModuleProcessor()
    }
