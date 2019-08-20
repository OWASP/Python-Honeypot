#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import json
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

EXCLUDES = ['/dev']
LOGFILE='tmp/ohp_ftp_weak_password_logs.txt'

class Watcher:

    def __init__(self):
        self.observer = Observer()
        self.stop_execution=False
        self.DIRECTORY_TO_WATCH = os.getcwd() + "/tmp/ohp_ftp_weak_container/"

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while not self.stop_execution:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")
        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if not (event.event_type == 'modified' and event.is_directory) and '/' + event.src_path.rsplit('/')[1] not in EXCLUDES:
            logfile_handle = open(LOGFILE, "a")
            print(event.event_type,event.src_path)
            logfile_handle.write(json.dumps({'status' : event.event_type,
                        'path': event.src_path,
                        'module_name' : 'ftp/weak_password',
                        'date' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                                 +'\n')
            logfile_handle.close()

class ModuleProcessor:
    """
    this is the processor to run after docker machine is up to grab the log files or do other needed process...
    """
    def __init__(self):
        self.kill_flag = False
        self.log_filename='tmp/ohp_ftp_weak_password_logs.txt'
        self.watcher = Watcher()

    def processor(self):
        """
        processor function will be called as a new thread and will be die when kill_flag is True
        :return:
        """
        if os.path.exists(self.log_filename):
            os.remove(self.log_filename)  # remove if exist from past
        while not self.kill_flag:
            #self.watcher.run() # when this is done it transfers the control to run and never returns back
            # maybe one solution would be to run this in a different thread
            time.sleep(0.1)


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
