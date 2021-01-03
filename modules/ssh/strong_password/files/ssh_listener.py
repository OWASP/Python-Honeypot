#!/usr/bin/env python3
import socket
import sys
import threading
import _thread
import paramiko
import json
import datetime

HOST_KEY = paramiko.RSAKey(filename='/root/.ssh/id_rsa')
SSH_PORT = 22
LOGFILE = '/root/logs/ohp_ssh_strong_password_creds_logs.txt'
LOGFILE_LOCK = threading.Lock()


class SSHServerHandler(paramiko.ServerInterface):
    def __init__(self, client_addr):
        self.event = threading.Event()
        self.ip = client_addr[0]

    def check_auth_password(self, username, password):
        LOGFILE_LOCK.acquire()
        try:
            logfile_handle = open(LOGFILE, "a")
            logfile_handle.write(
                json.dumps(
                    {
                        "username": username,
                        "password": password,
                        "ip": str(self.ip),
                        "module_name": "ssh/strong_password",
                        'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                ) + "\n"
            )
            logfile_handle.close()
        finally:
            LOGFILE_LOCK.release()
        return paramiko.AUTH_FAILED

    @staticmethod
    def get_allowed_auths(username):
        return 'password'


def handle_connections(client, client_addr):
    transport = paramiko.Transport(client)
    transport.add_server_key(HOST_KEY)
    server_handler = SSHServerHandler(client_addr)

    transport.start_server(server=server_handler)

    channel = transport.accept(1)
    if channel is not None:
        channel.close()


def main():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("", SSH_PORT))
        server_socket.listen(100)
        paramiko.util.log_to_file('/root/logs/paramiko.log')

        while True:
            try:
                client_socket, client_addr = server_socket.accept()
                _thread.start_new_thread(handle_connections, (client_socket, client_addr))
            except Exception as e:
                print("ERROR: Client handling", e)

    except Exception as e:
        print("ERROR: Failed to create socket", e)
        sys.exit(1)


main()
