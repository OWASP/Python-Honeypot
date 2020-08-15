import secure_smtpd
import ssl, smtpd, asyncore, socket, logging, signal, time, sys

from .smtp_channel import SMTPChannel
from asyncore import ExitNow
from .process_pool import ProcessPool
from ssl import SSLError
try:
    from Queue import Empty
except ImportError:
    # We're on python3
    from queue import Empty

class SMTPServer(smtpd.SMTPServer):

    def __init__(self, localaddr, remoteaddr, ssl=False, certfile=None,\
                 keyfile=None, ssl_version=ssl.PROTOCOL_SSLv23, \
                 require_authentication=False, credential_validator=None,\
                 maximum_execution_time=30, process_count=5):
        smtpd.SMTPServer.__init__(self, localaddr, remoteaddr)
        self.logger = logging.getLogger(secure_smtpd.LOG_NAME)
        self.certfile = certfile
        self.keyfile = keyfile
        self.ssl_version = ssl_version
        self.subprocesses = []
        self.require_authentication = require_authentication
        self.credential_validator = credential_validator
        self.ssl = ssl
        self.maximum_execution_time = maximum_execution_time
        self.process_count = process_count
        self.process_pool = None

    def handle_accept(self):
        self.process_pool = ProcessPool(self._accept_subprocess,\
                                        process_count=self.process_count)
        self.close()

    def _accept_subprocess(self, queue):
        while True:
            try:
                newsocket = None
                self.socket.setblocking(1)
                pair = self.accept()
                map = {}

                if pair is not None:

                    self.logger.info('_accept_subprocess(): smtp connection'+
                                     'accepted within subprocess.')

                    newsocket, fromaddr = pair
                    newsocket.settimeout(self.maximum_execution_time)

                    if self.ssl:
                        newsocket = ssl.wrap_socket(
                            newsocket,
                            server_side=True,
                            certfile=self.certfile,
                            keyfile=self.keyfile,
                            ssl_version=self.ssl_version,
                        )
                    channel = SMTPChannel(
                        self,
                        newsocket,
                        fromaddr,
                        require_authentication=self.require_authentication,
                        credential_validator=self.credential_validator,
                        map=map
                    )

                    self.logger.info('_accept_subprocess(): '+
                                     'starting asyncore within subprocess.')

                    asyncore.loop(map=map)

                    self.logger.error('_accept_subprocess():'+
                                      'asyncore loop exited.')
            except (ExitNow, SSLError):
                self._shutdown_socket(newsocket)
                self.logger.info('_accept_subprocess():'+
                                 'smtp channel terminated asyncore.')
            except Exception as e:
                if newsocket is not None:
                    self._shutdown_socket(newsocket)
                self.logger.error('_accept_subprocess():'+
                                  ' uncaught exception: %s' % str(e))

    def _shutdown_socket(self, s):
        try:
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        except Exception as e:
            self.logger.error('_shutdown_socket(): failed\
            to cleanly shutdown socket: %s' % str(e))


    def run(self):
        asyncore.loop()
        if hasattr(signal, 'SIGTERM'):
            def sig_handler(signal,frame):
                self.logger.info("Got signal %s, shutting down." % signal)
                sys.exit(0)
            signal.signal(signal.SIGTERM, sig_handler)
        while 1:
            time.sleep(1)
