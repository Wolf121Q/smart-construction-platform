#!/bin/bash

source ../venv/bin/activate
gunicorn ConstructionManagementSystem.wsgi:application --bind 0.0.0.0:443 \
	--certfile Certs/dhai-r.com.pk.crt.pem \
	--keyfile Certs/dhai-r.com.pk.key.pem