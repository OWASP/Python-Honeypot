#!/usr/bin/env python
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import concurrent
import sys
import os
import subprocess
import random
import string
import shutil
import inspect
import json
import elasticsearch
from core.color import reset_cmd_color
from core.exit_helper import exit_failure
from shutil import which


def logo():
    """
    OWASP HoneyPot Logo
    """
    # TODO : Fix the cyclic dependency later
    from core.alert import write_to_api_console
    write_to_api_console(open('.owasp_honeypot').read())
    reset_cmd_color()


def version():
    """
    version of python

    Returns:
        integer version of python (2 or 3)
    """
    return int(sys.version_info[0])


def os_name():
    """
    OS name

    Returns:
        OS name in string
    """
    return sys.platform


def get_timeout_error():
    """
    Get the timeout error thrown by pyshark apply_on_packets function
    """
    try:
        # If asyncio timeout error exists, this will be returned
        return asyncio.exceptions.TimeoutError
    except Exception:
        # For older python versions, where asyncio timeout error
        # doesn't exist, this one will be returned.
        return concurrent.futures._base.TimeoutError


def check_for_requirements(start_api_server):
    """
    check if requirements exist

    Returns:
        True if exist otherwise False
    """
    # TODO : Fix the cyclic dependency later
    from config import api_configuration
    from core.messages import load_messages
    messages = load_messages().message_contents
    # check external required modules
    api_config = api_configuration()
    external_modules = open(os.path.join(os.getcwd(), 'requirements.txt'), 'r').read().split('\n')
    for module_name in external_modules:
        try:
            __import__(
                module_name.split('==')[0] if 'library_name=' not in module_name
                else module_name.split('library_name=')[1].split()[0]
            )
        except Exception:
            exit_failure(
                "pip3 install -r requirements.txt ---> " + module_name + " not installed!"
            )
    # check elasticsearch
    try:
        connection = elasticsearch.Elasticsearch(
            api_config["api_database"],
            http_auth=api_config["api_database"]
        )
        connection.indices.get_alias("*")
    except Exception:
        exit_failure(messages["elasticsearch_not_found"])
    # check if its honeypot server not api server
    if not start_api_server:
        # check docker
        try:
            subprocess.check_output(["docker", "--help"],
                                    stderr=subprocess.PIPE)
        except Exception:
            exit_failure(messages["cannot_communicate_with_docker"])
        # check for commandline requirements
        commands = {
            'tshark': which('tshark'),
            'ps': which('ps'),
            'grep': which('grep'),
            'kill': which('kill')
        }
        for command in commands:
            if commands[command] is None:
                exit_failure(
                    messages["install_tools"] + "{0}".format(json.dumps(commands, indent=4))
                )
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
        "tmp/thread_" + "".join(
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
    return "".join(random.choice("0123456789abcdef") for _ in range(length))


def byte_to_str(data):
    """
    convert data to str

    :param data: data
    :return: str(data)
    """
    return str(
        data if isinstance(data, str) else data.decode() if data is not None else ""
    )


def is_verbose_mode():
    """
    is run as verbose mode?

    :return: boolean
    """
    return '--verbose' in sys.argv or '-v' in sys.argv
