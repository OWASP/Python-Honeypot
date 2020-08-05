#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Credits : https://github.com/awhitehatter/mailoney
"""

import socket
import sys
import errno
import time
import threading
import datetime
import asyncore
import asynchat
import os
import json

MAILSERVER_NAME = os.environ["MAILSERVER_NAME"]
BIND_IP='0.0.0.0'
BIND_PORT=25
LOGFILE = '/root/logs/ohp_smtp_honeypot_logs.txt'
__version__ = 'ESMTP Exim 4.69 #1 Thu, 29 Jul 2010 05:13:48 -0700'
EMPTYSTRING = ''
NEWLINE = '\n'

output_lock = threading.Lock()
hpc,hpfeeds_prefix = None,""

def log_to_file(ip, port, data):
    output_lock.acquire()
    try:
        logfile_handle = open(LOGFILE, "a")
        logfile_handle.write(
            json.dumps(
                {
                    "ip": ip,
                    "data": data,
                    "port": port,
                    "module_name": "smtp/mail_honeypot",
                    'date': datetime.datetime.now().\
                    strftime("%Y-%m-%d %H:%M:%S")
                }
            ) + "\n"
        )
        logfile_handle.close()
    finally:
        output_lock.release()


class SMTPChannel(asynchat.async_chat):
    COMMAND = 0
    DATA =1

    def __init__(self, server, conn, addr):
        asynchat.async_chat.__init__(self, conn)
        self.__rolling_buffer = ""
        self.__server = server
        self.__conn = conn
        self.__addr = addr
        self.__line = []
        self.__state = self.COMMAND
        self.__greeting = 0
        self.__mailfrom = None
        self.__rcpttos = []
        self.__data = ''
        self.__fqdn = MAILSERVER_NAME
        try:
            self.__peer = conn.getpeername()
        except socket.error as err:
            # a race condition  may occur if the other end is closing
            # before we can get the peername
            self.close()
            if err[0] != errno.ENOTCONN:
                raise
            return
        #print >> DEBUGSTREAM, 'Peer:', repr(self.__peer)
        self.push('220 %s %s' % (self.__fqdn, __version__))
        self.set_terminator(b'\r\n')

    # Overrides base class for convenience
    def push(self, msg):
        msg = msg + '\r\n'
        msg = msg.encode()
        asynchat.async_chat.push(self, msg)

    # # Implementation of base class abstract method
    def collect_incoming_data(self, data):
        data = data.decode('utf-8')
        self.__line.append(data)
        del data

    # Implementation of base class abstract method
    def found_terminator(self):
        line = EMPTYSTRING.join(self.__line)
        log_to_file(self.__addr[0], self.__addr[1], line)

        self.__line = []
        if self.__state == self.COMMAND:
            if not line:
                self.push('500 Error: bad syntax')
                return
            method = None
            i = line.find(' ')
            if i < 0:
                command = line.upper()
                arg = None
            else:
                command = line[:i].upper()
                arg = line[i+1:].strip()
            #command = command.decode('utf-8')
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
            status = self.__server.process_message(self.__peer, \
                                                   self.__mailfrom,\
                                                   self.__rcpttos,\
                                                   self.__data)
            self.__rcpttos = []
            self.__mailfrom = None
            self.__state = self.COMMAND
            self.set_terminator(b'\r\n')
            if not status:
                self.push('250 Ok')
            else:
                self.push(status)

    # SMTP and ESMTP commands
    def smtp_HELO(self, arg):
        if not arg:
            self.push('501 Syntax: HELO hostname')
            return
        if self.__greeting:
            self.push('503 Duplicate HELO/EHLO')
        else:
            self.__greeting = arg
            self.push('250 %s' % self.__fqdn)

    def smtp_EHLO(self, arg):
        if not arg:
            self.push('501 Syntax: EHLO hostname')
            return
        if self.__greeting:
            self.push('503 Duplicate HELO/EHLO')
        else:
            self.__greeting = arg
            self.push('250-{0} Hello {1} [{2}]'.format(self.__fqdn, \
                                                       arg, self.__addr[0]))
            self.push('250-SIZE 52428800')
            self.push('250 AUTH LOGIN PLAIN')

    def smtp_NOOP(self, arg):
        if arg:
            self.push('501 Syntax: NOOP')
        else:
            self.push('250 Ok')

    def smtp_QUIT(self, arg):
        # args is ignored
        self.push('221 Bye')
        self.close_when_done()

    def smtp_AUTH(self, arg):
        # Accept any auth attempt
        self.push('235 Authentication succeeded')

    # factored
    def __getaddr(self, keyword, arg):
        address = None
        keylen = len(keyword)
        print(keyword,arg)
        if arg[:keylen].upper() == keyword:
            address = arg[keylen:].strip()
            if not address:
                pass
            elif address[0] == '<' and address[-1] == '>' and address != '<>':
                # Addresses can be in the form <person@dom.com> but watch out
                # for null address, e.g. <>
                address = address[1:-1]
        return address

    def smtp_MAIL(self, arg):
        #print >> DEBUGSTREAM, '===> MAIL', arg
        address = self.__getaddr('FROM:', arg) if arg else None
        if not address:
            self.push('501 Syntax: MAIL FROM:<address>')
            return
        if self.__mailfrom:
            self.push('503 Error: nested MAIL command')
            return
        self.__mailfrom = address
        #print >> DEBUGSTREAM, 'sender:', self.__mailfrom
        self.push('250 Ok')

    def smtp_RCPT(self, arg):
        #print >> DEBUGSTREAM, '===> RCPT', arg
        if not self.__mailfrom:
            self.push('503 Error: need MAIL command')
            return
        address = self.__getaddr('TO:', arg) if arg else None
        if not address:
            self.push('501 Syntax: RCPT TO: <address>')
            return
        self.__rcpttos.append(address)
        #print >> DEBUGSTREAM, 'recips:', self.__rcpttos
        self.push('250 Ok')

    def smtp_RSET(self, arg):
        if arg:
            self.push('501 Syntax: RSET')
            return
        # Resets the sender, recipients, and data, but not the greeting
        self.__mailfrom = None
        self.__rcpttos = []
        self.__data = ''
        self.__state = self.COMMAND
        self.push('250 Ok')

    def smtp_DATA(self, arg):
        if not self.__rcpttos:
            self.push('503 Error: need RCPT command')
            return
        if arg:
            self.push('501 Syntax: DATA')
            return
        self.__state = self.DATA
        self.set_terminator(b'\r\n.\r\n')
        self.push('354 End data with <CR><LF>.<CR><LF>')


class SMTPServer(asyncore.dispatcher):
    def __init__(self, localaddr, remoteaddr):
        self._localaddr = localaddr
        self._remoteaddr = remoteaddr
        asyncore.dispatcher.__init__(self)
        try:
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            # try to re-use a server port if possible
            self.set_reuse_addr()
            self.bind(localaddr)
            self.listen(5)
        except:
            # cleanup asyncore.socket_map before raising
            self.close()
            raise
        else:
            pass
            #print (DEBUGSTREAM, '%s started at %s\n\tLocal addr: \
            #    %s\n\t\Remote addr:%s' % (self.__class__.__name__,\
            #time.ctime(time.time()), localaddr, remoteaddr)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            conn, addr = pair
            #print >> DEBUGSTREAM, 'Incoming connection from %s' % repr(addr)
            SMTPChannel(self, conn, addr)

    def handle_close(self):
        self.close()

    # API for "doing something useful with the message"
    def process_message(self, peer, mailfrom, rcpttos, data):
        """Override this abstract method to handle messages from the client.

        peer is a tuple containing (ipaddr, port) of the client that made the
        socket connection to our smtp port.

        mailfrom is the raw address the client claims the message is coming
        from.

        rcpttos is a list of raw addresses the client wishes to deliver the
        message to.

        data is a string containing the entire full text of the message,
        headers (if supplied) and all.  It has been `de-transparencied'
        according to RFC 821, Section 4.5.2.  In other words, a line
        containing a `.' followed by other text has had the leading dot
        removed.

        This function should return None, for a normal `250 Ok' response;
        otherwise it returns the desired response string in RFC 821 format.

        """
        raise NotImplementedError



def module():

    class SchizoOpenRelay(SMTPServer):

        def process_message(self, peer, mailfrom, rcpttos, data):
            #setup the Log File
            log_to_file(peer[0], peer[1], '')
            log_to_file(peer[0], peer[1], '*' * 50)
            log_to_file(peer[0], peer[1], 'Mail from: {0}'.format(mailfrom))
            log_to_file(peer[0], peer[1], 'Mail to: {0}'.format(", ".\
                                                                join(rcpttos)))
            log_to_file(peer[0], peer[1], data)

            loghpfeeds = {}
            loghpfeeds['ServerName'] = MAILSERVER_NAME
            loghpfeeds['Timestamp'] = format(time.time())
            loghpfeeds['SrcIP'] = peer[0]
            loghpfeeds['SrcPort'] = peer[1]
            loghpfeeds['MailFrom'] = mailfrom
            loghpfeeds['MailTo'] = format(", ".join(rcpttos))
            loghpfeeds['Data'] = data
            #log_to_hpfeeds("mail", json.dumps(loghpfeeds))


    def run():
        SchizoOpenRelay((BIND_IP, BIND_PORT), None)
        print ('[*] Mail Relay listening on {}:{}'.format(BIND_IP,BIND_PORT))
        try:
            asyncore.loop()
            print ("exiting for some unknown reason")
        except KeyboardInterrupt:
            print ('Detected interruption, terminating...')
    run()

if __name__ == "__main__":
    module()
