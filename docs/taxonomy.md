# OpenDXL Web API Taxonomy

![Taxonomy](./images/taxonomy.jpg)


## Tested on AX Appliance
This has been tested using an AX & NX appliance as Malware Object Alerts

## Current Examples

### Base URL
* On local box ```http://127.0.0.1:5000```
* Your Remote box will be defined by you ```http://mycoolhost```

### TIE "Threat Intelligence Exchange"
* **Set TIE** Reputation (HTTP GET) - Sets file reputation in TIE

    ```/tie/setfile```
      
* Set TIE Reputation with **FireEye** (HTTP POST)
    
    JSON POST [See FireEye Example](fireeye.md)
    
    ```/tie/fireeye/setfile/<security token>```

* **Get TIE** Reputation (HTTP GET) - Gets file reputation from TIE

    ```/tie/getfile```   

### MAR "McAfee Active Response"
* **Get MAR Clients** - Gets a list of all end points with MAR installed

```http://127.0.0.1:5000/mar/getclients/?token=<security token>```
      
### Example URL   
http://127.0.0.1:5000/tie/getfile?sha1=D4186881780D48BF55D4D59171B115634E3C7BA6&token=<security token>

#### Values
* **token** - Security Token defined in opendxl_web_api.py as a static.  Better practice to use a solution like Vault Hashicorp
* **sha1** (at least one) - The SHA1 hash of the file analyzed
* **sha256** (at least one) - The SHA256 hash of the file analyzed
* **md5** (at least one) - The MD5 hash of the file analyzed
* **filename** (optional) - The file name of the file analyzed
* **comment** (optional) - Comment to place in ePO
* **trustlevel** - File reputation      

### About
* About the tool ```/about```
