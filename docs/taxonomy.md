# OpenDXL Web API Taxonomy

![Taxonomy](./images/taxonomy.jpg)

## Current Examples

### Base URL
* On local box ```http://127.0.0.1```
* Your Remote box will be defined by you ```http://mycoolhost```

### TIE "Threat Intelligence Exchange"
* Set TIE Reputation

      /tie/setfile

* Get TIE Reputation
      
      /tie/getfile

* Examples:
      
      You can use the MD5, SHA1, or SHA256 hash for any file to retrieve it's reputation.
      
      http://127.0.0.1/tie/getfile?md5=hash&sha1=hash&sha256=hash
      
      

### About
* About the tool ```/about```
