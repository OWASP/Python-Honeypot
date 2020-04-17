#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime


def now(model="%Y-%m-%d %H:%M:%S"):
    """
    get now date and time
    Args:
        model:  the date and time model, default is "%Y-%m-%d %H:%M:%S"

    Returns:
        the date and time of now
    """
    return datetime.datetime.now().strftime(model)


def hours(hour_to_seconds):
    """
    integer to hour(s)
    Args:
        hour_to_seconds: hours (integer)

    Returns:
        seconds equal to hours (integer)
    """

    return int(hour_to_seconds * 60 * 60)
