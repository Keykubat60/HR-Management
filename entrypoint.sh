#!/bin/sh

python manage.py makemigrations
python manage.py migrate

# Erstellen des Superusers
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

gunicorn mein_hrm.wsgi:application --bind 0.0.0.0:8000
