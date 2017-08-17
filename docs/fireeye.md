# FireEye Configuration

##Send JSON using HTTP POST

1. Log into the FireEye appliance with an administrator account
2. Click “Settings”
3. Click “Notifications”
4. Click the “http” hyperlink
5. Make sure the "Event type" check box is selected
6. If the Global HTTP Settings are already set—leave them
7. Add HTTP Server
8. Name Your Server (i.e. OpenDXLHTTP)
9. Check Enabled
10. Uncheck Auth
11. Check SSL Enabled

**Choose JSON Concise**

### URL: http://opendxlapi:5000/tie/fireeye/setfile/your token


![fireeye configuration](images/fireeye-splunk.jpg)   

### Curl Example
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d @fireeye.json http://127.0.0.1:5000/tie/fireeye/setfile/<security token>

### Values Sent to TIE
* MD5 File Hash
* File Name of analysised file
* Comment 
* Trust Level known_malicious

### Fireeye JSON example
```
{
  "product": "MAS",
  "appliance-id": "00:00:00:00:00:00",
  "appliance": "fireeye-000000",
  "alert": {
    "src": {
      "url": "/data/share/winxp-sp3/src/41281428cd6f503f948e931d546e340c.exe"
    },
    "severity": "majr",
    "alert-url": "https://fireeye-000000/malware_analysis/analyses?maid=146658",
    "explanation": {
      "malware-detected": {
        "malware": {
          "malicious": "yes",
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
}
```
