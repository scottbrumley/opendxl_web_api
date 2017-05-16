#!/bin/bash

set -e

if [[ -d "/vagrant" ]]; then
    ROOT_DIR="/vagrant/"
else
    ROOT_DIR="$(pwd)/"
fi

export FLASK_PORT=5000   ## Configure Flask Port
source /${ROOT_DIR}/tests/vars.sh

function setFileRep {
    TEST_NAME="Test WannaCry"
    echo "#### TEST: ${TEST_NAME} ####"
    echo "     Testing ${TEST_URL}/tie/setfile/?sha256=${1}&token=${FLASK_TOKEN} ####"

    WEB_CONTENT=$(sudo wget -O - "${TEST_URL}/tie/setfile/?sha256=${1}&token=${FLASK_TOKEN}&comment=WannaCry&trustlevel=known_malicious$json=true" 2>&1)
    if [[ ${WEB_CONTENT} == *"error"* ]]; then
        echo ""
        echo "TEST FAILED: ${TEST_NAME}"
        echo $WEB_CONTENT
        exit 1
    else
        echo "TEST SUCCESS: ${TEST_NAME}"
    fi
}


echo "Setting Files Hashes from Wanna Cry Ransomware Attack 2017"
while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "Setting TIE Reputation: $line"
    setFileRep $line
done < "$1"

