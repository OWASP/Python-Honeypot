#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from config import user_configuration
from logging.handlers import RotatingFileHandler

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — "
    + "%(levelname)s — %(filename)s:%(lineno)d — "
    + "%(message)s"
)
LOG_FILE = user_configuration()["events_log_file"]


def get_file_handler():
    """
    Returns file handler for the log file
    """
    file_handler = RotatingFileHandler(LOG_FILE)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    """
    Creates the logger with the logger name and returns it

    Args:
        logger_name
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # highest level
    logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate error upto parent
    logger.propagate = False

    return logger
