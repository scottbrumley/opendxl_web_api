# This sample demonstrates invoking the McAfee Threat Intelligence Exchange
# (TIE) DXL service to retrieve the the reputation of files (as identified
# by their hashes)

import base64
import json, time, datetime
from threading import Thread, Event
import ConfigParser
import eventlet
eventlet.sleep()
eventlet.monkey_patch()

from dxlclient.callbacks import EventCallback, RequestCallback
from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
#from dxlclient.message import Message, Request
from dxlclient.service import ServiceRegistrationInfo

from dxltieclient import TieClient
from dxltieclient.constants import HashType, TrustLevel, FileProvider

from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from flask_socketio import SocketIO

# Import common logging and configuration
from common import *

## DXL Client Configuration
CONFIG_FILE_NAME = "./dxlclient.config"

# The topic for requesting file reputations
FILE_GET_REP_TOPIC = "/mcafee/service/tie/file/reputation"
FILE_SET_REP_TOPIC = "/mcafee/service/tie/file/reputation/set"

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE_NAME)

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

## TIE Reputation Average Map
tiescoreMap = {0:'Not Set', 1:'Known Malicious', 15: 'Most Likely Malicious', 30: 'Might Be Malicious',50: 'Unknown',70:"Might Be Trusted",85: "Most Likely Trusted", 99: "Known Trusted",100: "Known Trusted Installer"}
## TIE Provider Map
providerMap = {1:'GTI', 3:'Enterprise Reputation', 5:'ATD',7:"MWG"}

## Message String
messStr = ""

Config = ConfigParser.ConfigParser()
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

def addVendorService(idStr, nameStr, topicStr ):
    try:
        vendorsDict[idStr] = {}
        vendorsDict[idStr]['name'] = nameStr
        vendorsDict[idStr]['topic'] = topicStr
        vendorsDict[idStr]['count'] = 0
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

def readConfigSections():
    Config.read("monitor.config")
    return Config.sections()

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

vendorsSections = readConfigSections()

for vendorSect in vendorsSections:
    venId = ConfigSectionMap(vendorSect)['vendorid']
    venName = ConfigSectionMap(vendorSect)['vendorname']
    venTopic = ConfigSectionMap(vendorSect)['vendortopic']
    print "Adding " + venName + " Topic: " + venTopic
    addVendorService(venId,venName,venTopic)

##### About #####
@app.route('/about')
def about():
    myToken = ""
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
    myToken = ""
    if request.args.get('token'):
        myToken = request.args.get('token')

    if not authenticate(myToken):
        return jsonify(
            access = "access denied"
        )
    return "Path needs to be /service/action"
##### END TIE #####

def hashMe(md5,sha1,sha256):
    myHash = {}
    if md5 == None and sha1 == None and sha256 == None:
        return myHash
    else:
        ### Verify SHA1 string
        if is_sha1(sha1):
            myHash[HashType.SHA1] = sha1
        ### Verify SHA256 string
        if is_sha256(sha256):
            myHash[HashType.SHA256] = sha256
        if is_md5(md5):
            myHash[HashType.MD5] = md5
    return myHash

## Get the file reputation properties from TIE using md5 or sha1
def getTieRep(md5,sha1,sha256):
    with DxlClient(config) as client:
        # Connect to the fabric
        client.connect()

        # Create the McAfee Threat Intelligence Exchange (TIE) client
        tie_client = TieClient(client)
        myGetHashes = hashMe(md5,sha1,sha256)
        #
        # Request and display reputation for notepad.exe
        #

        reputations_dict = tie_client.get_file_reputation(myGetHashes)

            #myReturnVal = json.dumps(reputations_dict, sort_keys=True, indent=4, separators=(',', ': ')) + "\n"
    return reputations_dict

## Check if it is a SHA1
def is_sha1(maybe_sha):
    if maybe_sha == None:
        return False

    if maybe_sha == "":
        return False

    if len(maybe_sha) != 40:
        return False
    try:
        sha_int = int(maybe_sha, 16)
    except ValueError:
        return False
    return True

## Check if it is a SHA256
def is_sha256(maybe_sha):

    if maybe_sha == None:
        return False

    if maybe_sha == "":
        return False

    if len(maybe_sha) != 64:
        return False

    try:
        sha_int = int(maybe_sha, 16)
    except ValueError:
        return False
    return True

## Check if it is an MD5
def is_md5(maybe_md5):

    if maybe_md5 == None:
        return False

    if maybe_md5 == "":
        return False

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
    myToken = ""

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

        myReturnProps = getTieRep(md5,sha1,sha256)
        ### Load JSON into fileProps Dictionary
        propList = getFileProps(myReturnProps)

        if json == "true":
            return jsonify(
                myReturnProps
            )
        else:
            return render_template('reputation.html', md5=md5, sha1=sha1, sha256=sha256, propList=propList,action="getfile",json=json)

def initCharts():
    vendorList = getVendorList()

    for vendorId in vendorList:
        vendorTopic = getVendorTopic(vendorId)

        now = datetime.datetime.now()
        later = now + datetime.timedelta(seconds = 1)
        eventTime = now.strftime("%Y-%m-%d %H:%M:%S")
        startTime =  now.strftime("%Y,%m,%d,%H,%M,%S")
        endTime =  later.strftime("%Y,%m,%d,%H,%M,%S")

        #             messStr = "{'data':'Hi There'}"
        #if len(vendorsDict[vendorId]['message']) > 0:
        #    vendorsDict[vendorId]['message'] = vendorsDict[vendorId]['message'] + ', ' + '{"c":[{"v": "' + getVendorName(vendorId) + '"}, {"v": null}, {"v": "<h2>' + event.destination_topic + '</h2><br>' + eventTime + '<br>' + str(resultStr) + '"}, {"v": "Date(' + startTime + ')", "f":null}, {"v": "Date(' + endTime + ')", "f":null}]}'
        #else:

        lastMessage = vendorsDict[vendorId]['message']
        vendorsDict[vendorId]['message'] = '{"c":[{"v": "' + getVendorName(vendorId) + '"}, {"v": null}, {"v": "<h2>' + vendorTopic + '</h2><br>' + eventTime + '<br>Start"}, {"v": "Date(' + startTime + ')", "f":null}, {"v": "Date(' + endTime + ')", "f":null}]}'

        #print "Mess String: " + vendorsDict[vendorId]['message']
        ## Send JSON
        #             socketio.emit("my_response", {'data':'Hi There'} , namespace='/test')
        if (isDup(vendorTopic, lastMessage)):
            print "Dup Message Found.  Not Sending."
        else:
            # Add 1 to message Count
            vendorsDict[vendorId]['count'] = 0
            vendorCount = [vendorsDict[vendorId]['name'],     vendorsDict[vendorId]['count']]
            socketio.emit("timeline", {'data': vendorsDict[vendorId]['message']}, namespace='/test')
            socketio.emit("count", {'data': vendorCount}, namespace='/test')

def drawTimeLine(resultStr, topicStr):
    # Extract
    print "Topic: " + topicStr
    vendorId = getVendorId(topicStr)

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
    vendorsDict[vendorId]['message'] = '{"c":[{"v": "' + getVendorName(vendorId) + '"}, {"v": null}, {"v": "<h2>' + topicStr + '</h2><br>' + eventTime + '<br>' + str(resultStr) + '"}, {"v": "Date(' + startTime + ')", "f":null}, {"v": "Date(' + endTime + ')", "f":null}]}'

    #print "Mess String: " + vendorsDict[vendorId]['message']
    ## Send JSON
    #             socketio.emit("my_response", {'data':'Hi There'} , namespace='/test')
    if (isDup(topicStr, lastMessage)):
        print "Dup Message Found.  Not Sending."
    else:
        # Add 1 to message Count
        vendorsDict[vendorId]['count'] += 1
        vendorCount = [vendorsDict[vendorId]['name'],     vendorsDict[vendorId]['count']]
        socketio.emit("timeline", {'data': vendorsDict[vendorId]['message']}, namespace='/test')
        socketio.emit("count", {'data': vendorCount}, namespace='/test')

class ChgRepCallback(EventCallback):
    def on_event(self, event):
        resultStr = json.loads(event.payload.decode())
        topicStr = event.destination_topic

        drawTimeLine(resultStr,topicStr)

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

    vendorIdStr = "Test"
    topicStr = "Topic"
    resultStr = ""
    now = datetime.datetime.now()
    later = now + datetime.timedelta(minutes = 1)
    eventTime = now.strftime("%Y-%m-%d %H:%M:%S")
    startTime = now.strftime("%Y,%m,%d,%H,%M,%S")
    endTime = later.strftime("%Y,%m,%d,%H,%M,%S")

    #startMess = '{"c":[{"v": "' + vendorIdStr + '"}, {"v": null}, {"v": "<h2>' + topicStr + '</h2><br>' + eventTime + '<br>' + str(resultStr) + '"}, {"v": "Date(' + startTime + ')", "f":null}, {"v": "Date(' + endTime + ')", "f":null}]}'
    #socketio.emit("my_response", {'data': startMess} , namespace='/test')

    initCharts()

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
    # File Hashes
    #mySetHashes = {HashType.MD5: "", HashType.SHA1: "", HashType.SHA256: ""}

    trustlevelInt = getTrustLevel(trustlevelStr)

    mySetHashes = hashMe(md5,sha1,sha256)

    print "mySetHashes:"
    print mySetHashes

    # Create the client
    with DxlClient(config) as client:

        # Connect to the fabric
        client.connect()

        # Create the McAfee Threat Intelligence Exchange (TIE) client
        tie_client = TieClient(client)

        if trustlevelInt != -1:
            # Set the Enterprise reputation for notepad.exe to Known Trusted
            tie_client.set_file_reputation(
                trustlevelInt ,
                mySetHashes,
                filename=filenameStr,
                comment=commentStr
            )
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
    myToken = ""

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

### Default API
@app.route('/')
def root_path():
    myToken = ""
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
    myToken = ""
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