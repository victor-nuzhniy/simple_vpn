#!/bin/bash
echo "Make database migrations at startup of project."
while ! python manage.py makemigrations vpn 2>&1; do
  echo "Making migrations is in progress status"
  sleep 3
done
echo "Migrate the database at startup of project."
while ! python manage.py migrate 2>&1; do
  echo "Migration is in progress status."
  sleep 3
done
echo "Run collectstatic command."
while ! python manage.py collectstatic --noinput 2>&1; do
  echo "Collectstatic in progress."
  sleep 3
done
echo "Create superuser if it had not been created earlier."
while ! python manage.py init_create_superuser 2>&1; do
  echo "Create initial superuser, if it had not been created earlier."
  sleep 3
done
echo "Change default created site name and added second one."
while ! python manage.py init_site_operations 2>&1; do
  echo "Create initial superuser, if it had not been created earlier."
  sleep 3
done
echo "Django docker is fully configured successfully."
gunicorn -b unix:/gunicorn_socket/simple_site simple_site.wsgi --workers 3 --bind 0.0.0.0:8000 &
gunicorn -b unix:/gunicorn_socket/vpn_site vpn_site.wsgi --workers 3 --bind 0.0.0.0:8001
exec "$@"