#!/bin/bash
set -e

if [[ -d "/vagrant" ]]; then
    ROOT_DIR="/vagrant/"
else
    ROOT_DIR="$(pwd)/"
fi

export FLASK_PORT=5000   ## Configure Flask Port
source /${ROOT_DIR}/tests/vars.sh
source /${ROOT_DIR}/tests/changerep.sh

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

function test_sha1 {
    TEST_NAME="SHA1 File Hash"
    echo "#### TEST: ${TEST_NAME} ####"
    echo "     Testing ${TEST_URL}/tie/getfile/?sha1=${SHA1_TEST}&json=true ####"
    WEB_CONTENT=$(wget -O - "${TEST_URL}/tie/getfile/?sha1=${SHA1_TEST}&token=${FLASK_TOKEN}&json=true" 2>&1)
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
    WEB_CONTENT=$(wget -O - "${TEST_URL}/tie/getfile/?sha256=${SHA256_TEST}&token=${FLASK_TOKEN}&json=true" 2>&1)
    if [[ ${WEB_CONTENT} == *"error"* ]]; then
        echo ""
        echo "TEST FAILED: ${TEST_NAME}"
        echo $


        WEB_CONTENT
        exit 1
    else
        echo "TEST SUCCESS: ${TEST_NAME}"
    fi
}

function test_md5 {
    TEST_NAME="MD5 File Hash"
    echo "#### TEST: ${TEST_NAME} ####"
    echo "     Testing ${TEST_URL}/tie/getfile/?md5=${MD5_TEST}&json=true ####"
    WEB_CONTENT=$(wget -O - "${TEST_URL}/tie/getfile/?md5=${MD5_TEST}&token=${FLASK_TOKEN}&json=true" 2>&1)
    if [[ ${WEB_CONTENT} == *"error"* ]]; then
        echo ""
        echo "TEST FAILED: ${TEST_NAME}"
        echo $WEB_CONTENT
        exit 1
    else
        echo "TEST SUCCESS: ${TEST_NAME}"
    fi
}

testJson='{
  "product": "MAS",
  "appliance-id": "00:00:00:00:00:00",
  "appliance": "fireeye-000000",
  "alert": {
    "src": {
      "url": "/data/ma/share/winxp-sp3/src/41281428cd6f503f948e931d546e340c.exe"
    },
    "severity": "majr",
    "alert-url": "https://fireeye-85f7be/malware_analysis/analyses?maid=146658",
    "explanation": {
      "malware-detected": {
        "malware": {
          "executed-at": "2017-05-09T14:30:25Z",
          "md5sum": "41281428cd6f503f948e931d546e340c",
          "type": "exe",
          "name": "Trojan.LuminosityLink"
        }
      }
    },
    "occurred": "2017-05-09T14:30:25Z",
    "action": "notified",
    "id": "146658",
    "name": "malware-object"
  },
  "version": "7.7.5.577562",
  "msg": "concise"
}'

function test_fireEye {
    TEST_NAME="Test FireEye"
    echo "#### TEST: ${TEST_NAME} ####"
    echo "     Testing ${TEST_URL}/tie/fireeye/setfile/${MD5_TEST} ####"

    WEB_CONTENT=$(wget -O-  --header "Content-Type: application/json" --post-file /${ROOT_DIR}/tests/fireeye.json "${TEST_URL}/tie/fireeye/setfile/${FLASK_TOKEN}" 2>&1)
    if [[ ${WEB_CONTENT} == *"error"* ]]; then
        echo ""
        echo "TEST FAILED: ${TEST_NAME}"
        echo $WEB_CONTENT
        exit 1
    else
        echo "TEST SUCCESS: ${TEST_NAME}"
    fi
}

function setFileRep {
    TEST_NAME="Test WannaCry ${1}"
    echo "#### TEST: ${TEST_NAME} ####"
    echo "     Testing ${TEST_URL}/tie/setfile/?sha256=${1}&token=${FLASK_TOKEN} ####"

    WEB_CONTENT=$(wget -O - "${TEST_URL}/tie/setfile/?sha256=${1}&token=${FLASK_TOKEN}&comment=WannaCry&trustlevel=known_malicious$json=true" 2>&1)
    if [[ ${WEB_CONTENT} == *"error"* ]]; then
        echo ""
        echo "TEST FAILED: ${TEST_NAME}"
        echo $WEB_CONTENT
        exit 1
    else
        echo "TEST SUCCESS: ${TEST_NAME}"
    fi
}

function setWannaCryHashes {
    echo "Setting Files Hashes from Wanna Cry Ransomware Attack 2017"
    while IFS='' read -r line || [[ -n "$line" ]]; do
        #echo "Setting TIE Reputation: $line"
        setFileRep $line
    done < "$1"
}

### Begin Testing ###

test_http_code                      ## Test basic HTTP function and return 200 HTTP STATUS CODE
test_sha1                           ## Test Getting a SHA1 hash reputation
test_sha256                         ## Test Getting a SHA256 hash reputation
test_fireEye                        ## Test Setting FireEye Reputation in TIE
test_set unknown tzsync.exe         ## Test Setting File Reputation
test_set known_trusted tzsync.exe   ## Test Setting File Reputation
setWannaCryHashes /${ROOT_DIR}/tests/wannacryhashes.txt ## Set WanaCry File Hashes to known malicious
echo "All Test Successful"