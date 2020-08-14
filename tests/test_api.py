#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import requests
from core.get_modules import load_all_modules

API_URL = 'http://127.0.0.1:5000'


class TestApi(unittest.TestCase):

    def test_index(self):
        """
        Test if the API is running
        """
        response = requests.get(API_URL)
        self.assertEqual(response.status_code, 200)

    def test_count_all_events(self):
        response = requests.get(API_URL + "/api/events/count/all")
        self.assertGreaterEqual(response.json()["count"], 0)
        self.assertEqual(response.status_code, 200)

    def test_count_honeypot_events(self):
        response = requests.get(API_URL + "/api/events/count/honeypot")
        self.assertGreaterEqual(response.json()["count"], 0)
        self.assertEqual(response.status_code, 200)

    def test_count_network_events(self):
        response = requests.get(API_URL + "/api/events/count/network")
        self.assertGreaterEqual(response.json()["count"], 0)
        self.assertEqual(response.status_code, 200)

    def test_count_credential_events(self):
        response = requests.get(API_URL + "/api/events/count/credential")
        self.assertGreaterEqual(response.json()["count"], 0)
        self.assertEqual(response.status_code, 200)

    def test_count_file_events(self):
        response = requests.get(API_URL + "/api/events/count/file")
        self.assertGreaterEqual(response.json()["count"], 0)
        self.assertEqual(response.status_code, 200)

    def test_count_data_events(self):
        response = requests.get(API_URL + "/api/events/count/data")
        self.assertGreaterEqual(response.json()["count"], 0)
        self.assertEqual(response.status_code, 200)

        response = requests.get(API_URL + "/api/events/count/data?date=2020-08-14")
        self.assertGreaterEqual(response.json()["count"], 0)
        self.assertEqual(response.status_code, 200)

    def test_top_ten_honeypot_events(self):
        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/ip")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/ip?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/ip?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/ip?country=US&date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/port")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/port?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/port?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/port?country=US&date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/username")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/username?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/username?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/username?country=US&date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/password")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/password?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/password?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/password?country=US&date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/machine_name")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/machine_name?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/machine_name?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(
            API_URL + "/api/events/count/groupby/honeypot/machine_name?country=US&date=2020-08-14"
        )
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/country")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/country?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/honeypot/country?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(
            API_URL + "/api/events/count/groupby/honeypot/country?country=US&date=2020-08-14"
        )
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

    def test_top_ten_network_events(self):
        response_port = requests.get(API_URL + "/api/events/count/groupby/network/ip")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/network/ip?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/network/ip?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/network/ip?country=US&date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/network/port")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/network/port?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/network/port?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/network/port?country=US&date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/network/username")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/network/username?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/network/username?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/network/username?country=US&date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/network/password")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/network/password?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/network/password?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/network/password?country=US&date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/network/machine_name")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/network/machine_name?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/network/machine_name?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(
            API_URL + "/api/events/count/groupby/network/machine_name?country=US&date=2020-08-14"
        )
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/network/country")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/network/country?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/network/country?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(
            API_URL + "/api/events/count/groupby/network/country?country=US&date=2020-08-14"
        )
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

    def test_top_ten_credential_events(self):
        response_port = requests.get(API_URL + "/api/events/count/groupby/credential/ip")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/credential/ip?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/credential/ip?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/credential/ip?country=US&date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/credential/port")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/credential/port?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/credential/port?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/credential/port?country=US&date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/credential/username")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/credential/username?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/credential/username?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(
            API_URL + "/api/events/count/groupby/credential/username?country=US&date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/credential/password")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/credential/password?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/credential/password?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(
            API_URL + "/api/events/count/groupby/credential/password?country=US&date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/credential/machine_name")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/credential/machine_name?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/credential/machine_name?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(
            API_URL + "/api/events/count/groupby/credential/machine_name?country=US&date=2020-08-14"
        )
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/credential/country")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/credential/country?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/credential/country?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(
            API_URL + "/api/events/count/groupby/credential/country?country=US&date=2020-08-14"
        )
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

    def test_top_ten_file_events(self):
        response_port = requests.get(API_URL + "/api/events/count/groupby/file/ip")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/file/ip?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/file/ip?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/file/ip?country=US&date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/file/port")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/file/port?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/file/port?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/file/port?country=US&date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/file/username")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/file/username?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/file/username?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/file/username?country=US&date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/file/password")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/file/password?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/file/password?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/file/password?country=US&date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/file/machine_name")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/file/machine_name?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/file/machine_name?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(
            API_URL + "/api/events/count/groupby/file/machine_name?country=US&date=2020-08-14"
        )
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/file/country")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/file/country?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/file/country?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(
            API_URL + "/api/events/count/groupby/file/country?country=US&date=2020-08-14"
        )
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

    def test_top_ten_data_events(self):
        response_port = requests.get(API_URL + "/api/events/count/groupby/data/ip")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/data/ip?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/data/ip?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/data/ip?country=US&date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/data/port")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/data/port?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/data/port?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/data/port?country=US&date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/data/username")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/data/username?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/data/username?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/data/username?country=US&date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/data/password")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/data/password?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/data/password?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/data/password?country=US&date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/data/machine_name")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/data/machine_name?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/data/machine_name?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(
            API_URL + "/api/events/count/groupby/data/machine_name?country=US&date=2020-08-14"
        )
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/data/country")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/data/country?country=US")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/count/groupby/data/country?date=2020-08-14")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

        response_port = requests.get(
            API_URL + "/api/events/count/groupby/data/country?country=US&date=2020-08-14"
        )
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

    def test_honeypot_events_list(self):
        response_honeypot = requests.get(API_URL + "/api/events/explore/honeypot")
        self.assertGreaterEqual(len(response_honeypot.json()), 0)
        self.assertEqual(response_honeypot.status_code, 200)

        response_honeypot_countries = requests.get(
            API_URL + "/api/events/explore/honeypot?module_name=ssh/strong_password"
        )
        self.assertGreaterEqual(len(response_honeypot_countries.json()), 0)
        self.assertEqual(response_honeypot_countries.status_code, 200)

        response_honeypot_countries = requests.get(
            API_URL + "/api/events/explore/honeypot?date=2020-08-14"
        )
        self.assertGreaterEqual(len(response_honeypot_countries.json()), 0)
        self.assertEqual(response_honeypot_countries.status_code, 200)

        response_honeypot_machinenames = requests.get(
            API_URL + "/api/events/explore/honeypot?module_name=ssh/strong_password&date=2020-08-14"
        )
        self.assertGreaterEqual(len(response_honeypot_machinenames.json()), 0)
        self.assertEqual(response_honeypot_machinenames.status_code, 200)

    def test_network_events_list(self):
        response_network = requests.get(API_URL + "/api/events/explore/network")
        self.assertGreaterEqual(len(response_network.json()), 0)
        self.assertEqual(response_network.status_code, 200)

        response_network_countries = requests.get(
            API_URL + "/api/events/explore/network?module_name=ssh/strong_password"
        )
        self.assertGreaterEqual(len(response_network_countries.json()), 0)
        self.assertEqual(response_network_countries.status_code, 200)

        response_network_countries = requests.get(
            API_URL + "/api/events/explore/network?date=2020-08-14"
        )
        self.assertGreaterEqual(len(response_network_countries.json()), 0)
        self.assertEqual(response_network_countries.status_code, 200)

        response_network_machinenames = requests.get(
            API_URL + "/api/events/explore/network?module_name=ssh/strong_password&date=2020-08-14"
        )
        self.assertGreaterEqual(len(response_network_machinenames.json()), 0)
        self.assertEqual(response_network_machinenames.status_code, 200)

    def test_credential_events_list(self):
        response_credential = requests.get(API_URL + "/api/events/explore/credential")
        self.assertGreaterEqual(len(response_credential.json()), 0)
        self.assertEqual(response_credential.status_code, 200)

        response_credential_countries = requests.get(
            API_URL + "/api/events/explore/credential?module_name=ssh/strong_password"
        )
        self.assertGreaterEqual(len(response_credential_countries.json()), 0)
        self.assertEqual(response_credential_countries.status_code, 200)

        response_credential_countries = requests.get(
            API_URL + "/api/events/explore/credential?date=2020-08-14"
        )
        self.assertGreaterEqual(len(response_credential_countries.json()), 0)
        self.assertEqual(response_credential_countries.status_code, 200)

        response_credential_machinenames = requests.get(
            API_URL + "/api/events/explore/credential?module_name=ssh/strong_password&date=2020-08-14"
        )
        self.assertGreaterEqual(len(response_credential_machinenames.json()), 0)
        self.assertEqual(response_credential_machinenames.status_code, 200)

    def test_file_events_list(self):
        response_file = requests.get(API_URL + "/api/events/explore/file")
        self.assertGreaterEqual(len(response_file.json()), 0)
        self.assertEqual(response_file.status_code, 200)

        response_file_countries = requests.get(
            API_URL + "/api/events/explore/file?module_name=ssh/strong_password"
        )
        self.assertGreaterEqual(len(response_file_countries.json()), 0)
        self.assertEqual(response_file_countries.status_code, 200)

        response_file_countries = requests.get(
            API_URL + "/api/events/explore/file?date=2020-08-14"
        )
        self.assertGreaterEqual(len(response_file_countries.json()), 0)
        self.assertEqual(response_file_countries.status_code, 200)

        response_file_machinenames = requests.get(
            API_URL + "/api/events/explore/file?module_name=ssh/strong_password&date=2020-08-14"
        )
        self.assertGreaterEqual(len(response_file_machinenames.json()), 0)
        self.assertEqual(response_file_machinenames.status_code, 200)

    def test_data_events_list(self):
        response_data = requests.get(API_URL + "/api/events/explore/data")
        self.assertGreaterEqual(len(response_data.json()), 0)
        self.assertEqual(response_data.status_code, 200)

        response_data_countries = requests.get(
            API_URL + "/api/events/explore/data?module_name=ssh/strong_password"
        )
        self.assertGreaterEqual(len(response_data_countries.json()), 0)
        self.assertEqual(response_data_countries.status_code, 200)

        response_data_countries = requests.get(
            API_URL + "/api/events/explore/data?date=2020-08-14"
        )
        self.assertGreaterEqual(len(response_data_countries.json()), 0)
        self.assertEqual(response_data_countries.status_code, 200)

        response_data_machinenames = requests.get(
            API_URL + "/api/events/explore/data?module_name=ssh/strong_password&date=2020-08-14"
        )
        self.assertGreaterEqual(len(response_data_machinenames.json()), 0)
        self.assertEqual(response_data_machinenames.status_code, 200)

    def test_all_module_names(self):
        """
        Test module-names endpoint
        """
        module_names = load_all_modules()
        response = requests.get(API_URL + "/api/core/list/modules")
        self.assertCountEqual(module_names, response.json()["module_names"])


if __name__ == '__main__':
    unittest.main()
