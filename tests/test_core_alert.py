#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch
import sys
from core.alert import (is_not_run_from_api, info, write, warn)


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

    @staticmethod
    def test_info():
        msg_content = "Hello"
        print("this test will spit the message_content in logging format")
        info(msg_content)

    @staticmethod
    def test_write_content():
        msg_content = "Hello"
        print("this test will spit the message_content in simple format")
        write(msg_content)

    @staticmethod
    def test_warn():
        msg_content = "Error"
        print("this test will spit the message_content in warning format")
        warn(msg_content)
