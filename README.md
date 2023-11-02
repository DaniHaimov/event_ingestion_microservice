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
3. [Deploy PostgreSQL](README.md#deploy-postgresql)
4. [Deploy RabbitMQ](README.md#deploy-rabbitmq) (Should be deployed by the `alerts_notifications_microservice`)


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
* `POST` /api/events: Create a new event.
* `GET` /api/events/<event_id>: Retrieve an event by ID.
* `PUT` /api/events/<event_id>: Update an existing event by ID.
* `DELETE` /api/events/<event_id>: Delete an event by ID.
* `POST` /admin/rules: Create a new rule.

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

## Deploy RabbitMQ
### Local Install
```bash

```
  
### Container Deploy
```bash
docker pull rabbitmq
docker run -d --name rabbitmq_name -p listen_port:5672 -p manage_listen_port:15672 rabbitmq:latest
```