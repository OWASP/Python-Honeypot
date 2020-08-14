#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import oschmod
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from database.connector import insert_to_file_change_events_collection
from database.datatypes import FileEventsData
from core.compatible import byte_to_str
from core.time_helper import now


def is_excluded(path, dirs):
    """
    if path is excluded in list of dirs/files

    :param path: path to check for exclude
    :param dirs: list of excludes
    :return: Boolean
    """
    for directory in dirs:
        if path.startswith(directory):
            return True
    return False


class ContainerFilesHandler(FileSystemEventHandler):
    def __init__(self):
        self.log_filename = None
        self.EXCLUDES = None
        self.module_name = None

    def on_any_event(self, event):
        if not (event.event_type == 'modified' and event.is_directory) \
                and not is_excluded(event.src_path, self.EXCLUDES):
            insert_to_file_change_events_collection(
                FileEventsData(
                    file_path=byte_to_str(event.src_path),
                    status=byte_to_str(event.event_type),
                    module_name=self.module_name,
                    date=now(),
                    is_directory=event.is_directory
                )
            )


class FileMonitor:
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
        event_handler = ContainerFilesHandler()
        event_handler.log_filename = self.log_filename
        event_handler.EXCLUDES = self.EXCLUDES
        event_handler.module_name = self.module_name

        # set 777 permission and allow container read/write/execute
        oschmod.set_mode(self.DIRECTORY_TO_WATCH, '777')

        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        while not self.stop_execution:
            try:
                time.sleep(0.1)
            except Exception:
                pass
