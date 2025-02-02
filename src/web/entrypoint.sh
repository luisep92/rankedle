#!/bin/bash

echo "Creating migrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate

echo "Create super user for admin panel"
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('$DJANGO_ADMIN', 'admin@example.com', '$DJANGO_PASSWORD')" | python manage.py shell
#python manage.py createsuperuser

echo "Run webserver..."
exec "$@"
