#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from core.load import load_honeypot_engine

if __name__ == "__main__":
    load_honeypot_engine()  # load the engine
    os._exit(0)
