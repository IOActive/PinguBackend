#!/bin/bash

set -e

echo "Starting MinIO entrypoint..."

# Check if .venv exists, create it if it doesn't
echo "Virtual environment already exists. Activating..."
python3 -m venv .venv
source .venv/bin/activate
pip install pyyaml

# Load configuration and export environment variables
echo "Loading configuration from config.yaml..."
eval "$(python /load_config_to_env.py --config /etc/pingu/config/minio/config.yaml)"
sleep 2

# Verify the variable (optional, for debugging)
echo "MINIO_WEB_PORT is set to: ${MINIO_WEB_PORT}"

# Start MinIO server
echo "Starting MinIO server..."
minio server /data --console-address ":${MINIO_WEB_PORT}"