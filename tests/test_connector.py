import os
import unittest

from database.connector import (honeypot_events, honeypot_events_queue,
                                insert_to_honeypot_events_queue,
                                insert_to_network_events_queue, network_events,
                                network_events_queue,
                                push_events_queues_to_database)
from database.datatypes import HoneypotEvent, NetworkEvent


class TestConnector(unittest.TestCase):

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
