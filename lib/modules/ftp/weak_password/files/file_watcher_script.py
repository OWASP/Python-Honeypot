#!/usr/bin/env python3

import json
import time
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

EXCLUDES = ['/dev']
LOGFILE = '/root/logs/ohp_ftp_weak_password_logs.txt'


class Watcher:

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except Exception as _:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if not (event.event_type == 'modified' and event.is_directory) \
                and '/' + event.src_path.rsplit('/')[1] not in EXCLUDES:
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


if __name__ == '__main__':
    w = Watcher()
    w.run()
