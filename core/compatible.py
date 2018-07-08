#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
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
    from core import color
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


def check_for_requirements():
    """
    check if requirements exist

    Returns:
        True if exist otherwise False
    """
    # first requirement is docker
    from core.alert import messages
    if os.popen("docker info").read() == "":
        __die_failure(messages("en", "docker_error"))
    return True


def hours(hours):
    """
    integer to hour(s)
    Args:
        hours: hours (integer)

    Returns:
        seconds equal to hours (integer)
    """

    return int(hours) * 60 * 60


def make_tmp_thread_dir():
    """
    create random thread directory

    Returns:
        name of directory or False
    """
    return mkdir("tmp/thread_"
                 + "".join([str(string.string.ascii_uppercase + string.string.ascii_lowercase + string.digits)[
                                random.randint(0, len(str(string.uppercase + string.lowercase +
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
