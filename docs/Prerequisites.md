# Prerequisites

## Configuration Information
* Put your broker certs in the brokercerts/ directory [Certificate Setup](./cert_setup.md)
* Put your client certificates in the certs/ directory [Certificate Setup](./cert_setup.md)
* Edit dxlclient.config and add your Broker(s)

## Automated Environment
1. Download Vagrant https://www.vagrantup.com/downloads.html
2. Run installer for Vagrant
3. Download Virtualbox https://www.virtualbox.org/wiki/Downloads?replytocom=98578
4. Run installer for Virtualbox
3. Download Git https://git-scm.com/downloads


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
