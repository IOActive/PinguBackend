#!/bin/bash

set -e

echo "Starting bootstrap process..."

# Get the absolute path of the script's directory
SCRIPT_DIR=$(dirname "$(realpath "$0")")


# Step 1: Bootstrap the database
echo "Bootstrapping the database..."
python $SCRIPT_DIR/bootstrap_db.py

# Step 2: Setup message queues
echo "Setting up message queues..."
python $SCRIPT_DIR/bootstrap_queues.py

# Step 3: Create Django admin user
echo "Creating Django admin user..."
python $SCRIPT_DIR/create_admin_user.py

# Step 4: Load initial data
echo "Loading initial data..."
python $SCRIPT_DIR/load_initial_data.py

echo "Bootstrap process completed successfully."
