#!/bin/bash

REQ_SSL_VER="1.0.1"
SWARM_MASTER=192.168.193.80
FLASK_PORT=5000
FLASK_PID_FILE=/tmp/flask.pid

### Docker Info
BUILD_VER="0.1.1"
LOCAL_BUILD="mcafee/opendxl-webapi:${BUILD_VER}"
REMOTE_BUILD="sbrumley/opendxl-webapi:${BUILD_VER}"


setRootDir(){
    if [[ -d "/vagrant" ]]; then
        ROOT_DIR="/vagrant/"
    else
        ROOT_DIR="$(pwd)/"
    fi
}

testVARSet() {
    if [[ -v SWARM_MASTER ]]; then
        echo SWARM Master is Here: ${SWARM_MASTER}
    fi
}

testVARSet