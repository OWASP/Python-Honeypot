import unittest
from unittest.mock import patch
import sys
from core.compatible import (byte_to_str, is_verbose_mode, generate_token)


class TestCoreAlert(unittest.TestCase):

    def test_run_with_verbose_option(self):
        testargs = ['python3', 'ohp.py', '--verbose']
        with patch.object(sys, 'argv', testargs):
            returned_value = is_verbose_mode()
            self.assertEqual(returned_value, True)

    def test_run_without_verbose_option(self):
        testargs = ['python3', 'ohp.py']
        with patch.object(sys, 'argv', testargs):
            returned_value = is_verbose_mode()
            self.assertEqual(returned_value, False)

    def test_byte_to_str(self):
        content = b"hello"
        self.assertIsInstance(byte_to_str(content), str)

    def test_generate_token(self):
        self.assertEqual(len(generate_token(16)), 16)
        self.assertEqual(len(generate_token(32)), 32)
        self.assertEqual(len(generate_token(48)), 48)
        self.assertEqual(len(generate_token(1)), 1)
        self.assertEqual(len(generate_token()), 32)  # default
