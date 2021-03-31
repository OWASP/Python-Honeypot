from secure_smtpd import SMTPServer
import asyncore
import sys
import threading
import json
import datetime

LOGFILE = '/root/logs/ohp_smtp_honeypot_logs.txt'


class FakeCredentialValidator:
    def __init__(self):
        self.output_lock = threading.Lock()

    def log_to_file(self, ip, port, username, password):
        self.output_lock.acquire()
        try:
            logfile_handle = open(LOGFILE, "a")
            logfile_handle.write(
                json.dumps(
                    {
                        "ip": ip,
                        "username": username,
                        "password": password,
                        "port": port,
                        'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "module_name": "smtp/strong_password",
                    }
                ) + "\n"
            )
            logfile_handle.close()
        finally:
            self.output_lock.release()

    def validate(self, username, password, fromaddr):
        self.log_to_file(fromaddr[0], fromaddr[1], username, password)
        return False


try:
    SMTPServer(
        ('0.0.0.0', 25),
        None,
        require_authentication=True,
        ssl=False,
        credential_validator=FakeCredentialValidator(),
    ).run()
except Exception as e:
    print(e)
    sys.exit()
