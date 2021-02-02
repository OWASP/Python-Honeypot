#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from core.load import load_honeypot_engine

if __name__ == "__main__":
    sys.exit(0 if load_honeypot_engine() is True else 1)
