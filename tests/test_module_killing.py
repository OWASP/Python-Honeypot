import os
import sys
import unittest
import subprocess
import signal
from os.path import dirname, abspath
from time import time

from core.messages import load_messages

messages = load_messages().message_contents


def run_container_in_sub_process(command, kill_container_command):
    is_network_traffic_capture_started = False
    parent_directory = str(dirname(dirname(abspath(__file__))))
    output = str()
    expected_result = False
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=False,
                               cwd=parent_directory)
    start_time = time()
    for c in iter(lambda: process.stdout.read(1), b""):
        if time() - start_time > 300:
            os.kill(process.pid, signal.SIGINT)
            break
        sys.stdout.buffer.write(c)
        output += c.decode("utf-8")
        if messages["network_traffic_capture_start"] in output and is_network_traffic_capture_started is False:
            is_network_traffic_capture_started = True
            os.system(kill_container_command)
        elif is_network_traffic_capture_started is True and "finished." in output:
            expected_result = True
            break
    assert True is expected_result


class TestModules(unittest.TestCase):

    def test_module_ftp_weak_password(self):
        kill_container_command = "docker kill ohp_ftpserver_weak_password"
        command = ["python3", "ohp.py", "-m", "ftp/weak_password"]
        run_container_in_sub_process(command, kill_container_command)

    def test_module_ftp_strong_password(self):
        kill_container_command = "docker kill ohp_ftpserver_strong_password"
        command = ["python3", "ohp.py", "-m", "ftp/strong_password"]
        run_container_in_sub_process(command, kill_container_command)

    def test_module_http_basic_auth_strong_password(self):
        kill_container_command = "docker kill ohp_httpserver_basic_auth_strong_password"
        command = ["python3", "ohp.py", "-m", "http/basic_auth_strong_password"]
        run_container_in_sub_process(command, kill_container_command)

    def test_module_http_basic_auth_weak_password(self):
        kill_container_command = "docker kill ohp_httpserver_basic_auth_weak_password"
        command = ["python3", "ohp.py", "-m", "http/basic_auth_weak_password"]
        run_container_in_sub_process(command, kill_container_command)

    def test_module_http_ics_veeder_root_guardian_ast(self):
        kill_container_command = "docker kill ohp_icsserver_veeder_root_guardian_ast"
        command = ["python3", "ohp.py", "-m", "ics/veeder_root_guardian_ast"]
        run_container_in_sub_process(command, kill_container_command)

    def test_module_smtp_strong_password(self):
        kill_container_command = "docker kill ohp_smtpserver_strong_password"
        command = ["python3", "ohp.py", "-m", "smtp/strong_password"]
        run_container_in_sub_process(command, kill_container_command)

    def test_module_ssh_weak_password(self):
        kill_container_command = "docker kill ohp_sshserver_weak_password"
        command = ["python3", "ohp.py", "-m", "ssh/weak_password"]
        run_container_in_sub_process(command, kill_container_command)

    def test_module_ssh_strong_password(self):
        kill_container_command = "docker kill ohp_sshserver_strong_password"
        command = ["python3", "ohp.py", "-m", "ssh/strong_password"]
        run_container_in_sub_process(command, kill_container_command)
