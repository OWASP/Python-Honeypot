#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from api.utility import fix_date
from api.utility import fix_limit
from api.utility import fix_skip
from api.utility import msg_structure


class TestApiUtility(unittest.TestCase):

    def test_msg_structure_pass(self):
        self.assertEqual(
            msg_structure("ok", "Hello OWASP"),
            {
                "status": "ok",
                "msg": "Hello OWASP"
            }
        )

    def test_msg_structure_fail(self):
        self.assertNotEqual(
            msg_structure("failed", "Hello again"),
            {
                "status": "ok",
                "msg": "Hello again"
            }
        )

    def test_fix_skip_pass(self):
        returned_values = fix_skip('0')
        self.assertTrue(isinstance(returned_values, int))
        self.assertEqual(returned_values, 0)

    def test_fix_skip_fail(self):
        returned_values = fix_skip('0')
        self.assertFalse(isinstance(returned_values, str))
        self.assertNotEqual(returned_values, 1)

    def test_fix_limit_pass(self):
        returned_values = fix_limit('10')
        self.assertEqual(returned_values, 10)
        self.assertTrue(isinstance(returned_values, int))

    def test_fix_limit_fail(self):
        returned_values = fix_limit('0')
        self.assertNotEqual(returned_values, 11)
        self.assertFalse(isinstance(returned_values, str))

    def test_fix_date(self):
        self.assertListEqual(
            fix_date("02:05:2019"),
            ['02:05:2019', '02:05:2019 23:59:59']
        )
        self.assertListEqual(
            fix_date("02:05:2019 | 01:05:2019"),
            ['02:05:2019 ', ' 01:05:2019']
        )
        self.assertListEqual(
            fix_date("02/05/2019 | 01/05/2019"),
            ['02/05/2019  00:00:00', ' 01/05/2019 23:59:59']
        )
        self.assertListEqual(
            fix_date("02/05/2019"),
            ['02/05/2019 00:00:00', '02/05/2019 23:59:59']
        )
