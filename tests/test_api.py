#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

import requests

from database.connector import (honeypot_events, network_events,
                                honeypot_events_queue,
                                insert_to_honeypot_events_queue,
                                insert_to_network_events_queue,
                                network_events_queue,
                                push_events_queues_to_database)
from database.datatypes import HoneypotEvent, NetworkEvent

API_URL = 'http://127.0.0.1:5000'


class TestApi(unittest.TestCase):
  

    def test_index(self):
        """
        Test if the API is running
        """
        response = requests.get(API_URL)
        self.assertEqual(response.status_code, 200)


    def test_count_all_events(self):
        """
        Test count_all_events end-point of the API returns a value 
        greater than or equal to zero.
        """
        response = requests.get(API_URL + "/api/events/count-all-events")
        self.assertGreaterEqual(response.json()["count_all_events"], 0)
        self.assertEqual(response.status_code, 200)

    
    def test_count_honeypot_events(self):
        """
        Test count_honeypot_events end-point of the API returns a value 
        greater than or equal to zero.
        """
        response = requests.get(API_URL + "/api/events/count-honeypot-events")
        self.assertGreaterEqual(response.json()["count_honeypot_events"], 0)
        self.assertEqual(response.status_code, 200)


    def test_count_network_events(self):
        """
        Test count_network_events end-point of the API returns a value 
        greater than or equal to zero.
        """
        response = requests.get(API_URL + "/api/events/count-network-events")
        self.assertGreaterEqual(response.json()["count_network_events"], 0)
        self.assertEqual(response.status_code, 200)


    def test_top_ten_honeypot_events(self):
        """
        Test if honeypot-events-ips and honeypot-events-ports end-points
        returns lists.
        """
        response_ip = requests.get(API_URL + "/api/events/honeypot-events-ips")
        self.assertGreaterEqual(len(response_ip.json()), 0)
        self.assertEqual(response_ip.status_code, 200)
        
        response_port = requests.get(API_URL + "/api/events/honeypot-events-ports")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)


    def test_top_ten_network_events(self):
        """
        Test if network-events-ips and network-events-ports end-points
        returns lists.
        """
        response_ip = requests.get(API_URL + "/api/events/network-events-ips")
        self.assertGreaterEqual(len(response_ip.json()), 0)
        self.assertEqual(response_ip.status_code, 200)

        response_port = requests.get(API_URL + "/api/events/network-events-ports")
        self.assertGreaterEqual(len(response_port.json()), 0)
        self.assertEqual(response_port.status_code, 200)

    
    def test_honeypot_events_list(self):
        """
        Test if honeypot-events, honeypot-events-countries,
        honeypot-events-machinenames end-points returns lists.
        """
        response_honeypot = \
            requests.get(API_URL + "/api/events/honeypot-events")
        self.assertGreaterEqual(len(response_honeypot.json()), 0)
        self.assertEqual(response_honeypot.status_code, 200)

        response_honeypot_countries = \
            requests.get(API_URL + "/api/events/honeypot-events-countries")
        self.assertGreaterEqual(len(response_honeypot_countries.json()), 0)
        self.assertEqual(response_honeypot_countries.status_code, 200)

        response_honeypot_machinenames = \
            requests.get(API_URL + "/api/events/honeypot-events-machinenames")
        self.assertGreaterEqual(len(response_honeypot_machinenames.json()), 0)
        self.assertEqual(response_honeypot_machinenames.status_code, 200)


    def test_network_events_list(self):
        """
        Test if network-events, network-events-countries,
        network-events-machinenames end-points returns lists.
        """
        response_network = \
                requests.get(API_URL + "/api/events/network-events")
        self.assertGreaterEqual(len(response_network.json()), 0)
        self.assertEqual(response_network.status_code, 200)

        response_network_countries = \
                requests.get(API_URL + "/api/events/network-events-countries")
        self.assertGreaterEqual(len(response_network_countries.json()), 0)
        self.assertEqual(response_network_countries.status_code, 200)

        response_network_machinenames = \
            requests.get(API_URL + "/api/events/network-events-machinenames")
        self.assertGreaterEqual(len(response_network_machinenames.json()), 0)
        self.assertEqual(response_network_machinenames.status_code, 200)


    def test_all_module_names(self):
        """
        Test module-names endpoint
        """
        module_names = ['ics/veeder_root_guardian_ast',
                        'http/basic_auth_strong_password',
                        'http/basic_auth_weak_password',
                        'ftp/strong_password',
                        'ftp/weak_password',
                        'ssh/strong_password',
                        'ssh/weak_password']
        response = requests.get(API_URL + "/api/events/module-names")
        self.assertListEqual(module_names, response.json()["module_names"])

    
    def test_credential_events(self):
        """
        Test module-events, most-usernames-used and most-passwords-used
        end-points
        """
        response_modules = \
                requests.get(API_URL + "/api/events/module-events")
        self.assertGreaterEqual(len(response_modules.json()), 0)
        self.assertEqual(response_modules.status_code, 200)

        response_usernames = \
                requests.get(API_URL + "/api/events/most-usernames-used")
        self.assertGreaterEqual(len(response_usernames.json()), 0)
        self.assertEqual(response_usernames.status_code, 200)

        response_passwords = \
            requests.get(API_URL + "/api/events/most-passwords-used")
        self.assertGreaterEqual(len(response_passwords.json()), 0)
        self.assertEqual(response_passwords.status_code, 200)


    def test_push_event_queues_to_db(self):
        """
        Test pushing events from queues to database.
        """
        honeypot_event = HoneypotEvent(
                                ip_dest="11.22.33.44",
                                port_dest=80,
                                ip_src="12.23.34.45",
                                port_src=1010,
                                module_name="http/weak_password",
                                machine_name="stockholm_server_1"
                            )
        
        network_event = NetworkEvent(
                                ip_dest="13.14.15.16",
                                port_dest=8090,
                                ip_src="22.33.44.55",
                                port_src=1100,
                                machine_name="stockholm_server_1"
                            )

        # Insert events to queues
        insert_to_honeypot_events_queue(honeypot_event)
        insert_to_network_events_queue(network_event)
        
        self.assertEqual(honeypot_events_queue[0]["ip_src"], "12.23.34.45")
        self.assertEqual(network_events_queue[0]["ip_src"], "22.33.44.55")
    
        push_events_queues_to_database()

        self.assertEqual(len(honeypot_events_queue), 0)
        self.assertEqual(len(network_events_queue), 0)

        # Delete test events from the database
        honeypot_events.delete_one(honeypot_event)
        network_events.delete_one(network_event)



        



if __name__ == '__main__':
    unittest.main()
