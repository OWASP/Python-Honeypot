#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.color import reset_cmd_color
from core.alert import write_to_api_console


def logo():
    """
    OWASP HoneyPot Logo
    """
    write_to_api_console(open('.owasp_honeypot').read())
    reset_cmd_color()
