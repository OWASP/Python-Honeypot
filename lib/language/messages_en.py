#!/usr/bin/env python
# -*- coding: utf-8 -*-


def all_messages():
    """
    keep all messages in en

    Returns:
        all messages in JSON
    """
    return \
        {
            "honeypot_started": "OWASP Honeypot started ...",
            "available_modules": "list of available modules",
            "module_not_available": "module {0} is not available"
        }
