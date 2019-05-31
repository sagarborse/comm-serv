#!/bin/bash
echo "RUNNING"
#source .env
#pip install -r requirements.txt

python /commservice/src/manage.py makemigrations 
python  /commservice/src/manage.py migrate
cd /commservice/src
gunicorn --workers=${WORKERS} -b 0.0.0.0:${APP_PORT} --access-logfile /commservice/logs/gunicorn-access.logs --error-logfile /commservice/logs/gunicorn-errors.logs core.wsgi 
#python -u /commservice/src/manage.py runserver 0.0.0.0:8000 

