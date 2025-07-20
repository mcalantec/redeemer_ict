#!/usr/bin/env bash

echo "🛠️ Applying database migrations..."
python manage.py migrate --noinput || { echo "❌ Migration failed"; exit 1; }

echo "👤 Creating superuser..."
python create_admin.py || echo "⚠️ Superuser creation skipped"

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "🚀 Starting Daphne server..."
daphne ict_ticketing.asgi:application
