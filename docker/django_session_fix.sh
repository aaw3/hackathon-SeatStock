#!/bin/bash
echo "Migrating database to fix issue..."
docker exec -it seatstock-django /home/app/webapp/seatstock_django/manage.py migrate
