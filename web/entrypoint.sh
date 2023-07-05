#!/bin/sh
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input
export DJANGO_SUPERUSER_USERNAME=root
export DJANGO_SUPERUSER_EMAIL=admin@admin.com
export DJANGO_SUPERUSER_PASSWORD=root
python manage.py createsuperuser --noinput
python manage.py runserver 0.0.0.0:8000
exec "$@"



