import time
from multiprocessing import Process, Queue

class ProcessPool(object):
    
    def __init__(self, func, process_count=5):
        self.func = func
        self.process_count = process_count
        self.queue = Queue()
        self._create_processes()
    
    def _create_processes(self):
        for i in range(0, self.process_count):
            process = Process(target=self.func, args=[self.queue])
            process.daemon = True
            process.start()
