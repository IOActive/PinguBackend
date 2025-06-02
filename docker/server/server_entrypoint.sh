#!/bin/bash

set -e

echo "Starting server entrypoint..."

# Fix PythonPath

export PYTHONPATH=/pinguBackend/src:$PYTHONPATH


# Wait for services using Python
echo "Checking service readiness..."
python src/scripts/wait_for_service.py

# Check if this is the first run
if [ ! -f /pinguBackend/tmp/.bootstrapped ]; then
    echo "First run detected. Running bootstrap tasks..."

    # Get the absolute path of the script's directory
    src/bootstrap/bootstrap.sh

    # Create a marker file to indicate bootstrap has been completed
    touch /pinguBackend/tmp/.bootstrapped
else
    echo "Bootstrap already completed. Skipping bootstrap tasks."
fi

# Start the server
echo "Starting Django server..."
python manage.py runserver --settings PinguBackend.settings.development
