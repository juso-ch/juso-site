#!/bin/sh
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate

if [ ! -e first_run.lock ]
then
  python manage.py loaddata site
  touch first_run.lock
fi

exec "$@"
