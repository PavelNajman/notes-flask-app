#!/bin/bash
flask db upgrade
exec gunicorn -b 0.0.0.0 'app:create_app("production")'