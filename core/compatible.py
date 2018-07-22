#!/usr/bin/env python
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import random
import string
from core._die import __die_failure

__version__ = "0.0.1"
__code_name__ = "SAME"


def _version_info():
    """
    version information of the framework

    Returns:
        an array of version and code name
    """
    return [__version__, __code_name__]


def logo():
    """
    OWASP HoneyPot Logo
    """
    from core.alert import write_to_api_console
    from core.color import finish
    write_to_api_console("""
      ______          __      _____ _____  
     / __ \ \        / /\    / ____|  __ \ 
    | |  | \ \  /\  / /  \  | (___ | |__) |
    | |  | |\ \/  \/ / /\ \  \___ \|  ___/  
    | |__| | \  /\  / ____ \ ____) | |      
     \____/   \/  \/_/    \_\_____/|_|
                      _    _                        _____      _   
                     | |  | |                      |  __ \    | |  
                     | |__| | ___  _ __   ___ _   _| |__) |__ | |_ 
                     |  __  |/ _ \| "_ \ / _ \ | | |  ___/ _ \| __|
                     | |  | | (_) | | | |  __/ |_| | |  | (_) | |_ 
                     |_|  |_|\___/|_| |_|\___|\__, |_|   \___/ \__|
                                               __/ |
                                              |___/   \n\n""")
    finish()


def version():
    """
    version of python

    Returns:
        integer version of python (2 or 3)
    """
    return int(sys.version_info[0])


def check(language):
    """
    check if framework compatible with the OS
    Args:
        language: language

    Returns:
        True if compatible otherwise None
    """
    # from core.color import finish
    from core.alert import messages
    if "linux" in os_name() or "darwin" in os_name():
        pass
        # os.system("clear")
    elif "win32" == os_name() or "win64" == os_name():
        # if language != "en":
        #    from core.color import finish
        #    from core.alert import error
        #   error("please use english language on windows!")
        #    finish()
        #    sys.exit(1)
        # os.system("cls")
        pass
    else:
        __die_failure(messages(language, "error_platform"))
    if version() is 2 or version() is 3:
        pass
    else:
        __die_failure(messages(language, "python_version_error"))
    logo()
    return True


def os_name():
    """
    OS name

    Returns:
        OS name in string
    """
    return sys.platform


def is_windows():
    """
    check if the framework run in Windows OS

    Returns:
        True if its running on windows otherwise False
    """
    if "win32" == os_name() or "win64" == os_name():
        return True
    return False


def check_for_requirements(start_api_server):
    """
    check if requirements exist

    Returns:
        True if exist otherwise False
    """
    from core.alert import messages
    from config import api_configuration
    # check external required modules
    try:
        import pymongo
        import netaddr
        import flask
        del netaddr
        del flask
    except Exception as _:
        __die_failure("pip install -r requirements.txt")
    # check mongodb
    try:
        connection = pymongo.MongoClient(api_configuration()["api_database"],
                                         serverSelectionTimeoutMS=api_configuration()[
                                             "api_database_connection_timeout"])
        connection.list_database_names()
    except Exception as _:
        __die_failure("cannot connect to mongodb")
    # check if its honeypot server not api server
    if not start_api_server:
        # check docker
        try:
            subprocess.check_output(["docker", "--help"], stderr=subprocess.PIPE)
        except Exception as _:
            __die_failure(messages("en", "docker_error"))
        # check tshark
        try:
            subprocess.check_output(["tshark", "--help"], stderr=subprocess.PIPE)
        except Exception as _:
            __die_failure("please install tshark fist!")
    return True


def make_tmp_thread_dir():
    """
    create random thread directory

    Returns:
        name of directory or False
    """
    return mkdir("tmp/thread_"
                 + "".join([str(string.ascii_uppercase + string.ascii_lowercase + string.digits)[
                                random.randint(0, len(str(string.ascii_uppercase + string.ascii_lowercase +
                                                          string.digits)) - 1)] for i in range(15)]))


def mkdir(dir):
    """
    create directory

    Args:
        dir: directory path

    Returns:
        Name of directory or False
    """
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
        except Exception as _:
            return False
    return dir


def generate_token(length=32):
    """
    generate token using hex chars

    Args:
        length: length of token - default 32

    Returns:
        token string
    """
    return "".join(random.choice("0123456789abcdef") for _ in range(32))
