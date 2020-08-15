import socket
import smtplib
import secure_smtpd
from .smtp_server import SMTPServer
from .store_credentials import StoreCredentials

class ProxyServer(SMTPServer):
    """Implements an open relay.  Inherits from secure_smtpd, so can handle
    SSL incoming.  Modifies attributes slightly:

    * if "ssl" is true accepts SSL connections inbound and connects via SSL
        outbound
    * adds "ssl_out_only", which can be set to True when "ssl" is False so that
        inbound connections are in plain text but outbound are in SSL
    * adds "debug", which if True copies all inbound messages to logger.info()
    * ignores any credential validators, passing any credentials upstream
    """
    def __init__(self, *args, **kwargs):
        self.ssl_out_only = False
        if 'ssl_out_only' in kwargs:
            self.ssl_out_only = kwargs.pop('ssl_out_only')

        self.debug = False
        if 'debug' in kwargs:
            self.debug = kwargs.pop('debug')

        if kwargs['credential_validator'] is None:
            kwargs['credential_validator'] = StoreCredentials()

        SMTPServer.__init__(self, *args, **kwargs)

    def process_message(self, peer, mailfrom, rcpttos, data):
        if self.debug:
            # ------------------------
            # stolen directly from stmpd.DebuggingServer
            inheaders = 1
            lines = data.split('\n')
            self.logger.info('---------- MESSAGE FOLLOWS ----------')
            for line in lines:
                # headers first
                if inheaders and not line:
                    self.logger.info('X-Peer: %s', peer[0])
                    inheaders = 0
                self.logger.info(line)
            self.logger.info('------------ END MESSAGE ------------')

        # ------------------------
        # following code is direct from smtpd.PureProxy
        lines = data.split('\n')
        # Look for the last header
        i = 0
        for line in lines:
            if not line:
                break
            i += 1
        lines.insert(i, 'X-Peer: %s' % peer[0])
        data = '\n'.join(lines)
        self._deliver(mailfrom, rcpttos, data)

    def _deliver(self, mailfrom, rcpttos, data):
        # ------------------------
        # following code is adapted from smtpd.PureProxy with modifications to
        # handle upstream SSL
        refused = {}
        try:
            if self.ssl or self.ssl_out_only:
                s = smtplib.SMTP_SSL()
            else:
                s = smtplib.SMTP()

            s.connect(self._remoteaddr[0], self._remoteaddr[1])
            if self.credential_validator.stored:
                # we had credentials passed in, use them
                s.login(
                    self.credential_validator.username,
                    self.credential_validator.password
                )
            try:
                refused = s.sendmail(mailfrom, rcpttos, data)
                if refused != {}:
                    self.logger.error('some connections refused %s', refused)
            finally:
                s.quit()
        except smtplib.SMTPRecipientsRefused as e:
            self.logger.exception('')
            refused = e.recipients
        except (socket.error, smtplib.SMTPException) as e:
            self.logger.exception('')

            # All recipients were refused.  If the exception had an associated
            # error code, use it.  Otherwise,fake it with a non-triggering
            # exception code.
            errcode = getattr(e, 'smtp_code', -1)
            errmsg = getattr(e, 'smtp_error', 'ignore')
            for r in rcpttos:
                refused[r] = (errcode, errmsg)
        return refused
