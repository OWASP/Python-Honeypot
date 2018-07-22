#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.compatible import generate_token


def module_configuration():
    """
    module configuration

    Returns:
        JSON/Dict module configuration
    """
    return {
        "username": "root",
        "password": generate_token(16)
    }
