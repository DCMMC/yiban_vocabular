#!/bin/bash
# for centos7
# export PATH="$HOME/.local/bin:$PATH"
# export LD_LIBRARY_PATH=/usr/local/lib
pipenv run python3 ./vocabulary/manage.py makemigrations
pipenv run python3 ./vocabulary/manage.py runserver 0.0.0.0:8081
