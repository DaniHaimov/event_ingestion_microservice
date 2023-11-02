# Event Ingestion Microservice

## Introduction
This app provides a simple REST API for creating, reading, updating, and deleting events. 
It integrates with RabbitMQ as a message broker to handle event-driven operations 
and includes CRUD operations interacting with a PostgreSQL database.

## Features
- **Event CRUD REST API**
- **Docker Integration**: Designed to run within a Docker container for easy deployment.

## Installation
Before installation, ensure that Docker and Python are installed on your system.
1. Clone the repository or download the application files.
2. [Install](https://github.com/DaniHaimov/alerts_notifications_microservice) `alerts_notifications_microservice`
3. [Deploy PostgreSQL](#Deploy_PostgreSQL)
4. [Deploy RabbitMQ](#Deploy_RabbitMQ) (Should be deployed by the `alerts_notifications_microservice`)


## Configuration
Before running the application, configure the environment variables. Create a `.env` file in the root directory and set the following variables:
```text
PORT=<app_port>
DB_NAME=<your_db_name>
DB_USER=<your_db_user>
DB_PASS=<your_db_password>
DB_HOST=<your_db_host>
DB_PORT=<your_db_port>
MESSAGE_BROKER_PRODUCER_HOST=<your_broker_host>
MESSAGE_BROKER_PRODUCER_PORT=<your_broker_port>
MESSAGE_BROKER_PRODUCER_NAME=<your_broker_name>
```

## Running the Application
run `alerts_notifications_microservice` that consume to same message queue
### Running on your local machine
```bash
python app.py
```
### Running on docker
```bash
docker compose up
```

## Endpoints
The application provides endpoints for event management with JSON responses:
* `POST` /api/events: Create a new event.</br>
This endpoint is used to create a new event. 
The request must include the event details in JSON format. 
Upon successful creation, the event is also sent to RabbitMQ for handling.
    #### Request:
    ```json
    POST /api/events
    Content-Type: application/json
    {
      "event": "event content",
      "created_by": "Joe"
    }
  ```
  #### Successful Response:
    ```json
    HTTP/1.1 201 Created
    Content-Type: application/json
    {
      "event_id": "123e4567-e89b-12d3-a456-426655440000"
      "status": "Event created",
    }
  ```
* `GET` /api/events/<event_id>: Retrieve an event by ID.</br>
This endpoint retrieves the details of a specific event by its unique identifier.
    #### Request:
    ```json
    GET /api/events/123e4567-e89b-12d3-a456-426655440000
  ```
  #### Successful Response:
    ```json
    HTTP/1.1 200 OK
    Content-Type: application/json
    {
      "event_id": "123e4567-e89b-12d3-a456-426655440000",
      "event": "event content",
      "created_by": "Joe",
      "created_at": "2023-11-02T14:25:00Z"
    }
  ```
  #### Failed Response:
    ```json
    HTTP/1.1 404 Not Found
    Content-Type: application/json
    {
        "status": "Event not found"
    }
  ```
* `PUT` /api/events/<event_id>: Update an existing event by ID.</br>
This endpoint updates an existing event identified by its ID with new information provided in the request body.
    #### Request:
    ```json
    PUT /api/events/123e4567-e89b-12d3-a456-426655440000
    Content-Type: application/json
    {
      "event": "event content Updated"
    }
  ```
  #### Successful Response:
    ```json
    HTTP/1.1 200 OK
    Content-Type: application/json
    {
        "status": "Event updated",
        "event_id": "123e4567-e89b-12d3-a456-426655440000"
    }
  ```
  #### Failed Response:
    ```json
    HTTP/1.1 404 Not Found
    Content-Type: application/json
    {
        "status": "Event not found"
    }
  ```
* `DELETE` /api/events/<event_id>: Delete an event by ID.</br>
This endpoint deletes an event based on its ID.
    #### Request:
    ```json
    DELETE /api/events/123e4567-e89b-12d3-a456-426655440000
  ```
  #### Successful Response:
    ```json
    HTTP/1.1 202 Accepted
    Content-Type: application/json
    {
        "status": "Event deleted",
        "event_id": "123e4567-e89b-12d3-a456-426655440000"
    }
  ```
  #### Failed Response:
    ```json
    HTTP/1.1 404 Not Found
    Content-Type: application/json
    {
        "status": "Event not found"
    }
  ```
* `POST` /admin/rules: Create a new rule.</br>
This endpoint add a rule to `alerts_notifications_microservice`
    ```json
      Coming soon
    ```

## Dependencies
This application requires the following Python packages:
* Flask
* pika
* psycopg2-binary
* dotenv
* Waitress (for production server)

Install dependencies using `pip`:
```bash
pip install -r requirements.txt
```
<a name="Deploy_PostgreSQL"></a>
## Deploy PostgreSQL
### Local Deploy
```bash
  // Refresh the apt-get repository
  sudo apt-get update
  // Install PostgreSQL
  sudo apt-get install postgresql postgresql-contrib
  // Start the service
  sudo service postgresql start
```
  
### Container Deploy
```bash
docker pull postgres
docker run --name postgres_name -e POSTGRES_PASSWORD=postgres_pass -d postgres
```
This creates a container named `some-postgres` and assigns important environment variables before running everything in the background. Postgres requires a password to function properly, which is why that’s included. 
<br>
NOTICE: don't forget create database

<a name="Deploy_RabbitMQ"></a>
## Deploy RabbitMQ
### Local Install
```bash
  // Refresh the apt-get repository
  sudo apt-get update
  // Install RabbitMQ
  sudo apt-get install rabbitmq-server
  // Start the RabbitMQ
  sudo systemctl start rabbitmq-server
```
  
### Container Deploy
```bash
docker pull rabbitmq
docker run -d --name rabbitmq_name -p listen_port:5672 -p manage_listen_port:15672 rabbitmq:latest
```