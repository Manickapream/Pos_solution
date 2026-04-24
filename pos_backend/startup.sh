#!/bin/bash
# Render startup script for Django
# Runs every time the service starts

echo "🗄️ Running migrations..."
python manage.py migrate --noinput

echo "📂 Collecting static files..."
python manage.py collectstatic --noinput

echo "👤 Creating superuser (if not exists)..."
python manage.py create_superuser_auto

echo "🚀 Starting server..."
gunicorn pos_backend.wsgi:application --bind 0.0.0.0:8000 --workers 2
