release: python manage.py migrate --noinput
web: gunicorn phone_wholesale.wsgi --log-file -
worker: REMAP_SIGTERM=SIGQUIT celery -A phone_wholesale worker -l info