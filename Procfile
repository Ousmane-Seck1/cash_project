release: python manage.py migrate
web: gunicorn cash_project.wsgi --log-file -
worker: celery -A cash_project worker -l info
