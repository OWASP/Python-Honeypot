#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import yaml
from config import user_configuration


def load_messages():
    return json.dumps(
        yaml.safe_load(
            open("lib/messages/{language}.yaml".format(language=user_configuration()['language']), encoding="utf-8")
            )
        )