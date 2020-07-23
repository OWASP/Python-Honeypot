#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
from core import color
from core.compatible import version
from core.time_helper import now


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


def messages(language, msg_id):
    """
    load a message from message library with specified language

    Args:
        language: language
        msg_id: message id

    Returns:
        the message content in the selected language if message found \
        otherwise return message in English
    """
    # Returning selected language
    # todo: fix -1 to a variable name or add comment
    if language == -1:
        return list(
            set(
                [
                    langs.rsplit("_")[1].rsplit(".")[0] for langs in
                    os.listdir(
                        os.path.dirname(
                            os.path.abspath(__file__)
                        ).replace(
                            "\\", "/"
                        ) + "/../lib/language/"
                    )
                    if langs != "readme.md" and langs.rsplit("_")[1].rsplit(".")[0] != ""
                ]
            )
        )
    # Importing messages
    try:
        msgs = getattr(
            __import__(
                "lib.language.messages_{0}".format(language),
                fromlist=["all_messages"]
            ),
            "all_messages"
        )()[str(msg_id)]
    except Exception:
        msgs = getattr(
            __import__(
                "lib.language.messages_en",
                fromlist=["all_messages"]
            ),
            "all_messages"
        )()[str(msg_id)]
    if version() == 2:
        return msgs.decode("utf8")
    return msgs


def input_msg(content):
    """
    build the input message to get input from users

    Args:
        content: content of the message

    Returns:
        the message in input structure
    """
    if version() == 2:
        return color.color_cmd("yellow") + \
               "[+] " + \
               color.color_cmd("green") + \
               content.encode("utf8") + \
               color.color_cmd("reset")
    else:
        return bytes(
            color.color_cmd("yellow") +
            "[+] " + color.color_cmd("green") +
            content +
            color.color_cmd("reset"),
            "utf8"
        )


def info(content, log_in_file=None, mode=None,
         event=None, language=None, thread_tmp_filename=None):
    """
    build the info message, log the message in
    database if requested, rewrite the thread temporary file

    Args:
        content: content of the message
        log_in_file: log filename name
        mode: write mode, [w, w+, wb, a, ab, ...]
        event: standard event in JSON structure
        language: the language
        thread_tmp_filename: thread temporary filename

    Returns:
        None
    """
    if is_not_run_from_api():  # prevent to stdout if run from API
        if version() == 2:
            sys.stdout.write(
                color.color_cmd("yellow") +
                "[+] [{0}] ".format(now()) +
                color.color_cmd("green") +
                content.encode("utf8") +
                color.color_cmd("reset") +
                "\n"
            )
        else:
            sys.stdout.buffer.write(
                bytes(
                    color.color_cmd("yellow") +
                    "[+] [{0}] ".format(now()) +
                    color.color_cmd("green") +
                    content +
                    color.color_cmd("reset") +
                    "\n",
                    "utf8"
                )
            )
            sys.stdout.flush()

    if event:  # if an event is present log it
        from core.log import __log_into_file
        __log_into_file(log_in_file, mode, json.dumps(event))
        # if thread temporary filename present, rewrite it
        if thread_tmp_filename:
            __log_into_file(thread_tmp_filename, "w", "0")
    return


def write(content):
    """
    simple print a message

    Args:
        content: content of the message

    Returns:
        None
    """
    if is_not_run_from_api():
        if version() == 2:
            sys.stdout.write(
                content.encode("utf8")
            )
        else:
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
    if is_not_run_from_api():
        if version() == 2:
            sys.stdout.write(
                color.color_cmd("blue") +
                "[!] [{0}] ".format(now()) +
                color.color_cmd("yellow") +
                content.encode("utf8") +
                color.color_cmd("reset") +
                "\n"
            )
        else:
            sys.stdout.buffer.write(
                bytes(
                    color.color_cmd("blue") +
                    "[!] [{0}] ".format(now()) +
                    color.color_cmd("yellow") +
                    content +
                    color.color_cmd("reset") +
                    "\n",
                    "utf8")
            )
            sys.stdout.flush()
    return


def verbose_info(content, log_in_file=None, mode=None,
                 event=None, language=None, thread_tmp_filename=None):
    """
    build the info message, log the message in database
    if requested, rewrite the thread temporary file

    Args:
        content: content of the message
        log_in_file: log filename name
        mode: write mode, [w, w+, wb, a, ab, ...]
        event: standard event in JSON structure
        language: the language
        thread_tmp_filename: thread temporary filename

    Returns:
        None
    """
    if is_not_run_from_api():  # prevent to stdout if run from API
        if version() == 2:
            sys.stdout.write(
                color.color_cmd("cyan") +
                "[v] [{0}] ".format(now()) +
                color.color_cmd("grey") +
                content.encode("utf8") +
                color.color_cmd("reset") +
                "\n"
            )
        else:
            sys.stdout.buffer.write(
                bytes(
                    color.color_cmd("cyan") +
                    "[v] [{0}] ".format(now()) +
                    color.color_cmd("grey") +
                    content +
                    color.color_cmd("reset") +
                    "\n",
                    "utf8"
                )
            )
            sys.stdout.flush()

    if event:  # if an event is present log it
        from core.log import __log_into_file
        __log_into_file(log_in_file, mode, json.dumps(event))
        # if thread temporary filename present, rewrite it
        if thread_tmp_filename:
            __log_into_file(thread_tmp_filename, "w", "0")
    return


def error(content):
    """
    build the error message

    Args:
        content: content of the message

    Returns:
        the message in error structure - None
    """

    if version() == 2:
        sys.stdout.write(
            color.color_cmd("red") +
            "[X] [{0}] ".format(now()) +
            color.color_cmd("yellow") +
            content.encode("utf8") +
            color.color_cmd("reset") +
            "\n"
        )
    else:
        sys.stdout.buffer.write(
            (
                color.color_cmd("red") +
                "[X] [{0}] ".format(now()) +
                color.color_cmd("yellow") +
                content + color.color_cmd("reset") +
                "\n"
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
    if version() == 2:
        sys.stdout.write(
            content.encode("utf8")
        )
    else:
        sys.stdout.buffer.write(
            bytes(content, "utf8")
        )
        sys.stdout.flush()
    return
