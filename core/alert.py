#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import traceback
from core.color import color_cmd
from core.log import get_logger
from core.time_helper import now
from core.compatible import is_verbose_mode

logger = get_logger("ohp_core")


def is_not_run_from_api():
    """
    check if framework run from API to prevent any alert

    Returns:
        True if run from API otherwise False
    """
    if "--start-api-server" in sys.argv \
            or (len(sys.argv) == 4 and "transforms" in sys.argv[1]):
        return False
    return True


def info(content):
    """
    build the info message, log the message in
    database if requested, rewrite the thread temporary file

    Args:
        content: content of the message

    Returns:
        None
    """
    sys.stdout.buffer.write(
        bytes(
            color_cmd("yellow")
            + "[+] [{0}] ".format(now())
            + color_cmd("green")
            + content
            + color_cmd("reset")
            + "\n",
            "utf8"
        )
    )
    sys.stdout.flush()
    return


def write(content):
    """
    simple print a message

    Args:
        content: content of the message

    Returns:
        None
    """
    sys.stdout.buffer.write(
        bytes(content, "utf8") if isinstance(content, str) else content
    )
    sys.stdout.flush()
    return


def warn(content):
    """
    build the warn message

    Args:
        content: content of the message

    Returns:
        the message in warn structure - None
    """
    logger.warning(content)
    sys.stdout.buffer.write(
        bytes(
            color_cmd("blue")
            + "[!] [{0}] ".format(now())
            + color_cmd("yellow")
            + content
            + color_cmd("reset")
            + "\n",
            "utf8")
    )
    sys.stdout.flush()

    return


def verbose_info(content):
    """
    build the info message, log the message in database
    if requested, rewrite the thread temporary file

    Args:
        content: content of the message

    Returns:
        None
    """
    if is_verbose_mode():
        logger.info(content)
        sys.stdout.buffer.write(
            bytes(
                color_cmd("cyan")
                + "[v] [{0}] ".format(now())
                + color_cmd("grey")
                + content
                + color_cmd("reset")
                + "\n",
                "utf8"
            )
        )
        sys.stdout.flush()
    return


def error(content):
    """
    build the error message

    Args:
        content: content of the message

    Returns:
        the message in error structure - None
    """
    logger.error(content)
    sys.stdout.buffer.write(
        (color_cmd("red")
         + "[X] [{0}] ".format(now())
         + color_cmd("yellow")
         + content + color_cmd("reset")
         + "\n"
         ).encode("utf8")
    )

    if "--v" in sys.argv or "--very-verbose" in sys.argv:
        sys.stdout.buffer.write(
            (color_cmd("red")
             + "[X] [{0}] ".format(now())
             + color_cmd("yellow")
             + "Command entered by the user: "
             + color_cmd("green")
             + "python " + " ".join(sys.argv)
             + "\n"
             ).encode("utf8")
        )

    if "---v" in sys.argv or "--extreme-verbose" in sys.argv:
        sys.stdout.buffer.write(
            (color_cmd("red")
             + "[X] [{0}] ".format(now())
             + color_cmd("yellow")
             + "Command entered by the user: "
             + color_cmd("green")
             + "python " + " ".join(sys.argv)
             + "\n"
             ).encode("utf8")
        )
        sys.stdout.buffer.write(
            (color_cmd("red")
             + "[X] [{0}] ".format(now())
             + "Stack Trace \n"
             ).encode("utf8")
        )
        for line in traceback.format_stack():
            sys.stdout.buffer.write(
                (color_cmd("red")

                 + line
                 ).encode("utf8")
            )

    sys.stdout.flush()
    return


def write_to_api_console(content):
    """
    simple print a message in API mode

    Args:
        content: content of the message

    Returns:
        None
    """
    sys.stdout.buffer.write(
        bytes(content, "utf8")
    )
    sys.stdout.flush()
    return
