# This sample demonstrates invoking the McAfee Threat Intelligence Exchange
# (TIE) DXL service to retrieve the the reputation of files (as identified
# by their hashes)

import base64
#import logging
import os
import sys
import random
import json, time, datetime
from threading import Thread, Event
import threading
import eventlet
eventlet.monkey_patch()


from dxlclient.callbacks import EventCallback, RequestCallback
from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
from dxlclient.message import Message, Request
from dxlclient.service import ServiceRegistrationInfo

from dxltieclient import TieClient
from dxltieclient.constants import HashType, TrustLevel, FileProvider, ReputationProp, CertProvider, CertReputationProp, CertReputationOverriddenProp

from flask import Flask
from flask import render_template
from flask import jsonify
from flask import stream_with_context, request, Response
from flask_socketio import SocketIO, emit

# Import common logging and configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from common import *

# Enable logging, this will also direct built-in DXL log messages.
# See - https://docs.python.org/2/howto/logging-cookbook.html
#log_formatter = logging.Formatter('%(asctime)s %(name)s - %(levelname)s - %(message)s')

#console_handler = logging.StreamHandler()
#console_handler.setFormatter(log_formatter)

#logger = logging.getLogger()
#logger.addHandler(console_handler)
#logger.setLevel(logging.INFO)

## DXL Client Configuration
CONFIG_FILE_NAME = "./dxlclient.config"

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

## Message String
messStr = ""

## Vendors Topic Dictionary
vendorsDict = {}

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

## Start Web API
app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet")
thread = Thread()
thread_stop_event = Event()

##### About #####
@app.route('/about')
def about():
    if request.args.get('token'):
        myToken = request.args.get('token')

    if not authenticate(myToken):
        return jsonify(
            access = "access denied"
        )
    return "Web API for OpenDXL.  Written by Scott Brumley McAfee"
##### End About #####

##### TIE #####
@app.route('/tie')
def tie():
    if request.args.get('token'):
        myToken = request.args.get('token')

    if not authenticate(myToken):
        return jsonify(
            access = "access denied"
        )
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

## Get File Properties and Map with Providers and TIE Score
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

## Test for correct Authentication Token
def authenticate(token):
    if token == "27612211994137900087":
        return True
    else:
        return False

### TIE GET FILE REP with MD5 hash
@app.route('/tie/getfile/')
def getFileRep():
    json = "false"
    md5 = None
    sha1 = None
    sha256 = None
    myToken = None

    if request.args.get('md5'):
        md5 = request.args.get('md5')
    if request.args.get('sha1'):
        sha1 = request.args.get('sha1')
    if request.args.get('json'):
        json = request.args.get('json')
    if request.args.get('sha256'):
        sha256 = request.args.get('sha256')
    if request.args.get('token'):
        myToken = request.args.get('token')

    if not authenticate(myToken):
        return jsonify(
            access = "access denied"
        )

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

def addVendorService(idStr, nameStr, topicStr ):
    try:
        vendorsDict[idStr] = {}
        vendorsDict[idStr]['name'] = nameStr
        vendorsDict[idStr]['topic'] = topicStr
        vendorsDict[idStr]['message'] = ""
        return 1
    except:
        return 0

def delVendorService(idStr):
    try:
        del vendorsDict[idStr]
        return 1
    except:
        return 0

def chgVendorService(idStr, nameStr, topicStr):
    try:
        if nameStr != vendorsDict[idStr]['name']:
            vendorsDict[idStr]['name'] = nameStr
        if nameStr != vendorsDict[idStr]['topic']:
            vendorsDict[idStr]['topic'] = topicStr
        return 1
    except:
        return 0

def getVendorTopic(idStr):
    try:
        return vendorsDict[idStr]['topic']
    except:
        return ""

def getVendorName(idStr):
    try:
        return vendorsDict[idStr]['name']
    except:
        return ""

def getVendorList():
    vendorLst = []
    try:
        for vendor in vendorsDict:
            vendorLst.append(vendor)
        return vendorLst
    except:
        return []

def getVendorId(topicStr):
    try:
        for key, vendors in vendorsDict.iteritems():
            if vendors["topic"] == topicStr:
                return key
    except:
        return ""

class ChgRepCallback(EventCallback):
    def on_event(self, event):
        # Extract
        resultStr = json.loads(event.payload.decode())
        print "Topic: " + event.destination_topic
        #print resultStr
        vendorId = getVendorId(event.destination_topic)

        now = datetime.datetime.now()
        later = now + datetime.timedelta(minutes = 5)
        eventTime = now.strftime("%Y-%m-%d %H:%M:%S")
        startTime = now.strftime("%Y,%m,%d,%H,%M,%S")
        endTime = later.strftime("%Y,%m,%d,%H,%M,%S")

        #             messStr = "{'data':'Hi There'}"
        #if len(vendorsDict[vendorId]['message']) > 0:
        #    vendorsDict[vendorId]['message'] = vendorsDict[vendorId]['message'] + ', ' + '{"c":[{"v": "' + getVendorName(vendorId) + '"}, {"v": null}, {"v": "<h2>' + event.destination_topic + '</h2><br>' + eventTime + '<br>' + str(resultStr) + '"}, {"v": "Date(' + startTime + ')", "f":null}, {"v": "Date(' + endTime + ')", "f":null}]}'
        #else:

        lastMessage = vendorsDict[vendorId]['message']
        vendorsDict[vendorId]['message'] = '{"c":[{"v": "' + getVendorName(vendorId) + '"}, {"v": null}, {"v": "<h2>' + event.destination_topic + '</h2><br>' + eventTime + '<br>' + str(resultStr) + '"}, {"v": "Date(' + startTime + ')", "f":null}, {"v": "Date(' + endTime + ')", "f":null}]}'

        #print "Mess String: " + vendorsDict[vendorId]['message']
        ## Send JSON
        #             socketio.emit("my_response", {'data':'Hi There'} , namespace='/test')
        if (isDup(event.destination_topic, lastMessage)):
            print "Dup Message Found.  Not Sending."
        else:
            socketio.emit("timeline", {'data': vendorsDict[vendorId]['message']}, namespace='/test')

def isDup(topicStr, message):
    vendorId = getVendorId(topicStr)
    if (message == vendorsDict[vendorId]['message']):
        return True
    else:
        return False

class dxlWait(Thread):
    def __init__(self):
        self.delay = 1
        super(dxlWait, self).__init__()

    def getEvents(self):
        """
        Get Events off the DXL fabric
        """

        ## Create Web API request queue
        SERVICE_TYPE = "/opendxl/webapi"
        REQUEST_TOPIC = SERVICE_TYPE + "/requests"

        class MyRequestCallback(RequestCallback):
            def on_request(self, request):
                # Extract
                print "Service recieved request payload: " + request.payload.decode()

        # Create the client
        with DxlClient(config) as client:
            # Connect to the fabric
            client.connect()

            ## Register with ePO and add the request topic
            info = ServiceRegistrationInfo(client, SERVICE_TYPE)
            client.register_service_sync(info, 10)
            info.add_topic(REQUEST_TOPIC, MyRequestCallback())

            ## Get list of vendorIDs and subscribe to each topic
            vendorList = getVendorList()
            for vendor in vendorList:
                client.add_event_callback(vendorsDict[vendor]['topic'], ChgRepCallback())

            ## Listent to Events
            print "Listening for Events"
            while not thread_stop_event.isSet():
                time.sleep(self.delay)

    def run(self):
        self.getEvents()

### Route for dxl
@app.route('/dxl/')
def dxlMessages():
    return render_template('messages.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    print('Client connected')

    addVendorService('mcafeetie','McAfee TIE','/mcafee/event/tie/file/repchange/broadcast')
    addVendorService('mcafeeepo','McAfee ePO','/mcafee/event/epo/dxl/compinfo/response')
    addVendorService('mcafeemar','McAfee MAR','/mcafee/mar/agent/query/all')
    addVendorService('arubacp','Aruba ClearPass','/aruba/event/clearpass/log')
    addVendorService('checkpointfw','Check Point Firewall','/checkpoint/event/detection')
    addVendorService('scotto','Cool Queue','/scottbrumley/sample/basicevent')

    vendorIdStr = "Test"
    topicStr = "Topic"
    resultStr = ""
    now = datetime.datetime.now()
    later = now + datetime.timedelta(minutes = 1)
    eventTime = now.strftime("%Y-%m-%d %H:%M:%S")
    startTime = now.strftime("%Y,%m,%d,%H,%M,%S")
    endTime = later.strftime("%Y,%m,%d,%H,%M,%S")

    startMess = '{"c":[{"v": "' + vendorIdStr + '"}, {"v": null}, {"v": "<h2>' + topicStr + '</h2><br>' + eventTime + '<br>' + str(resultStr) + '"}, {"v": "Date(' + startTime + ')", "f":null}, {"v": "Date(' + endTime + ')", "f":null}]}'
    #socketio.emit("my_response", {'data': startMess} , namespace='/test')

    if not thread.isAlive():
        print "Starting Thread"
        thread = dxlWait()
        thread.start()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

## Convert from FireEye Severity to McAfee Reputation
def fireeyeToMcAfee(sevStr):
    trustlevelStr = "most_likely_trusted"
    if sevStr == "majr":
        trustlevelStr = "known_malicious"

    if sevStr == "unkn":
        trustlevelStr = "unknown"

    if sevStr == "minr":
        trustlevelStr = "might_be_malicious"

    if sevStr == "crit":
        trustlevelStr = "known_malicious"
    return trustlevelStr

## Map McAfee Trust Level from trustlevel string provided
def getTrustLevel(trustlevelStr):
    trustlevelStr = trustlevelStr.lower()
    if trustlevelStr == 'known_trusted':
        return TrustLevel.KNOWN_TRUSTED
    elif trustlevelStr == 'known_trusted_install':
        return TrustLevel.KNOWN_TRUSTED_INSTALLER
    elif trustlevelStr == 'most_likely_trusted':
        return TrustLevel.MOST_LIKELY_TRUSTED
    elif trustlevelStr == 'might_be_trusted':
        return TrustLevel.MIGHT_BE_TRUSTED
    elif trustlevelStr == 'unknown':
        return TrustLevel.UNKNOWN
    elif trustlevelStr == 'might_be_malicious':
        return TrustLevel.MIGHT_BE_MALICIOUS
    elif trustlevelStr == 'most_likely_malicious':
        return TrustLevel.MOST_LIKELY_MALICIOUS
    elif trustlevelStr == 'known_malicious':
        return TrustLevel.KNOWN_MALICIOUS
    elif trustlevelStr == 'not_set':
        return TrustLevel.NOT_SET
    return -1

## Set the TIE reputation of a file via MD5, SHA1, or SHA256 hash
def setReputation(trustlevelStr, md5, sha1, sha256, filenameStr, commentStr):
    trustlevelInt = getTrustLevel(trustlevelStr)

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

        if trustlevelInt != -1:
            # Set the Enterprise reputation for notepad.exe to Known Trusted
            tie_client.set_file_reputation(
                trustlevelInt , {
                    HashType.MD5: md5,
                    HashType.SHA1: sha1,
                    HashType.SHA256: sha256
                },
                filename=filenameStr,
                comment=commentStr)
        else:
            return jsonify(
                error = "invalid trust level",
                trustlevel = trustlevelStr
            )

### TIE SET FILE REP
@app.route('/tie/setfile/', methods = ['GET', 'POST'])
def setTieRep():
    if request.method == 'GET':
        json = "false"
        md5 = ""
        sha1 = ""
        sha256 = ""
        filenameStr = ""
        trustLevelStr = ""
        myToken = ""
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
        if request.args.get('trustlevel'):
            trustLevelStr = request.args.get('trustlevel')

        if request.args.get('token'):
            myToken = request.args.get('token')

        if not authenticate(myToken):
            return jsonify(
                access = "access denied"
            )

        setReputation(trustLevelStr, md5, sha1, sha256, filenameStr, commentStr)

        if json == "true":
            return jsonify(
                status=trustLevelStr
            )
        else:
            return render_template('reputation.html', md5=md5, sha1=sha1, sha256=sha256, status=trustLevelStr, filename=filenameStr, comment=commentStr, action="setfile",json=json)
    if request.method == 'POST':
        data = request.form

### FIREEYE TIE SET FILE REP
@app.route('/tie/fireeye/setfile/<myToken>', methods = ['GET','POST'])
def setFireEyeTieRep(myToken):
    md5 = ""
    sha1 = ""
    sha256 = ""
    commentStr = "Reputation set from FireEye via OpenDXL"
    filenameStr = ""
    severityStr = "unkn"

    if not authenticate(myToken):
        return jsonify(
            access = "access denied"
        )

    content = request.json
    print content

    severityStr = content['alert']['severity']
    print "Severity = " + severityStr

    ## check for malware detection and malware fields.  If they exist get md5 if it exists
    if 'malware-detected' in content['alert']['explanation']:
        if 'malware' in content['alert']['explanation']['malware-detected']:
            ## Get md5 hash from FireEye and FileName
            if 'md5sum' in content['alert']['explanation']['malware-detected']['malware']:
                md5 = content['alert']['explanation']['malware-detected']['malware']['md5sum']
                print "md5 hash = " + md5
            else:
                return jsonify(
                    error="md5sum field not present in JSON"
                )

            ## If there is a filename and extention then get it
            ## Get FileName from FireEye
            if 'type' in content['alert']['explanation']['malware-detected']['malware'] and 'name' in content['alert']['explanation']['malware-detected']['malware']:
                filenameStr = content['alert']['explanation']['malware-detected']['malware']['name'] + "." + content['alert']['explanation']['malware-detected']['malware']['type']
                print "Filename = " + filenameStr
        else:
            return jsonify(
                error="malware field not present in JSON"
            )

    else:
        return jsonify(
            error="malware-detected field not present in JSON"
        )

    ## Check to make sure this is a valid md5 hash
    if md5 != "":
        if not is_md5(md5):
            return jsonify(
                error= "invalid md5"
            )

        trustlevelStr = fireeyeToMcAfee(severityStr)

        ## Set the Reputation in TIE
        setReputation(trustlevelStr, md5, sha1, sha256, filenameStr, commentStr)
    return jsonify(request.json)

### Get ePO System Information
@app.route('/epo/getsystem/')
def getSystem():
    # The ePO unique identifier
    EPO_UNIQUE_ID = None

    # The search text
    if request.args.get('query'):
        SEARCH_TEXT = request.args.get('query')
    if request.args.get('token'):
        myToken = request.args.get('token')

    if not authenticate(myToken):
        return jsonify(
            access = "access denied"
        )

    # Create the client
    with DxlClient(config) as client:

        # Connect to the fabric
        client.connect()

        # Create the ePO client
        epo_client = EpoClient(client, EPO_UNIQUE_ID)

        # Run the system find command
        res = epo_client.run_command("system.find",
                                     {"searchText": SEARCH_TEXT},
                                     output_format=OutputFormat.JSON)

        # Load find result into dictionary
        res_dict = json.loads(res, encoding='utf-8')

        # Display the results
        return json.dumps(res_dict, sort_keys=True, indent=4, separators=(',', ': '))

@app.route('/mar/getclients/')
def getMARClients():

    if request.args.get('token'):
        myToken = request.args.get('token')

    if not authenticate(myToken):
        return jsonify(
            access = "access denied"
        )

    ### Create the client
    with DxlClient(config) as client:

        # Connect to the fabric
        client.connect()

        # Create the McAfee Active Response (MAR) client
        mar_client = MarClient(client)

        # Performs the search
        result_context = \
            mar_client.search(
                projections=[{
                    "name": "HostInfo",
                    "outputs": ["ip_address","os","hostname"]
                }]
            )

        # Loop and display the results
        if result_context.has_results:
            search_result = result_context.get_results(limit=10)
            print "Results:"
            for item in search_result["items"]:
                print "    " + item["output"]['HostInfo|ip_address']
    return jsonify(search_result["items"])

### Default API
@app.route('/')
def root_path():
    if request.args.get('token'):
        myToken = request.args.get('token')

    if not authenticate(myToken):
        return jsonify(
            access = "access denied"
        )
    return 'This is for authorized personnel only.  Go away!'

### Test Page
@app.route('/ping')
def ping():
    if request.args.get('token'):
        myToken = request.args.get('token')

    if not authenticate(myToken):
        return jsonify(
            access = "access denied"
        )
    return 'pong'

if __name__ == '__main__':
    #app.run(debug=True, port=5000, host='0.0.0.0')
    socketio.run(app)
    #app.run()