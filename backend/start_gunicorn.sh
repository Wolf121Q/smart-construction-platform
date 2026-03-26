#!/bin/bash

source ../venv/bin/activate
gunicorn ConstructionManagementSystem.wsgi:application --bind 127.0.0.1:8000