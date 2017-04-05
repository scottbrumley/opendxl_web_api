#!/usr/bin/env bash
set -e

source /vagrant/tests/vars.sh

### Make sure Web Service Reponds with HTTP Code of 200
function test_http_code {
    TEST_NAME="HTTP CODE 200"
    echo "#### TEST: ${TEST_NAME} ####"
    echo "     Testing ${TEST_URL}/about ####"
    HTTP_CODE=$(sudo wget --spider -O - -S "${TEST_URL}/about&token=${FLASK_TOKEN}" 2>&1 | grep "HTTP/" | awk '{print $2}')
    if [[ ${HTTP_CODE} == "200" ]]; then
        echo "TEST SUCCESS: ${TEST_NAME}"
    else
        echo ""
        echo "TEST FAILED: ${TEST_NAME}"
        exit 1
    fi
}

function test_sha1 {
    TEST_NAME="SHA1 File Hash"
    echo "#### TEST: ${TEST_NAME} ####"
    echo "     Testing ${TEST_URL}/tie/getfile/?sha1=${SHA1_TEST}&json=true ####"
    WEB_CONTENT=$(sudo wget -O - "${TEST_URL}/tie/getfile/?sha1=${SHA1_TEST}&token=${FLASK_TOKEN}&json=true" 2>&1)
    if [[ ${WEB_CONTENT} == *"error"* ]]; then
        echo ""
        echo "TEST FAILED: ${TEST_NAME}"
        echo $WEB_CONTENT
        exit 1
    else
        echo "TEST SUCCESS: ${TEST_NAME}"
    fi
}

function test_sha256 {
    TEST_NAME="SHA256 File Hash"
    echo "#### TEST: ${TEST_NAME} ####"
    echo "     Testing ${TEST_URL}/tie/getfile/?sha256=${SHA256_TEST}&json=true ####"
    WEB_CONTENT=$(sudo wget -O - "${TEST_URL}/tie/getfile/?sha256=${SHA256_TEST}&token=${FLASK_TOKEN}&json=true" 2>&1)
    if [[ ${WEB_CONTENT} == *"error"* ]]; then
        echo ""
        echo "TEST FAILED: ${TEST_NAME}"
        echo $WEB_CONTENT
        exit 1
    else
        echo "TEST SUCCESS: ${TEST_NAME}"
    fi
}

function test_md5 {
    TEST_NAME="MD5 File Hash"
    echo "#### TEST: ${TEST_NAME} ####"
    echo "     Testing ${TEST_URL}/tie/getfile/?md5=${MD5_TEST}&json=true ####"
    WEB_CONTENT=$(sudo wget -O - "${TEST_URL}/tie/getfile/?md5=${MD5_TEST}&token=${FLASK_TOKEN}&json=true" 2>&1)
    if [[ ${WEB_CONTENT} == *"error"* ]]; then
        echo ""
        echo "TEST FAILED: ${TEST_NAME}"
        echo $WEB_CONTENT
        exit 1
    else
        echo "TEST SUCCESS: ${TEST_NAME}"
    fi
}

### Begin Testing ###

test_http_code
test_sha1
test_sha256
echo "All Test Successful"