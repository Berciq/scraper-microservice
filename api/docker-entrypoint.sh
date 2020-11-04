#!/bin/bash

echo "Setting up database"
python build_database.py

echo "Starting API service"
gunicorn --bind 0.0.0.0:5000 server:connex_app
