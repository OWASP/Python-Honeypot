#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from config import module_configuration


def now(model):
    return datetime.datetime.now().strftime(model)


def I20100():
    return "".join(
        [
            "\x01\r\nI20100\r\n",
            now("%b  %d, %Y %I:%M %p"),
            "\r\n\r\n",
            module_configuration()["company_name_address"],
            "\r\n\r\n\r\n",
            "IN-TANK INVENTORY       \r\n\r\n",
            "TANK PRODUCT             VOLUME TC VOLUME   ULLAGE   HEIGHT    WATER     TEMP\r\n",
            "  1  REGULAR               1693         0     9755    18.75     0.00    76.26\r\n",
            "  2  PLUS                  1788         0     6003    25.65     0.89    74.02\r\n",
            "  3  SUPREME               1748         0     7871    21.71     0.76    75.99\r\n",
            "  4  DIESEL                2147         0     7472    25.04     0.00    75.48",
            "\r\n\r\n",
            "\x03"
        ]
    )
