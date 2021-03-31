import logging, sys
from logging.handlers import RotatingFileHandler
from logging import StreamHandler

LOG_NAME = 'ohp_smtp_honeypot'

class Log:

    def __init__(self, log_name):
        self.log_name = log_name
        self.logger = logging.getLogger( self.log_name )
        self._remove_handlers()
        self._add_handler()
        self.logger.setLevel(logging.DEBUG)

    def _remove_handlers(self):
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)

    def _add_handler(self):
        try:
            handler = RotatingFileHandler(
                '/var/log/%s.log' % self.log_name,
                maxBytes=10485760,
                backupCount=3
            )
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        except IOError:
            self.logger.addHandler(StreamHandler(sys.stderr))

Log(LOG_NAME)
