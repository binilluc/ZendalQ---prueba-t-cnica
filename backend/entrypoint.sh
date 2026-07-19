#!/bin/sh
set -e

if [ -n "$DJANGO_DB_PATH" ]; then
  mkdir -p "$(dirname "$DJANGO_DB_PATH")"
fi

python manage.py migrate --noinput

if [ "$#" -gt 0 ]; then
  exec "$@"
else
  exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
fi
