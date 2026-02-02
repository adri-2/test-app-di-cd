#!/bin/bash
set -e

# Attendre la disponibilité de la DB (simple loop)
if [ -n "$DATABASE_HOST" ]; then
  echo "Waiting for database at $DATABASE_HOST:$DATABASE_PORT..."
  RETRIES=30
  until nc -z $DATABASE_HOST $DATABASE_PORT; do
    sleep 1
    RETRIES=$((RETRIES-1))
    if [ $RETRIES -le 0 ]; then
      echo "Database did not become available in time"
      exit 1
    fi
  done
fi

# Exécuter migrations
echo "Apply database migrations..."
python manage.py migrate --noinput

# Collect static files (only si DJANGO_COLLECTSTATIC=1)
if [ "${DJANGO_COLLECTSTATIC:-0}" = "1" ]; then
  echo "Collect static files..."
  python manage.py collectstatic --noinput
fi

# Exécuter la commande fournie en CMD
exec "$@"
