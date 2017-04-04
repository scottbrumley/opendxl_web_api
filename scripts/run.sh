#!/usr/bin/env bash

FLASK_APP="/vagrant/opendxl_web_api.py"
/usr/local/bin/flask run --host=0.0.0.0&
FLASK_PID="$!"

# do other stuff
echo $FLASK_PID
sleep 5
/vagrant/tests/urltests.sh

echo "Killing Flask"
KILLRET=$(sudo kill -SIGTERM $FLASK_PID 2>&1)

