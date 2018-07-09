#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core._time import hours


def docker_configuration():
    """
    docker configuration

    Returns:
        JSON/Dict docker configuration
    """
    return {
        "virtual_machine_storage_limit": 0.5,  # Gigabyte
        "virtual_machine_container_reset_factory_time": hours(1),  # hours

    }


def user_configuration():
    """
        user configuration

    Returns:
        JSON/Dict user configuration
    """
    return {
        "language": "en",
        "default_selected_modules": "ftp/weak_password,ssh/weak_password,http/basic_auth_weak_password",
        "default_excluded_modules": None,
    }
