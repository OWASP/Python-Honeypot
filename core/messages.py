#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
from config import user_configuration


def load_messages(language):
    languages = [language.replace(".yaml", "") for language in os.listdir("lib/messages")]
    if language is None and language not in languages:
        language = user_configuration()['language'] if user_configuration()['language'] in languages else "en_US"
    return yaml.safe_load(
        open(
            "lib/messages/{language}.yaml".format(language=language),
            encoding="utf-8"
        )
    )
