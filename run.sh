#!/bin/bash

set -e

if [ $# -ne 2 ]; then
    echo "Использование: ./run.sh <email> <password>"
    exit 1
fi

PYTHON=$(which python3 || true)
if [ -z "$PYTHON" ]; then
    echo "Python3 Не найден. Пожалуйста, установите Python3."
    exit 1
fi

if [ ! -d "venv" ]; then
    $PYTHON -m venv venv
fi

source venv/bin/activate

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "Файл requirements.txt не найден."
    exit 1
fi

python manage.py migrate

DJANGO_SUPERUSER_EMAIL=$1
DJANGO_SUPERUSER_PASSWORD=$2
DJANGO_SUPERUSER_USERNAME="admin"

python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL || true



