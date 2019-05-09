#!/bin/bash
pipenv run python3 ./vocabulary/manage.py makemigrations
pipenv run python3 ./vocabulary/manage.py runserver 0.0.0.0:8081
