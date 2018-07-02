#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.get_modules import load_all_modules
from core.alert import info
from core.color import finish
from core.alert import messages
from core.compatible import logo

# __check_external_modules created to check requirements before load the engine
if __name__ == "__main__":  # and __check_external_modules():
    logo()
    info(messages("en", "honeypot_started"))
    info(messages("en", "available_modules"))
    for module in load_all_modules():
        info(module)
    finish()
