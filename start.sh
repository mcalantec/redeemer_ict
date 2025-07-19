#!/bin/bash

echo "Running create_admin.py..."
python create_admin.py

echo "Starting Daphne server..."
daphne ict_ticketing.asgi:application
