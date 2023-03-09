#!/bin/bash
#python3.10 manage.py makemigrations --settings=PinguBackend.settings.docker_dev &
#python3.10 manage.py migrate --settings=PinguBackend.settings.docker_dev &
python3.10 manage.py runserver 0.0.0.0:8080 --settings=PinguBackend.settings.docker_dev
