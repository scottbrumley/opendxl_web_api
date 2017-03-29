# OpenDXL Web API Taxonomy

![Taxonomy](./images/taxonomy.jpg)

## Current Examples

### Base URL
* On local box ```http://127.0.0.1```
* Your Remote box will be defined by you ```http://mycoolhost```

### TIE "Threat Intelligence Exchange"
* Set TIE Reputation

      /tie/set

* Get TIE Reputation
      
      /tie/get

* Examples:
      
      Add either the MD5 for the file you want to find or both MD5 and SHA1 for the file.
      
      http://127.0.0.1/tie/get/md5-hash/sha1-hash
      
      

### About
* About the tool ```/about```
