#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
from config import user_configuration


class load_messages:
    def __init__(self):
        self.language = user_configuration()['language'] if user_configuration()['language'] in [
            language.replace(".yaml", "") for language in os.listdir("lib/messages")
            ] else "en_US"
        self.default_messages = yaml.safe_load(
            open(
                "lib/messages/en_US.yaml".format(language=self.language),
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
        