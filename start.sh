#!/usr/bin/env bash

echo "Running database migrations..."
python manage.py migrate --noinput || exit 1

echo "Creating superuser..."
python create_admin.py || echo "Superuser step skipped or failed"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Daphne server..."
daphne ict_ticketing.asgi:application
