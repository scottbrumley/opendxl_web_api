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
from dxltieclient.constants import HashType, TrustLevel

from flask import Flask
from flask import render_template

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
tiescoreMap = {1:'Known Malicious', 15: 'Most Likely Malicious', 30: 'Might Be Malicious',50: 'Unknown',70:"Might Be Trusted",86: "Most Likely Trusted", 99: "Known Trusted"}
## TIE Provider Map
providerMap = {1:'GTI', 3:'Enterprise Reputation'}

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
    return "Path needs to be /tie/md5_hash/sha1_hash"
##### END TIE #####

### TIE API
@app.route('/tie/get/<path:md5>/<path:sha1>')
@app.route('/tie/get/<path:md5>/', defaults={'sha1': ''})
def getTieRep(md5,sha1):

    if not is_hex(md5):
        return "MD5 Value should be hex"
    if not is_hex(sha1) and not sha1 == "":
        return "SHA1 Value should be hex"

    md5_hex = md5
    sha1_hex = sha1


    ## Make sure an MD5 or SHA1 hash are given
    if (md5_hex) or (sha1_hex):
        with DxlClient(config) as client:
            # Connect to the fabric
            client.connect()
            #
            # Request and display reputation for Putty
            #
            response_dict = get_tie_file_reputation(client=client,
                                                    md5_hex= md5_hex,
                                                    sha1_hex=sha1_hex)

        ### Filename You are Checking in TIE
        filename = ""
        ### Dump Dictionary into JSON
        myReturnVal = json.dumps(response_dict, sort_keys=True, indent=4, separators=(',', ': '))
        ### Load JSON into fileProps Dictionary
        fileProps = json.loads(myReturnVal)

        print fileProps['props']
        propList = []

        for provider in fileProps['reputations']:
            propDict = {}
            providerID = int(provider['providerId'])
            trustLevel = int(provider['trustLevel'])

            print "Create Date: " + str(provider['createDate'])
            if (providerID in providerMap):
                print "Provider: " + str(providerMap[providerID])
                propDict['provider'] = str(providerMap[providerID])
            else:
                print "Provider: Not Available"
                propDict['provider'] = "Not Available"

            if (trustLevel in tiescoreMap):
                print "Reputation: " + str(tiescoreMap[trustLevel])
                propDict['reputation'] = str(tiescoreMap[trustLevel])
            else:
                print "Reputation: Not Available"
                propDict['reputation'] = "Not Available"
            print ""
            propList.append(propDict)
        return render_template('reputation.html', md5=md5, sha1=sha1, filename=filename, propList=propList, myReturnVal=myReturnVal,action="getfile")
    else:
        myReturnVal = "Sorry Nobody Home"
        return myReturnVal

@app.route('/tie/set/<path:md5>/<path:sha1>')
@app.route('/tie/set/<path:md5>/', defaults={'sha1': ''})
def setTieRep(md5,sha1):
    statusStr="Failed"
    if not is_hex(md5):
        return "MD5 Value should be hex"
    if not is_hex(sha1) and not sha1 == "":
        return "SHA1 Value should be hex"

    md5_hex = md5
    sha1_hex = sha1

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
                HashType.SHA256: "2859635FEBCC5C38470828DAAECFF49179716ADDFC5AD9FADEB89722842B381A"
            },
            filename="tzsync.exe",
            comment="Reputation set via OpenDXL")

        print TrustLevel.KNOWN_TRUSTED
        print "Succeeded."
        statusStr="Succeeded"

        myReturnVal = {"md5": "" + md5 + "", "sha1": "" + sha1 + "", "status": "" + statusStr + ""}
        json_data = json.dumps(myReturnVal)

    return render_template('reputation.html', md5=md5, sha1=sha1,action="setfile",status=statusStr, myReturnVal=json_data)

### Default API
@app.route('/')
def hello_world():
    return 'This is for authorized personnel only.  Go away!'

if __name__ == '__main__':
    app.run()