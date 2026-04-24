#!/usr/bin/env bash
# Render Build Script for Django Backend
# This runs during every deploy on Render

set -o errexit

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "📂 Collecting static files..."
python manage.py collectstatic --no-input

echo "🗄️ Running migrations..."
python manage.py migrate --no-input

echo "👤 Creating superuser (if not exists)..."
python manage.py create_superuser_auto

echo "✅ Build complete!"
