#!/bin/bash

echo "Setting up database"
python -m api.build_database

echo "Starting API service"
gunicorn --bind 0.0.0.0:5000 api.server:connex_app
