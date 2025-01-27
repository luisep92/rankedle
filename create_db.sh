#!/bin/bash

cd ./src/web/  

echo "Creating migrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate

echo "Create super user for admin panel"
python manage.py createsuperuser

echo "Run webserver..."
python manage.py runserver
