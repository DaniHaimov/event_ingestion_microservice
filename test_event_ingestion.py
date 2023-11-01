import os
import unittest

import pika

import event_ingestion as service
from events_crud import EventsMockDbCRUD, EventsDbCRUD


class MockMsgBroker:
    def basic_publish(self, exchange, routing_key, body):
        print(f'{self}: {body}')


class EventIngestionTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        service.app.testing = True
        self.client = service.app.test_client()
        # self.client = http.client.HTTPConnection('localhost:5000')

        # Mock database setup
        service._db_crud = EventsMockDbCRUD()

        # service._db_crud = EventsDbCRUD(
        #     dbname=os.getenv('DB_NAME'),
        #     user=os.getenv('DB_USER'),
        #     password=os.getenv('DB_PASS'),
        #     host=os.getenv('DB_HOST'),
        #     port=os.getenv('DB_PORT'),
        #  )

        # Mock message broker setup
        service._channel = MockMsgBroker()

        # msg_broker_host = os.getenv("MESSAGE_BROKER_PRODUCER_HOST")
        # msg_broker_port = int(os.getenv("MESSAGE_BROKER_PRODUCER_PORT"))
        # msg_broker_name = os.getenv("MESSAGE_BROKER_PRODUCER_NAME")
        #
        # rabbit_connection = pika.BlockingConnection(
        #     pika.ConnectionParameters(host=msg_broker_host, port=msg_broker_port))
        # service._channel = rabbit_connection.channel()
        # service._channel.queue_declare(queue=msg_broker_name)

    def test_create_event(self):
        response = self.client.post('/api/events', json={
            'event': 'ROLE14543',
            'created_by': 'Daniel',
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Event created', response.json['status'])

    def test_get_event(self):
        # Create an event to retrieve
        create_response = self.client.post('/api/events', json={
            'event': 'get',
        })
        event_id = create_response.json['event_id']

        # Test retrieving the created event
        get_response = self.client.get(f'/api/events/{event_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json['event'], 'get')

    def test_update_event(self):
        # Create an event to update
        create_response = self.client.post('/api/events', json={
            'event': 'post'
        })
        event_id = create_response.json['event_id']

        # Test updating the event
        update_response = self.client.put(f'/api/events/{event_id}', json={
            'event': 'put'
        })
        self.assertEqual(update_response.status_code, 200)
        self.assertIn('Event updated', update_response.json['status'])

        # Verify the update
        get_response = self.client.get(f'/api/events/{event_id}')
        self.assertEqual(get_response.json['event'], 'put')

    def test_delete_event(self):
        # Create an event to delete
        create_response = self.client.post('/api/events', json={
            'event': 'delete'
        })
        event_id = create_response.json['event_id']
        # print(event_id)
        # Test deleting the event
        delete_response = self.client.delete(f'/api/events/{event_id}')
        self.assertEqual(delete_response.status_code, 200)
        self.assertIn('Event deleted', delete_response.json['status'])

        # Verify the deletion
        # get_response = self.client.get(f'/api/events/{event_id}')
        # self.assertEqual(get_response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
