#!/bin/bash

FLASK_PID_FILE="/tmp/flask_pid"

export FLASK_PORT=5000   ## Configure Flask Port

if [ -f ${FLASK_PID_FILE} ]; then
    echo "${FLASK_PID_FILE} exists"
    source ${FLASK_PID_FILE}
fi

function start {
    echo "Running Flask ..."
    FLASK_APP="/vagrant/opendxl_web_api.py"
    /usr/local/bin/flask run --host=0.0.0.0 --port=${FLASK_PORT}&
    FLASK_PID="$!"
    echo "FLASK_PID=${FLASK_PID}" > "${FLASK_PID_FILE}"
    sleep 5
}
function stop {
    echo "Stopping Flask ..."
    KILLRET=$(sudo kill -SIGTERM $FLASK_PID 2>&1)
    rm -rf ${FLASK_PID_FILE}
}

function restart {
    echo "Restarting Flask ..."
    stop
    start
}

function test {
    /vagrant/tests/urltests.sh
    if [[ $? == 1 ]]; then
        stop
    fi
}

if [[ ${1} == "start" ]]; then
    start
    # Testing
    test
    echo "Flask Started"
fi

if [[ ${1} == "stop" ]]; then
    stop
    echo "Flask Stopped"
fi

if [[ ${1} == "restart" ]]; then
    restart
    echo "Flask Restarted"
fi

if [[ ${1} == "status" ]]; then
    if [ -z $FLASK_PID ]; then
        echo "Flask is stopped"
    else
        CURR_PID=$(ps -p $FLASK_PID)
        if [[ "$CURR_PID" == *${FLASK_PID}* ]]; then
            echo "Flask is running"
        fi
    fi
fi