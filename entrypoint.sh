#!/bin/bash

# migrate database
python manage.py migrate --no-input

# collect static files
python manage.py collectstatic --no-input

# start server
python manage.py runserver 0.0.0.0:8000