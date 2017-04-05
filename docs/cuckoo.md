# Cuckoo Configuration

### Modify the **cuckoo/conf/reporting.conf**
```
[notification]
   # Notification module to inform external systems that analysis is finished.
   # You should consider keeping this as very last reporting module.
   enabled = no
    
   # External service URL where info will be POSTed.
   # example : https://my.example.host/some/destination/url
   url = http://opendxl.webservice.com/tie/setfile?token=<security token>&filename=tzsync.exe&trustlevel=known_trusted&sha1=D4186881780D48BF55D4D59171B115634E3C7BA6
    
   # Cuckoo host identifier - can be hostname.
   # for example : my.cuckoo.host
   identifier =
   ```

### Example URL   
http://127.0.0.1:5000/tie/setfile/?sha1=D4186881780D48BF55D4D59171B115634E3C7BA6&token=<security token>

#### Values
* token - Security Token defined in opendxl_web_api.py as a static.  Better practice to use a solution like Vault Hashicorp
* sha1 (at least one) - The SHA1 hash of the file analyzed
* sha256 (at least one) - The SHA256 hash of the file analyzed
* md5 (at least one) - The MD5 hash of the file analyzed
* filename (optional) - The file name of the file analyzed
* comment (optional) - Comment to place in ePO
* trustlevel - File reputation