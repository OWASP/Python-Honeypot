#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from database.connector import insert_file_change_events


class containerFilesHandler(FileSystemEventHandler):
    def __init__(self):
        self.log_filename = None
        self.EXCLUDES = None
        self.module_name = None

    @staticmethod
    def on_any_event(event):
        if not (event.event_type == 'modified' and event.is_directory):
            print(event)


class fileMonitor:
    def __init__(self):
        self.observer = Observer()
        self.log_filename = None
        self.log_filename_dump = None
        self.stop_execution = False
        self.DIRECTORY_TO_WATCH = None
        self.EXCLUDES = []
        self.module_name = None

    def stop(self):
        self.self_execution = True
        self.observer.stop()

    def run(self):
        event_handler = containerFilesHandler()
        event_handler.log_filename = self.log_filename
        event_handler.EXCLUDES = self.EXCLUDES
        event_handler.module_name = self.module_name

        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        while not self.stop_execution:
            try:
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
            except Exception as _:
                del _
            time.sleep(0.3)
