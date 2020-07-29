#!/usr/bin/python3

import socket
import _thread
import threading
from datetime import datetime
import json

users = {}
HOST = ''
PORT = 21
LOGFILE = '/root/logs/ohp_ftp_strong_password_creds_logs.txt'
LOGFILE_LOCK = threading.Lock()
SERVER_CONFIG = '/root/server.conf'
USER_CONFIG = '/root/users.conf'


def init_user_conf():
    f = open(USER_CONFIG, 'r')
    user_conf_lines = f.read().split('\n')
    for user_conf_line in user_conf_lines:
        split_line = user_conf_line.split(':')
    if len(split_line) >= 2:
        username = split_line[0]
        password = split_line[1]
        users[username] = password


def init_server_conf():
    f = open(SERVER_CONFIG, 'r')
    server_conf_lines = f.read().split('\n')
    for server_conf_line in server_conf_lines:
        split_line = server_conf_line.split('=')
    if len(split_line) >= 2:
        conf_variable_key = split_line[0]
        conf_variable_value = split_line[1]
        if conf_variable_key == 'PORT':
            port = int(conf_variable_value)
        elif conf_variable_key == 'HOST':
            if conf_variable_value != 'DEFAULT':
                host = str(conf_variable_value)
    return host, port


def clientThread(conn, connip):
    isLoggedIn = False
    isRecivingPassword = False
    login_user = ""
    log_msg = ""
    while True:
        conn_data = conn.recv(1024).decode()
        if not isLoggedIn and conn_data.startswith('USER'):
            login_user = conn_data[5:]
            conn.sendall('331 Please specify the password.\n'.encode())
            isRecivingPassword = True
        elif isRecivingPassword:
            if conn_data.startswith('PASS'):
                login_user = login_user.replace('\n', '').replace('\r', '')
                password = conn_data[5:].replace('\n', '').replace('\r', '')
                if login_user in users.keys() and not (login_user == '*'):
                    if users[login_user] == password:
                        conn.sendall('230 Login successful.\n'.encode())
                        log_msg = "SUCCESSFUL"
                    elif users[login_user] == '*':
                        conn.sendall('230 Login successful.\n'.encode())
                        log_msg = "SUCCESSFUL"
                    else:
                        conn.sendall('530 Incorrect Login.\n'.encode())
                        log_msg = 'FAILED'
                elif '*' in users.keys():
                    if users['*'] == password:
                        conn.sendall('230 Login successful.\n'.encode())
                        log_msg = "SUCCESSFUL"
                    else:
                        conn.sendall('530 Incorrect Login.\n'.encode())
                        log_msg = ' FAILED'
                else:
                    log_msg = 'FAILED'
                    conn.sendall('530 Incorrect Login.\n'.encode())
            if (log_msg != ''):
                print(log_msg)
                LOGFILE_LOCK.acquire()
                try:
                    logfile_handle = open(LOGFILE, "a")
                    logfile_handle.write(
                        json.dumps(
                            {
                                "username": login_user,
                                "password": password,
                                "ip": connip,
                                'login_status': log_msg,
                                "module_name": "ftp/strong_password",
                                'date':
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                        ) + "\n"
                    )
                    logfile_handle.close()
                finally:
                    LOGFILE_LOCK.release()
                    log_msg = ''
                    isRecivingPassword = False


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def init_ftp_server():
    s.bind((HOST, PORT))
    s.listen(50)
    print("FTP Honeypot running.")
    while 1:
        conn, addr = s.accept()
        print("client logged in from IP:" + str(addr[0]) + ":" + str(addr[1]))
        conn.sendall("220 (vsFTPd 3.0.3)\n".encode())
        _thread.start_new_thread(clientThread, (conn, str(addr[0])))


def getDateTime():
    now = datetime.now()
    currentDateTime = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    return currentDateTime


if __name__ == '__main__':
    print('Starting logging, Date (DD/MM/YY): ' + getDateTime() + "\n")
    print("configuring server settings...")
    try:
        HOST, PORT = init_server_conf()
    except Exception as e:
        print("FAILED: " + str(e))
        print("configuring FTP users...")
    try:
        init_user_conf()
    except Exception as e:
        print("FAILED: " + str(e))
    REAL_HOST = HOST
    if REAL_HOST == '':
        REAL_HOST = '*'
    print("Starting FTP Honeypot on: " + REAL_HOST + ":" + str(PORT) + "...")
    try:
        init_ftp_server()
    except Exception as e:
        print("FAILED: " + str(e))
