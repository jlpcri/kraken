#!/bin/sh

virtualenv --no-site-packages --clear env
. /usr/local/virtualenvs/krak/bin/activate

pip install --download-cache /tmp/jenkins/pip-cache -r kraken/requirements/jenkins.txt

python manage.py test --jenkins --settings=kraken.settings.jenkins
