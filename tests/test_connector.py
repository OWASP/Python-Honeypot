import unittest
from datetime import datetime

from database.connector import (credential_events, events_data,
                                honeypot_events,
                                insert_to_credential_events_collection,
                                insert_to_events_data_collection,
                                insert_to_honeypot_events_queue,
                                insert_to_network_events_queue, network_events,
                                push_events_queues_to_database)
from database.datatypes import (CredentialEvent, EventData, HoneypotEvent,
                                NetworkEvent)


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
        credential_record = credential_events.find_one(
                                        credential_event.__dict__)

        # Compare the record found in the DB with the one pushed
        self.assertEqual(credential_record["ip"],
                         credential_event.ip)

        self.assertEqual(credential_record["username"],
                         credential_event.username)

        self.assertEqual(credential_record["password"],
                         credential_event.password)

        # Delete test events from the database
        # credential_events.delete_one(credential_event.__dict__)

    def test_insert_eventss_data(self):
        """
        Test the data insertion to the events_data collection
        """
        event_data = EventData(
            ip="55.66.77.88",
            module_name="ics/veeder_root_guardian_ast",
            date=datetime.now(),
            data="Test Data"
        )

        insert_to_events_data_collection(event_data)

        # Find the record in the DB
        event_record_data = events_data.find_one(event_data.__dict__)

        # Compare the record found in the DB with the one pushed
        self.assertEqual(event_record_data["ip"], event_data.ip)
        self.assertEqual(event_record_data["data"],
                         event_data.data)

        events_data.delete_one(event_data.__dict__)


if __name__ == '__main__':
    unittest.main()
