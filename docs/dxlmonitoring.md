# DXL Monitoring

DXL monitoring monitors real-time communications on interesting topics using streaming.  Due to streaming no data will appear until something happens.  

## Configure Topics To Monitor
Edit monitor.config
```
[McAfeeTIE]
VendorID: mcafeetie
VendorName: McAfee TIE
VendorTopic: /mcafee/event/tie/file/repchange/broadcast

[McAfeeMAR]
VendorID: mcafeemar
VendorName: McAfee MAR
VendorTopic: /mcafee/mar/agent/query/all

[McAfeeEPO]
VendorID: mcafeeepo
VendorName: McAfee ePO
VendorTopic: /mcafee/event/epo/command/log

[ArubaCP]
VendorID: arubacp
VendorName: Aruba ClearPass
VendorTopic: /aruba/event/clearpass/log

[CheckPointFW]
VendorID: checkpointfw
VendorName: Check Point Firewall
VendorTopic: /checkpoint/event/detection
```

**VendorID:** Unique arbitrary vendor ID
**VendorName:** Name To Appear on Graphing
**VendorTopic:** Topic to monitor for messages

#### Send Test Data to Populate Graphs
**Run:** 
```
./tests/changerep.sh
```  
This will set a file reputation and change it forcing a TIE update broadcast to occur.

## Real-Time View
![Real-Time View](images/dxl-real-time.png)

## DXL Message View
![DXL Message View](images/messages.png)