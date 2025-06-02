#!/bin/bash

set -e

echo "Starting RabbitMQ entrypoint..."

export QUEUE_HOST=queue
export CELERY_BROKER_URL=amqp://queue

# Start RabbitMQ server
echo "Starting RabbitMQ server..."
exec docker-entrypoint.sh rabbitmq-server
