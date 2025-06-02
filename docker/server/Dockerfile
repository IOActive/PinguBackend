FROM python:3.14-rc-slim

WORKDIR /pinguBackend

# Install dependencies for compiling some Python packages
RUN apt update && apt install -y libpq-dev build-essential libffi-dev libmagic1

# Copy only the requirements.txt first and install dependencies
COPY requirements.txt /pinguBackend/
RUN pip install -r requirements.txt

# Now copy the application files (this is where changes will happen most often)
COPY ./src/ /pinguBackend/src/
COPY ./manage.py /pinguBackend/manage.py
COPY ./celery_runner.sh /pinguBackend/celery_runner.sh
COPY ./default_yml_configs/ /pinguBackend/default_yml_configs/

# Copy the bootstrap script last (less likely to change)
COPY ./src/bootstrap/ /pinguBackend/src/bootstrap/

# Copy the server entrypoint script last (should be relatively stable)
COPY docker/server/server_entrypoint.sh /pinguBackend/server_entrypoint.sh
RUN chmod +x /pinguBackend/server_entrypoint.sh

# Copy the bootstrap script last (if it changes infrequently)
RUN chmod +x /pinguBackend/src/bootstrap/bootstrap.sh

# Set the entrypoint for the server
ENTRYPOINT ["/pinguBackend/server_entrypoint.sh"]
