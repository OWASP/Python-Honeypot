import os
import unittest
from datetime import datetime
from dataclasses import asdict

from database.connector import (credential_events, honeypot_events,
                                honeypot_events_queue, ics_honeypot_events,
                                insert_to_credential_events_collection,
                                insert_to_honeypot_events_queue,
                                insert_to_ics_honeypot_events_collection,
                                insert_to_network_events_queue, network_events,
                                network_events_queue,
                                push_events_queues_to_database)
from database.datatypes import (CredentialEvent, HoneypotEvent,
                                ICSHoneypotEvent, NetworkEvent)


class TestConnector(unittest.TestCase):

    def test_push_event_queues_to_db(self):
        """
        Test pushing Honeypot and network events from queues
        to database.
        """
        honeypot_event = HoneypotEvent(
                                ip_dest="11.22.33.44",
                                port_dest=80,
                                ip_src="12.23.34.45",
                                port_src=1010,
                                module_name="http/basic_auth_weak_password",
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

        push_events_queues_to_database()

        # Find the records in the DB
        honeypot_record = honeypot_events.find_one(honeypot_event.__dict__)
        network_record = network_events.find_one(network_event.__dict__)
        
        # Compare the record found in the DB with the one pushed
        self.assertEqual(honeypot_record["ip_src"], honeypot_event.ip_src)
        self.assertEqual(honeypot_record["ip_dest"], honeypot_event.ip_dest)

        self.assertEqual(network_record["ip_src"], network_event.ip_src)
        self.assertEqual(network_record["ip_dest"], network_event.ip_dest)

        # Delete test events from the database
        honeypot_events.delete_one(honeypot_event.__dict__)
        network_events.delete_one(network_event.__dict__)

    
    def test_insert_to_credential_events(self):
        """
        Test the data insertion to the credential_events collection
        """

        credential_event = CredentialEvent(
                                ip="88.99.11.22",
                                username="admin",
                                password="password",
                                module_name="http/basic_auth_weak_password",
                                date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            )
        
        insert_to_credential_events_collection(credential_event)

        # Find the record in the DB
        credential_record = credential_events.find_one(credential_event.__dict__)

        # Compare the record found in the DB with the one pushed
        self.assertEqual(credential_record["ip"],
                         credential_event.ip)

        self.assertEqual(credential_record["username"],
                         credential_event.username)

        self.assertEqual(credential_record["password"],
                         credential_event.password)

        # Delete test events from the database
        # credential_events.delete_one(credential_event.__dict__)


    def test_insert_ics_honeypot_events(self):
        """
        Test the data insertion to the ics_honeypot_events collection 
        """
        ics_honeypot_event = ICSHoneypotEvent(
                                ip="55.66.77.88",
                                module_name="ics/veeder_root_guardian_ast",
                                date=datetime.now(),
                                data="Test Data"
                            )

        insert_to_ics_honeypot_events_collection(ics_honeypot_event)

        # Find the record in the DB
        ics_honeypot_record = ics_honeypot_events.find_one(ics_honeypot_event.__dict__)

        # Compare the record found in the DB with the one pushed
        self.assertEqual(ics_honeypot_record["ip"], ics_honeypot_event.ip)
        self.assertEqual(ics_honeypot_record["data"],
                         ics_honeypot_event.data)
        
        ics_honeypot_events.delete_one(ics_honeypot_event.__dict__)


if __name__ == '__main__':
    unittest.main()
