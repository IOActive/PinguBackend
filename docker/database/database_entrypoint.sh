#!/bin/bash

set -e

echo "Starting Database entrypoint..."

# Load configuration and set environment variables
echo "Loading configuration from config.yaml..."
python load_config_to_env.py --config /etc/pingu/config/database/config.yaml
sleep 2

export POSTGRES_HOST=database

# Start the database
echo "Starting PostgreSQL database..."
exec docker-entrypoint.sh postgres
