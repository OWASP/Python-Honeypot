#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
from config import user_configuration


class load_messages:
    languages = [
        language.replace(".yaml", "") for language in os.listdir("lib/messages") if ".yaml" in language
    ]
    language = user_configuration()['language'] if user_configuration()['language'] in languages else "en_US"

    def __init__(self):
        self.default_messages = yaml.safe_load(
            open(
                "lib/messages/en_US.yaml",
                encoding="utf-8"
            )
        )
        self.message_contents = yaml.safe_load(
            open(
                "lib/messages/{language}.yaml".format(language=self.language),
                encoding="utf-8"
            )
        )
        for message in self.default_messages:
            if message not in self.message_contents:
                self.message_contents[message] = self.default_messages[message]

    def get_translations(self, lang):
        if lang is None or lang not in self.languages:
            return self.message_contents
        return yaml.safe_load(
            open(
                "lib/messages/{language}.yaml".format(language=lang),
                encoding="utf-8"
            )
        )
