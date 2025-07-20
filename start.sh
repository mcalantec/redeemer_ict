#!/usr/bin/env bash

echo "Applying migrations..."
python manage.py migrate

echo "Creating superuser..."
python create_admin.py

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Daphne server..."
daphne ict_ticketing.asgi:application
