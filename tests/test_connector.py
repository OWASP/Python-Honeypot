import time
import unittest
from datetime import datetime
from multiprocessing import Queue

from database import connector
from database.connector import (insert_to_credential_events_collection,
                                insert_to_events_data_collection,
                                insert_to_honeypot_events_queue,
                                insert_to_network_events_queue,
                                push_events_queues_to_database)
from database.datatypes import (CredentialEvent,
                                EventData,
                                HoneypotEvent,
                                NetworkEvent)
from api.database_queries import filter_by_fields


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
            protocol='TCP',
            module_name="http/basic_auth_weak_password",
            machine_name="stockholm_server_1"
        )

        network_event = NetworkEvent(
            ip_dest="13.14.15.16",
            port_dest=8090,
            ip_src="22.33.44.55",
            port_src=1100,
            protocol='UDP',
            machine_name="stockholm_server_1"
        )

        honeypot_events_queue = Queue()
        network_events_queue = Queue()

        # Insert events to queues
        insert_to_honeypot_events_queue(honeypot_event, honeypot_events_queue)
        insert_to_network_events_queue(network_event, network_events_queue)

        push_events_queues_to_database(honeypot_events_queue, network_events_queue)

        time.sleep(1)

        honeypot_records = connector.elasticsearch_events.search(
            index='honeypot_events',
            body=filter_by_fields('11.22.33.44', ['ip_dest'])
        )['hits']['hits']
        network_records = connector.elasticsearch_events.search(
            index='network_events',
            body=filter_by_fields('13.14.15.16', ['ip_dest'])
        )['hits']['hits']

        # Find the records in the DB
        honeypot_record = honeypot_records[0]['_source']
        network_record = network_records[0]['_source']

        self.assertGreater(len(honeypot_records), 0)
        self.assertGreater(len(network_records), 0)

        # Compare the record found in the DB with the one pushed
        self.assertEqual(honeypot_record["ip_src"], honeypot_event.ip_src)
        self.assertEqual(honeypot_record["ip_dest"], honeypot_event.ip_dest)

        self.assertEqual(network_record["ip_src"], network_event.ip_src)
        self.assertEqual(network_record["ip_dest"], network_event.ip_dest)

        # Delete test events from the database
        connector.elasticsearch_events.delete(
            index='honeypot_events',
            id=honeypot_records[0]["_id"]
        )
        connector.elasticsearch_events.delete(
            index='network_events',
            id=network_records[0]["_id"]
        )

    def test_insert_to_credential_events(self):
        """
        Test the data insertion to the credential_events collection
        """

        credential_event = CredentialEvent(
            ip_src="88.99.11.22",
            username="admin",
            password="password",
            module_name="http/basic_auth_weak_password",
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        insert_to_credential_events_collection(credential_event)
        # wait for insert
        time.sleep(1)
        # Find the records in the DB
        credential_events = connector.elasticsearch_events.search(
            index='credential_events',
            body=filter_by_fields('88.99.11.22', ['ip_src'])
        )['hits']['hits']
        credential_record = credential_events[0]['_source']

        self.assertGreater(len(credential_events), 0)

        # Compare the record found in the DB with the one pushed
        self.assertEqual(
            credential_record["ip_src"],
            credential_event.ip_src
        )

        self.assertEqual(
            credential_record["username"],
            credential_event.username
        )

        self.assertEqual(
            credential_record["password"],
            credential_event.password
        )

        # Delete test events from the database
        connector.elasticsearch_events.delete(
            index='credential_events',
            id=credential_events[0]["_id"]
        )

    def test_insert_events_data(self):
        """
        Test the data insertion to the events_data collection
        """
        event_data = EventData(
            ip="55.66.77.88",
            module_name="ics/veeder_root_guardian_ast",
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data={"content": "Test Data"}
        )

        insert_to_events_data_collection(event_data)
        # wait for insert
        time.sleep(1)

        # Find the records in the DB
        event_records = connector.elasticsearch_events.search(
            index='data_events',
            body=filter_by_fields('55.66.77.88', ['ip_src'])
        )['hits']['hits']

        self.assertGreater(len(event_records), 0)

        event_record_data = event_records[0]['_source']
        # Compare the record found in the DB with the one pushed
        self.assertEqual(event_record_data["ip_src"], event_data.ip_src)
        self.assertEqual(
            event_record_data["data"],
            event_data.data
        )
        connector.elasticsearch_events.delete(
            index='data_events',
            id=event_records[0]["_id"]
        )


if __name__ == '__main__':
    unittest.main()
