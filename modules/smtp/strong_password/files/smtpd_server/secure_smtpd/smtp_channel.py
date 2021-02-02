import secure_smtpd
import smtpd
import base64
import asynchat
import logging
import os

from asyncore import ExitNow
NEWLINE = '\n'
EMPTYSTRING = ''
FQDN = os.environ["MAILSERVER_NAME"]

def decode_b64(data):
    '''Wrapper for b64decode, without having to struggle with bytestrings.'''
    byte_string = data.encode('utf-8')
    decoded = base64.b64decode(byte_string)
    return decoded.decode('utf-8')


def encode_b64(data):
    '''Wrapper for b64encode, without having to struggle with bytestrings.'''
    byte_string = data.encode('utf-8')
    encoded = base64.b64encode(byte_string)
    return encoded.decode('utf-8')


class SMTPChannel(smtpd.SMTPChannel):

    def __init__(self, smtp_server, newsocket, fromaddr,\
                 require_authentication=False,\
                 credential_validator=None, map=None):
        smtpd.SMTPChannel.__init__(self, smtp_server, newsocket, fromaddr)
        asynchat.async_chat.__init__(self, newsocket, map=map)

        self.require_authentication = require_authentication
        self.authenticating = False
        self.fromaddr = fromaddr
        self.authenticated = False
        self.username = None
        self.password = None
        self.credential_validator = credential_validator
        self.logger = logging.getLogger(secure_smtpd.LOG_NAME)

    def smtp_QUIT(self, arg):
        self.push('221 Bye')
        self.close_when_done()
        raise ExitNow()

    def collect_incoming_data(self, data):
        if not isinstance(data, str):
            # We're on python3, so we have to decode the bytestring
            data = data.decode('utf-8')
        self.__line.append(data)

    def smtp_EHLO(self, arg):
        if not arg:
            self.push('501 Syntax: HELO hostname')
            return
        if self.__greeting:
            self.push('503 Duplicate HELO/EHLO')
        else:
            self.__greeting = arg
            self.push('250-%s Hello %s' % (FQDN, arg))
            self.push('250-AUTH LOGIN PLAIN')
            self.push('250 EHLO')

    def smtp_AUTH(self, arg):
        if 'PLAIN' in arg:
            split_args = arg.split(' ')
            # second arg is Base64-encoded string of blah\0username\0password
            authbits = decode_b64(split_args[1]).split('\0')
            self.username = authbits[1]
            self.password = authbits[2]
            #print(self.fromaddr,self.newsocket)
            if self.credential_validator and \
            self.credential_validator.validate(self.username,\
                                               self.password,self.fromaddr):
                self.authenticated = True
                self.push('235 Authentication successful.')
            else:
                self.push('454 Temporary authentication failure.')
                raise ExitNow()

        elif 'LOGIN' in arg:
            self.authenticating = True
            split_args = arg.split(' ')

            # Some implmentations of 'LOGIN' seem to provide the username
            # along with the 'LOGIN' stanza, hence both situations are
            # handled.
            if len(split_args) == 2:
                self.username = decode_b64(arg.split(' ')[1])
                self.push('334 ' + encode_b64('Username'))
            else:
                self.push('334 ' + encode_b64('Username'))

        elif not self.username:
            self.username = decode_b64(arg)
            self.push('334 ' + encode_b64('Password'))
        else:
            self.authenticating = False
            self.password = decode_b64(arg)
            if self.credential_validator and \
               self.credential_validator.validate(self.username,\
                                                  self.password):
                self.authenticated = True
                self.push('235 Authentication successful.')
            else:
                self.push('454 Temporary authentication failure.')
                raise ExitNow()

    # This code is taken directly from the underlying smtpd.SMTPChannel
    # support for AUTH is added.
    def found_terminator(self):
        line = EMPTYSTRING.join(self.__line)

        if self.debug:
            self.logger.info('found_terminator(): data: %s' % repr(line))

        self.__line = []
        if self.__state == self.COMMAND:
            if not line:
                self.push('500 Error: bad syntax')
                return
            method = None
            i = line.find(' ')

            if self.authenticating:
                # If we are in an authenticating state, call the
                # method smtp_AUTH.
                arg = line.strip()
                command = 'AUTH'
            elif i < 0:
                command = line.upper()
                arg = None
            else:
                command = line[:i].upper()
                arg = line[i + 1:].strip()

            # White list of operations that are allowed prior to AUTH.
            if not command in ['AUTH', 'EHLO', 'HELO', 'NOOP', 'RSET', 'QUIT']:
                if self.require_authentication and not self.authenticated:
                    self.push('530 Authentication required')
                    return

            method = getattr(self, 'smtp_' + command, None)
            if not method:
                self.push('502 Error: command "%s" not implemented' % command)
                return
            method(arg)
            return
        else:
            if self.__state != self.DATA:
                self.push('451 Internal confusion')
                return
            # Remove extraneous carriage returns and de-transparency according
            # to RFC 821, Section 4.5.2.
            data = []
            for text in line.split('\r\n'):
                if text and text[0] == '.':
                    data.append(text[1:])
                else:
                    data.append(text)
            self.__data = NEWLINE.join(data)
            status = self.__server.process_message(
                self.__peer,
                self.__mailfrom,
                self.__rcpttos,
                self.__data
            )
            self.__rcpttos = []
            self.__mailfrom = None
            self.__state = self.COMMAND
            self.set_terminator(b'\r\n')
            if not status:
                self.push('250 Ok')
            else:
                self.push(status)
