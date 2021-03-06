# Prerequisites

## Configuration Information
* Change DXL Topic Authorization: TIE Server Set Enterprise Reputation (send) to include the system that will be running this client
* Change DXL Topic Authorization: Active Response Server API (receive) to include the system that will be running this client

## McAfee OpenDXL SDK

https://www.mcafee.com/us/developers/open-dxl/index.aspx

McAfee Threat Intelligence Exchange (TIE) DXL Python Client Library at the follow link:

https://github.com/opendxl/opendxl-tie-client-python/wiki

* Certificate Files Creation [link](https://opendxl.github.io/opendxl-client-python/pydoc/certcreation.html)
* ePO Certificate Authority (CA) Import [link](https://opendxl.github.io/opendxl-client-python/pydoc/epocaimport.html)
* ePO Broker Certificates Export  [link](https://opendxl.github.io/opendxl-client-python/pydoc/epobrokercertsexport.html)

### Edit the dxlclient.config
```
[Certs]
BrokerCertChain=/brokercerts/brokercerts.crt
CertFile=/certs/client.crt
PrivateKey=/certs/client.key

[Brokers]
unique_broker_id_1=broker_id_1;broker_port_1;broker_hostname_1;broker_ip_1
unique_broker_id_2=broker_id_2;broker_port_2;broker_hostname_2;broker_ip_2
```

## (Optional) Automated Environment
1. Download Vagrant https://www.vagrantup.com/downloads.html
2. Run installer for Vagrant
3. Download Virtualbox https://www.virtualbox.org/wiki/Downloads?replytocom=98578
4. Run installer for Virtualbox
5. Download Git https://git-scm.com/downloads

### On Windows
6. Start Menu --> cmd (shift + enter to go as Administrator)
7. set PATH=%PATH%;c:\Program Files\Git\usr\bin

### Example dxlclient.config
```
[Certs]
BrokerCertChain=/vagrant/brokercerts/brokercerts.crt
CertFile=/vagrant/certs/client.crt
PrivateKey=/vagrant/certs/client.key

[Brokers]
unique_broker_id_1=broker_id_1;broker_port_1;broker_hostname_1;broker_ip_1
unique_broker_id_2=broker_id_2;broker_port_2;broker_hostname_2;broker_ip_2
```
