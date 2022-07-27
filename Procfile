release: python manage.py migrate --noinput
web: gunicorn phone_wholesale.wsgi --log-file -
worker: REMAP_SIGTERM=SIGQUIT celery worker --app phone_wholesale --loglevel info