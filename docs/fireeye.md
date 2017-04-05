# Fireeye Configuration

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

### URL: http://opendxlapi:5000/setfile?token=<your token>


![fireeye configuration](docs/images/fireeye-splunk.jpg)   


### Fireeye JSON example
```
{"msg": "extended", "product": "Web MPS", "version":
"7.0.0.138133","appliance": "WebMPS.localdomain", "alert":
{"src": {"mac":"XX:XX:XX:XX:XX:XX", "ip": "169.250.0.1",
"host": "NA-testing.fe-notify-examples.com", "vlan": "0",
"port": "10"}, "severity": "majr", "alert- url": "https://
WebMPS.localdomain/event_stream/events_for_bot?inc_id=1",
"explanation": {"target-os": "WindowsXYZ", "protocol": "tcp",
"service": "FireEye-TestEvent EA Service", "analysis":
"replay", "cnc-services": {"cnc- service": [{"protocol":
"tcp", "port": "200", "channel": "FireEye-TestEvent Channel
1", "address": "FireEye-TestEvent.example.com"}, {"protocol":
"tcp", "port": "201", "channel": "cncs 2 channel
fields", "address": "127.0.0.100"}]}, "target-application":
"IEx123", "urls": "2", "malware- detected": {"malware":
[{"content": "lms-0/contents", "url": "compl_0_1- someurl.
x1y2z3.com", "type": "link", "name": "Suspicious.URL"},
{"content": "lms-0/contents", "url": "os-change-anomaly_0_1-
someurl.x1y2z3.com", "type":"link", "name": "Suspicious.URL"},
{"objurl": "compl_0_1-someurl.x1y2z3.com", "name": "FireEyeTestEvent-SIG"}]}},
"occurred": "2014-04-13T21:02:48Z","id":
"1", "action": "notified", "dst": {"ip": "127.0.0.20",
"mac":"XX:XX:XX:XX:XX:XX", "port": "20"}, "name": "webinfection"}}
```