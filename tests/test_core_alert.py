#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch
import sys
from core.alert import (is_not_run_from_api, messages, info, write, warn)
from lib.language.messages_en import all_messages


class TestCoreAlert(unittest.TestCase):

    def test_run_from_api(self):
        testargs = ['python3', 'ohp.py', '--start-api-server']
        with patch.object(sys, 'argv', testargs):
            returned_value = is_not_run_from_api()
            self.assertEqual(returned_value, False)

    def test_not_run_from_api(self):
        testargs = ['python3', 'ohp.py']
        with patch.object(sys, 'argv', testargs):
            returned_value = is_not_run_from_api()
            self.assertEqual(returned_value, True)

    def test_messages(self):
        help_menu_msg = messages("en", "show_help_menu")
        self.assertEqual("print this help menu", help_menu_msg)
        started_msg = messages("en", "honeypot_started")
        self.assertEqual("OWASP Honeypot started ...", started_msg)
        available_languages = messages(-1, "show_help_menu")
        self.assertEqual(['en'], available_languages)

    def test_info(self):
        msg_content = "Hello"
        print("this test will spit the message_content in logging format")
        info(msg_content)

    def test_write_content(self):
        msg_content = "Hello"
        print("this test will spit the message_content in simple format")
        write(msg_content)

    def test_warn(self):
        msg_content = "Error"
        print("this test will spit the message_content in warning format")
        warn(msg_content)
