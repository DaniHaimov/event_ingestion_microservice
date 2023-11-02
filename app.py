from flask import Flask, request, jsonify
import json
import pika

from events_crud import EventsDbCRUD, EventsDbCRUDInterface, EventsMockDbCRUD
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


_db_crud: EventsDbCRUDInterface
_channel = None
__msg_broker_name = os.getenv("MESSAGE_BROKER_PRODUCER_NAME")


@app.route('/api/events', methods=['POST'])
def create_event():
    event = request.json
    event_id = _db_crud.create(event)

    # Send event to RabbitMQ
    _channel.basic_publish(exchange='',
                           routing_key=__msg_broker_name,
                           body=json.dumps(event))

    res = jsonify({"status": "Event created", "event_id": event_id}), 201
    return res


@app.route('/api/events/<event_id>', methods=['GET'])
def read_event(event_id):
    record = _db_crud.read(event_id)
    if record is None:
        return jsonify({"status": "Event not found"}), 404
    return jsonify(record), 200


@app.route('/api/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    event = request.json
    record = _db_crud.update(event_id, event)
    if record is None:
        return jsonify({"status": "Event not found"}), 404
    return jsonify({"status": "Event updated", "event_id": event_id}), 200


@app.route('/api/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    record = _db_crud.delete(event_id)
    if record is None:
        return jsonify({"status": "Event not found"}), 404
    return jsonify({"status": "Event deleted", "event_id": event_id}), 200


# Add Roles
@app.route('/admin/roles', methods=['POST'])
def create_role(event_id):
    record = _db_crud.delete(event_id)
    if record is None:
        return jsonify({"status": "Event not found"}), 404
    return jsonify({"status": "Event deleted", "event_id": event_id}), 200


if __name__ == '__main__':
    # Set up DB connection
    _db_crud = EventsDbCRUD(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
    )

    # Mock database setup
    _db_crud = EventsMockDbCRUD()

    # Set up Message Broker connection
    msg_broker_host = os.getenv("MESSAGE_BROKER_PRODUCER_HOST")
    msg_broker_port = int(os.getenv("MESSAGE_BROKER_PRODUCER_PORT"))
    msg_broker_name = os.getenv("MESSAGE_BROKER_PRODUCER_NAME")

    # params = pika.URLParameters(msg_broker_host)
    rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters(host=msg_broker_host, port=msg_broker_port))
    _channel = rabbit_connection.channel()
    _channel.queue_declare(queue=msg_broker_name)

    app.run(debug=False)
