#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import ctypes


def __die_success():
    """
    exit the framework with code 0
    """
    from core.color import finish
    finish()
    sys.exit(0)


def __die_failure(msg):
    """
    exit the framework with code 1

    Args:
        msg: the error message
    """
    from core.color import finish
    from core.alert import error
    error(msg)
    finish()
    sys.exit(1)


def terminate_thread(thread):
    """
    kill a thread https://stackoverflow.com/a/15274929

    Args:
        thread: an alive thread

    Returns:
        True
    """
    from core.alert import info
    info("killing {0}".format(thread.name))
    if not thread.isAlive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
    return True
