#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import ctypes

from core.color import reset_cmd_color


def exit_success():
    """
    exit the framework with code 0
    """
    reset_cmd_color()
    sys.exit(0)


def exit_failure(msg):
    """
    exit the framework with code 1

    Args:
        msg: the error message
    """
    # TODO : Fix the cyclic dependency later
    from core.alert import error
    error(msg)
    reset_cmd_color()
    sys.exit(1)


def terminate_thread(thread, verbose=True):
    """
    kill a thread https://stackoverflow.com/a/15274929

    Args:
        thread: an alive thread
        verbose: verbose mode/boolean

    Returns:
        True/None
    """
    from core.alert import info
    if verbose:
        info("killing {0}".format(thread.name))
    if not thread.isAlive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident),
        exc
    )
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        # if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
    return True
