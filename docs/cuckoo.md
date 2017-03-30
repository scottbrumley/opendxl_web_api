# Cuckoo Configuration

Modify the **cuckoo/conf/reporting.conf**
```
[notification]
   # Notification module to inform external systems that analysis is finished.
   # You should consider keeping this as very last reporting module.
   enabled = no
    
   # External service URL where info will be POSTed.
   # example : https://my.example.host/some/destination/url
   url = http://opendxl.webservice.com/tie/set/
    
   # Cuckoo host identifier - can be hostname.
   # for example : my.cuckoo.host
   identifier =
   ```
   
