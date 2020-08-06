#!/usr/bin/env python
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import random
import string
import shutil
import inspect

from core.color import reset_cmd_color
from core.exit_helper import exit_failure


def logo():
    """
    OWASP HoneyPot Logo
    """
    # TODO : Fix the cyclic dependency later
    from core.alert import write_to_api_console
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
    reset_cmd_color()


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
    from core.alert import messages
    if os_name() not in ["linux", "darwin", "win32", "win64"]:
        exit_failure(messages(language, "error_platform"))
    if version() == 2 or version() == 3:
        pass
    else:
        exit_failure(messages(language, "python_version_error"))
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
    from config import api_configuration
    from core.alert import messages
    # check external required modules
    api_config = api_configuration()
    connection_timeout = api_config["api_database_connection_timeout"]
    try:
        import pymongo
        import netaddr
        import flask
        del netaddr
        del flask
    except Exception:
        exit_failure("pip install -r requirements.txt")
    # check mongodb
    try:
        connection = pymongo.MongoClient(
            api_config["api_database"],
            serverSelectionTimeoutMS=connection_timeout
        )
        connection.list_database_names()
    except Exception:
        exit_failure("cannot connect to mongodb")
    # check if its honeypot server not api server
    if not start_api_server:
        # check docker
        try:
            subprocess.check_output(["docker", "--help"],
                                    stderr=subprocess.PIPE)
        except Exception:
            exit_failure(messages("en", "docker_error"))
        # check tshark
        try:
            subprocess.check_output(["tshark", "--help"],
                                    stderr=subprocess.PIPE)
        except Exception:
            exit_failure("please install tshark first!")
    return True


def make_tmp_thread_dir():
    """
    create random thread directory

    Returns:
        name of directory or False
    """
    uppercase_string = string.ascii_uppercase
    lowercase_string = string.ascii_lowercase
    digits = string.digits
    combined_string = uppercase_string + lowercase_string + digits
    return mkdir(
        "tmp/thread_".join(
            [
                combined_string[random.randint(0, len(combined_string) - 1)] for _ in range(15)
            ]
        )
    )


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
        except Exception:
            return False
    return dir


def copy_dir_tree(src, dst, symlinks=True, ignore=None):
    """
    copytree a directory

    Args:
        src: source directory
        dst: destination directory
        symlinks: copy symlinks
        ignore: ignore

    Returns:
        True
    """
    # https://stackoverflow.com/a/12514470
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
    return True


def get_module_dir_path(module):
    """
    get a module path

    Args:
        module: module

    Returns:
        path
    """
    return os.path.dirname(
        inspect.getfile(module)
    )


def generate_token(length=32):
    """
    generate token using hex chars

    Args:
        length: length of token - default 32

    Returns:
        token string
    """
    return "".join(random.choice("0123456789abcdef") for _ in range(32))


def byte_to_str(data):
    """
    convert data to str

    :param data: data
    :return: str(data)
    """
    return str(data if isinstance(data, str) else data.decode()
    if isinstance(data, bytes) else data)


def is_verbose_mode():
    """
    is run as verbose mode?

    :return: boolean
    """
    return '--verbose' in sys.argv or '-v' in sys.argv
