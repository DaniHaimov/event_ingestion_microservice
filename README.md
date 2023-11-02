# Event Ingestion Microservice

## Overview
This app provides a simple REST API for creating, reading, updating, and deleting events. 
It integrates with RabbitMQ as a message broker to handle event-driven operations 
and includes CRUD operations interacting with a ProgreSQL database.

## Features
- **Create Event**: POST request to `/api/events`.
- **Read Event**: GET request to `/api/events/<event_id>`.
- **Update Event**: PUT request to `/api/events/<event_id>`.
- **Delete Event**: DELETE request to `/api/events/<event_id>`.
- **Add Role**: POST request to `/admin/roles`.

## Installation
1. Clone the repository or download the application files.

## Configuration
Before running the application, configure the environment variables. Create a `.env` file in the root directory and set the following variables:
```text
DB_NAME=<your_db_name>
DB_USER=<your_db_user>
DB_PASS=<your_db_password>
DB_HOST=<your_db_host>
DB_PORT=<your_db_port>
MESSAGE_BROKER_PRODUCER_HOST=<your_broker_host>
MESSAGE_BROKER_PRODUCER_PORT=<your_broker_port>
MESSAGE_BROKER_PRODUCER_NAME=<your_broker_name>
PORT=<app_port>
```

## Running the Application
To start the application, execute:
```bash
python app.py
```
The application uses Waitress as a production-grade server to serve the Flask application. By default, it binds to 0.0.0.0 on the port defined in the .env file.

## Endpoints
The application provides endpoints for event management with JSON responses:
* **POST** /api/events: Create a new event.
* **GET** /api/events/<event_id>: Retrieve an event by ID.
* **PUT** /api/events/<event_id>: Update an existing event by ID.
* **DELETE** /api/events/<event_id>: Delete an event by ID.
* **POST** /admin/roles: Create a new role.

## Dependencies
This application requires the following Python packages:
* Flask
* pika
* psycopg2-binary
* python-dotenv
* Waitress (for production server)

Install them using pip:
```bash
pip install -r requirements.txt
```

