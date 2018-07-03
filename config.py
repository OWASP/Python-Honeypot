#!/usr/bin/env python
# -*- coding: utf-8 -*-


def docker_configuration():
    """
    docker configuration

    Returns:
        JSON/Dict docker configuration
    """
    return {
        "virtual_machine_storage_limit": 0.5,  # Gigabyte
        "virtual_machine_container_reset_factory_time": 1 * 60 * 60  # hours

    }
