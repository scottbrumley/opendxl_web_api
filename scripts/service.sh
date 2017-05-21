#!/bin/bash

if [[ -d "/vagrant" ]]; then
    ROOT_DIR="/vagrant/"
else
    ROOT_DIR="$(pwd)/"
fi

source ${ROOT_DIR}scripts/vars.sh

if [ -f ${FLASK_PID_FILE} ]; then
    echo "${FLASK_PID_FILE} exists"
    source ${FLASK_PID_FILE}
else
    touch ${FLASK_PID_FILE}
fi

function start {
    echo "Running Flask ..."
    FLASK_APP="${ROOT_DIR}/opendxl_web_api.py"
    /usr/local/bin/flask run --host=0.0.0.0 --port=${FLASK_PORT}&
    echo "FLASK PID = " + $!
    FLASK_PID=$!
    echo "FLASK_PID=${FLASK_PID}" > "${FLASK_PID_FILE}"
    sleep 5
}

function debug {
    echo "Running Flask ..."
    FLASK_APP="${ROOT_DIR}/opendxl_web_api.py"
    /usr/local/bin/flask run --host=0.0.0.0 --port=${FLASK_PORT}
    echo "FLASK PID = " + $!
    FLASK_PID=$!
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
    /${ROOT_DIR}/tests/urltests.sh
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