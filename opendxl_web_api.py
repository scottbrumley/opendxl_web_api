# This sample demonstrates invoking the McAfee Threat Intelligence Exchange
# (TIE) DXL service to retrieve the the reputation of files (as identified
# by their hashes)

import logging
import os
import sys
import json
import base64
import logging
import os
import sys
import json

from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
from dxlclient.message import Message, Request

from dxltieclient import TieClient
from dxltieclient.constants import HashType, TrustLevel, FileProvider, ReputationProp, CertProvider, CertReputationProp, CertReputationOverriddenProp

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

# Import common logging and configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from common import *

# Enable logging, this will also direct built-in DXL log messages.
# See - https://docs.python.org/2/howto/logging-cookbook.html
log_formatter = logging.Formatter('%(asctime)s %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

CONFIG_FILE_NAME = "/vagrant/dxlclient.config"

# The topic for requesting file reputations
FILE_GET_REP_TOPIC = "/mcafee/service/tie/file/reputation"
FILE_SET_REP_TOPIC = "/mcafee/service/tie/file/reputation/set"

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE_NAME)
CONFIG_FILE = os.path.dirname(os.path.abspath(__file__)) + "/" + CONFIG_FILE_NAME

## Test value is hex
def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False
def base64_from_hex(hexstr):
    """
    Returns the base64 string for the hex string specified

    :param hexstr: The hex string to convert to base64
    :return: The base64 value for the specified hes string
    """
    return base64.b64encode(hexstr.decode('hex'))

def get_tie_file_reputation(client, md5_hex, sha1_hex):
    """
    Returns a dictionary containing the results of a TIE file reputation request

    :param client: The DXL client
    :param md5_hex: The MD5 Hex string for the file
    :param sha1_hex: The SHA-1 Hex string for the file
    :return: A dictionary containing the results of a TIE file reputation request
    """
    # Create the request message
    req = Request(FILE_GET_REP_TOPIC)

    # Create a dictionary for the payload
    payload_dict = {
        "hashes": [
            {"type": "md5", "value": base64_from_hex(md5_hex)},
            {"type": "sha1", "value": base64_from_hex(sha1_hex)}
        ]
    }

    # Set the payload
    req.payload = json.dumps(payload_dict).encode()

    # Send the request and wait for a response (synchronous)
    res = client.sync_request(req)

    # Return a dictionary corresponding to the response payload
    if res.message_type != Message.MESSAGE_TYPE_ERROR:
        return json.loads(res.payload.decode(encoding="UTF-8"))
    else:
        raise Exception("Error: " + res.error_message + " (" + str(res.error_code) + ")")

## TIE Reputation Average Map
tiescoreMap = {0:'Not Set', 1:'Known Malicious', 15: 'Most Likely Malicious', 30: 'Might Be Malicious',50: 'Unknown',70:"Might Be Trusted",85: "Most Likely Trusted", 99: "Known Trusted",100: "Known Trusted Installer"}
## TIE Provider Map
providerMap = {1:'GTI', 3:'Enterprise Reputation', 5:'ATD',7:"MWG"}

## Start Web API

app = Flask(__name__)

##### About #####
@app.route('/about')
def about():
    return "This example takes MD5 and SHA1 file hashes via a web API and return the results from TIE over DXL.  Written by Scott Brumley Intel Security"
##### End About #####

##### TIE #####
@app.route('/tie')
def tie():
    return "Path needs to be /service/action"
##### END TIE #####

## Get the file reputation properties from TIE using md5 or sha1
def getTieRep(md5,sha1,sha256):
    with DxlClient(config) as client:
        # Connect to the fabric
        client.connect()

        # Create the McAfee Threat Intelligence Exchange (TIE) client
        tie_client = TieClient(client)

        #
        # Request and display reputation for notepad.exe
        #
        if md5:
            reputations_dict = tie_client.get_file_reputation({HashType.MD5: md5})
        if sha1:
            reputations_dict = tie_client.get_file_reputation({HashType.SHA1: sha1})
        if sha256:
            reputations_dict = tie_client.get_file_reputation({HashType.SHA256: sha256})

        #myReturnVal = json.dumps(reputations_dict, sort_keys=True, indent=4, separators=(',', ': ')) + "\n"
    return reputations_dict

## Check if it is a SHA1
def is_sha1(maybe_sha):
    if len(maybe_sha) != 40:
        return False
    try:
        sha_int = int(maybe_sha, 16)
    except ValueError:
        return False
    return True

## Check if it is a SHA256
def is_sha256(maybe_sha):
    if len(maybe_sha) != 64:
        return False
    try:
        sha_int = int(maybe_sha, 16)
    except ValueError:
        return False
    return True

## Check if it is an MD5
def is_md5(maybe_md5):
    if len(maybe_md5) != 32:
        return False
    try:
        md5_int = int(maybe_md5, 16)
    except ValueError:
        return False
    return True

def getFileProps(myReturnVal):
    fileProps = myReturnVal
    propList = []

    if FileProvider.GTI in fileProps:
        propDict = {}
        propDict['provider'] = providerMap[fileProps[FileProvider.GTI]['providerId']]
        propDict['reputation'] = tiescoreMap[fileProps[FileProvider.GTI]['trustLevel']]
        propDict['createDate'] = fileProps[FileProvider.GTI]['createDate']
        propList.append(propDict)

    if FileProvider.ENTERPRISE in fileProps:
        propDict = {}
        propDict['provider'] = providerMap[fileProps[FileProvider.ENTERPRISE]['providerId']]
        propDict['reputation'] = tiescoreMap[fileProps[FileProvider.ENTERPRISE]['trustLevel']]
        propDict['createDate'] = fileProps[FileProvider.ENTERPRISE]['createDate']
        propList.append(propDict)

    if FileProvider.ATD in fileProps:
        propDict = {}
        propDict['provider'] = providerMap[fileProps[FileProvider.ATD]['providerId']]
        propDict['reputation'] = tiescoreMap[fileProps[FileProvider.ATD]['trustLevel']]
        propDict['createDate'] = fileProps[FileProvider.ATD]['createDate']
        propList.append(propDict)

    if FileProvider.MWG in fileProps:
        propDict = {}
        propDict['provider'] = providerMap[fileProps[FileProvider.MWG]['providerId']]
        propDict['reputation'] = tiescoreMap[fileProps[FileProvider.MWG]['trustLevel']]
        propDict['createDate'] = fileProps[FileProvider.MWG]['createDate']
        propList.append(propDict)

    return propList

### TIE GET FILE REP with MD5 hash
@app.route('/tie/getfile/')
def getFileRep():
    json = "false"
    md5 = None
    sha1 = None
    sha256 = None

    if request.args.get('md5'):
        md5 = request.args.get('md5')
    if request.args.get('sha1'):
        sha1 = request.args.get('sha1')
    if request.args.get('json'):
        json = request.args.get('json')
    if request.args.get('sha256'):
        sha256 = request.args.get('sha256')

    if md5 == None and sha1 == None and sha256 == None:
        return jsonify(
            error= "no file hash"
        )
    else:
        ### Verify SHA1 string
        if sha1 != None:
            if not is_sha1(sha1):
                return jsonify(
                    error= "invalid sha1"
                )

        ### Verify SHA256 string
        if sha256 != None:
            if not is_sha256(sha256):
                return jsonify(
                    error= "invalid sha256"
                )

        if md5 != None:
            if not is_md5(md5):
                return jsonify(
                    error= "invalid md5"
                )

        myReturnProps = getTieRep(md5,sha1,sha256)
        ### Load JSON into fileProps Dictionary
        propList = getFileProps(myReturnProps)

        if json == "true":
            return jsonify(
                myReturnProps
            )
        else:
            return render_template('reputation.html', md5=md5, sha1=sha1, sha256=sha256, propList=propList,action="getfile",json=json)

### TIE SET FILE REP
@app.route('/tie/setfile/')
def setTieRep():
    json = "false"
    md5 = ""
    sha1 = ""
    sha256 = ""
    filenameStr = ""
    commentStr = "Reputation set via OpenDXL"

    if request.args.get('md5'):
        md5 = request.args.get('md5')
    if request.args.get('sha1'):
        sha1 = request.args.get('sha1')
    if request.args.get('json'):
        json = request.args.get('json')
    if request.args.get('sha256'):
        sha256 = request.args.get('sha256')
    if request.args.get('filename'):
        filenameStr = request.args.get('filename')
    if request.args.get('comment'):
        commentStr = request.args.get('comment')

    if md5 == None and sha1 == None and sha256 == None:
        return jsonify(
            error= "no file hash"
        )
    else:
        ### Verify SHA1 string
        if sha1 != "":
            if not is_sha1(sha1):
                return jsonify(
                    error= "invalid sha1"
                )

        ### Verify SHA256 string
        if sha256 != "":
            if not is_sha256(sha256):
                return jsonify(
                    error= "invalid sha256"
                )

        if md5 != "":
            if not is_md5(md5):
                return jsonify(
                    error= "invalid md5"
                )

    # Create the client
    with DxlClient(config) as client:

        # Connect to the fabric
        client.connect()

        # Create the McAfee Threat Intelligence Exchange (TIE) client
        tie_client = TieClient(client)

        # Set the Enterprise reputation for notepad.exe to Known Trusted
        tie_client.set_file_reputation(
            TrustLevel.KNOWN_TRUSTED, {
                HashType.MD5: md5,
                HashType.SHA1: sha1,
                HashType.SHA256: sha256
            },
            filename="tzsync.exe",
            comment="Reputation set via OpenDXL")

    if json == "true":
        return jsonify(
            status="Succeeded"
        )
    else:
        return render_template('reputation.html', md5=md5, sha1=sha1, sha256=sha256, action="setfile",json=json)

### Default API
@app.route('/')
def hello_world():
    return 'This is for authorized personnel only.  Go away!'

if __name__ == '__main__':
    app.run()
