#!/bin/bash
# Azure startup script for Django
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn pos_backend.wsgi:application --bind 0.0.0.0:8000 --workers 2
