import unittest

from api.utility import fix_date, fix_limit, fix_skip, msg_structure


class TestApiUtility(unittest.TestCase):

    def test_msg_structure_pass(self):
        expected_output = {"status": "ok",
                           "msg": "Hello OWASP"
                           }
        returned_values = msg_structure("ok", "Hello OWASP")
        self.assertEqual(returned_values, expected_output)

    def test_msg_structure_fail(self):
        expected_output = {"status": "ok",
                           "msg": "Hello again"
                           }
        returned_values = msg_structure("failed", "Hello again")
        self.assertNotEqual(returned_values, expected_output)

    def test_fix_skip_pass(self):
        returned_values = fix_skip('0')
        self.assertTrue(type(returned_values) is int)
        self.assertEqual(returned_values, 0)

    def test_fix_skip_fail(self):
        returned_values = fix_skip('0')
        self.assertFalse(type(returned_values) is not int)
        self.assertNotEqual(returned_values, 1)

    def test_fix_limit_pass(self):
        returned_values = fix_limit('10')
        self.assertEqual(returned_values, 10)
        self.assertTrue(type(returned_values) is int)

    def test_fix_limit_fail(self):
        returned_values = fix_limit('0')
        self.assertNotEqual(returned_values, 11)
        self.assertFalse(type(returned_values) is not int)

    def test_fix_date(self):
        returned_values = fix_date("02:05:2019")
        expected_output = ['02:05:2019', '02:05:2019 23:59:59']
        self.assertListEqual(expected_output, returned_values)

    def test_fix_date_2(self):
        returned_values = fix_date("02:05:2019 | 01:05:2019")
        expected_output = ['02:05:2019 ', ' 01:05:2019']
        self.assertListEqual(expected_output, returned_values)

    def test_fix_date_3(self):
        returned_values = fix_date("02/05/2019 | 01/05/2019")
        expected_output = ['02/05/2019  00:00:00', ' 01/05/2019 23:59:59']
        self.assertListEqual(expected_output, returned_values)

    def test_fix_date_4(self):
        returned_values = fix_date("02/05/2019")
        expected_output = ['02/05/2019 00:00:00', '02/05/2019 23:59:59']
        self.assertListEqual(expected_output, returned_values)
