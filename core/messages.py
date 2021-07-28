#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import yaml
from config import user_configuration


class load_messages:
    def __init__(self):
        self.default_messages = yaml.safe_load(
            open(
                "lib/messages/en_US.yaml",
                encoding="utf-8"
            )
        )
        self.languages_list = [
            language.split('.yaml')[0] for language in os.listdir("lib/messages") if ".yaml" in language
        ]
        if "--language" in sys.argv and sys.argv[sys.argv.index('--language') + 1] in self.languages_list:
            self.language = sys.argv[sys.argv.index('--language') + 1]
        elif user_configuration()['language'] in self.languages_list:
            self.language = user_configuration()['language']
        else:
            self.language = "en_US"
        self.message_contents = yaml.safe_load(
            open(
                "lib/messages/{language}.yaml".format(language=self.language),
                encoding="utf-8"
            )
        )
        for message in self.default_messages:
            if message not in self.message_contents:
                self.message_contents[message] = self.default_messages[message]
