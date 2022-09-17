#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from config import sentry_configuration
from core.load import load_honeypot_engine
import sentry_sdk

if __name__ == "__main__":
    config = sentry_configuration()
    if config["sentry_monitoring"]:
        sentry_sdk.init(
            dsn=config["sentry_dsn_url"],
            traces_sample_rate=config["sentry_trace_rate"],
        )
    sys.exit(0 if load_honeypot_engine() is True else 1)
