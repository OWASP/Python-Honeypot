#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Credits : https://github.com/awhitehatter/mailoney
"""

import socket
import threading
import sys
import os
import datetime
import json


IP_ADDRESS = "0.0.0.0"
PORT = 25
MAIL_SERVERNAME = os.environ["MAILSERVER_NAME"]
LOGFILE = '/root/logs/ohp_smtp_honeypot_logs.txt'
output_lock = threading.Lock()


def log_to_file(ip, port, auth):
    output_lock.acquire()
    try:
        logfile_handle = open(LOGFILE, "a")
        logfile_handle.write(
            json.dumps(
                {
                    "ip": ip,
                    "authorization": auth,
                    "port": port,
                    'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "module_name": "smtp/strong_password",
                }
            ) + "\n"
        )
        logfile_handle.close()
    finally:
        output_lock.release()



def smtp_server():

    # server set up
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP_ADDRESS, PORT))
    server.listen(10)

    # setup the Postfix EHLO Response
    ehlo = '''250 {}
    250-PIPELINING
    250-SIZE 10240000
    250-VRFY
    250-ETRN
    250-STARTTLS
    250-AUTH LOGIN PLAIN
    250 8BITMIME\n'''.format(MAIL_SERVERNAME)

    print ('[*] SMTP Server listening on {}:{}'.format(IP_ADDRESS, PORT))

    def handle_client(client_socket):
        # Send banner
        client_socket.send('220 {} ESMTP Postfix\n'.\
                           format(MAIL_SERVERNAME).encode())

        while True:
            # Setup a loop to communicate with the client
            count = 0
            while count < 10:
                request=client_socket.recv(4096).lower()

                if b'ehlo' in request:
                    client_socket.send(ehlo.encode())
                    break
                else:
                    client_socket.send(
                        '502 5.5.2 Error: command not recognized\n'.encode()
                    )
                    count += 1

                #kill the client for too many errors
                if count == 10:
                    client_socket.send(\
                                       '421 4.7.0 {} Error: too many errors\n'.\
                                       format(MAIL_SERVERNAME).encode())
                    client_socket.close()
                    break

                #reset the counter and hope for creds
                count = 0
                while count < 10:
                    request = client_socket.recv(4096)
                    if b'auth plain' in request.lower():
                        #pull the base64 string and validate
                        request = request.decode()
                        request_part = request.split(' ')
                        if len(request_part)>1:
                            auth = request_part[2]
                            log_to_file(addr[0],addr[1],auth)
                            client_socket.send('235 2.0.0 Authentication Failed\n'.encode())

                    elif b'exit' in request:
                        count = 10
                        break
                    else:
                        client_socket.send("502 5.5.2 Error: command not recognized\n".encode())
                        count += 1

                    #kill the connection for too many failures
            if count == 10:
                client_socket.send('421 4.7.0 {} Error: too many errors\n'.format(MAIL_SERVERNAME).encode())
                client_socket.close()
                break

            # reset the count
            count = 0

    while True:
        client,addr = server.accept()
        print ("[*]Accepted connection from {}:{}".format(addr[0],addr[1]))

            # now handle client data
        client_handler = threading.Thread(target=handle_client(client,))
        client_handler.start()


if __name__ == "__main__":
    smtp_server()
