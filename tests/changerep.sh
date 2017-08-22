#!/bin/bash

TEST_URL="http://127.0.0.1:5000"
SHA1_TEST="D4186881780D48BF55D4D59171B115634E3C7BA6"

### Make sure Web Service Reponds with HTTP Code of 200
function test_http_code {
    TEST_NAME="HTTP CODE 200"
    echo "#### TEST: ${TEST_NAME} ####"
    echo "     Testing ${TEST_URL}/about ####"
    HTTP_CODE=$(wget --spider -O - -S "${TEST_URL}/about?token=${FLASK_TOKEN}" 2>&1 | grep "HTTP/" | awk '{print $2}')
    if [[ ${HTTP_CODE} == "200" ]]; then
        echo "TEST SUCCESS: ${TEST_NAME}"
    else
        echo ""
        echo "TEST FAILED: ${TEST_NAME}"
        exit 1
    fi
}

function test_set {
    TRUSTLEVEL=$1
    FILENAME=$2
    TEST_NAME="Set SHA1 File Hash ${TRUSTLEVEL}"
    echo "#### TEST: ${TEST_NAME} ####"
    echo "     Testing ${TEST_URL}/tie/setfile/?sha1=${SHA1_TEST}&filename=tzsync.exe&trustlevel=unknown ####"
    WEB_CONTENT=$(wget -O - "${TEST_URL}/tie/setfile/?sha1=${SHA1_TEST}&token=${FLASK_TOKEN}&filename=${FILENAME}&trustlevel=${TRUSTLEVEL}" 2>&1)
    if [[ ${WEB_CONTENT} == *"error"* ]]; then
        echo ""
        echo "TEST FAILED: ${TEST_NAME}"
        echo $WEB_CONTENT
        exit 1
    else
        echo "TEST SUCCESS: ${TEST_NAME}"
    fi
}

test_http_code
test_set unknown tzsync.exe
test_set known_trusted tzsync.exe

#http://192.168.193.80:5000/tie/setfile/?sha1=D4186881780D48BF55D4D59171B115634E3C7BA6&token=27612211994137900087&filename=tzsync.exe&trustlevel=unknown
#http://192.168.193.80:5000/tie/setfile/?sha1=D4186881780D48BF55D4D59171B115634E3C7BA6&token=27612211994137900087&filename=tzsync.exe&trustlevel=known_trusted