#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.compatible import check_for_requirements
from core.load import load_honeypot_engine

# check_for_requirements created to check requirements before load the engine
if __name__ == "__main__" and check_for_requirements():
    load_honeypot_engine()  # load the engine
