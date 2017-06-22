# Quick Start Using Docker

[Prerequisites](Prerequisites.md)



``` 
1. git clone https://github.com/scottbrumley/opendxl_web_api.git
2. cd opendxl_web_api
3. ./scripts/build.sh
4. copy brokercerts/ , certs/ , dxlclient.config , monitor.config to project directory
5. /vagrant/scripts/run.sh
6. sudo docker ps
```

## Description of Steps
1. Clone the Git Repo
2. Enter the project directory 
3. Build a local base container
4. Copy Configuration Files, Broker certs and Client certs to local build directory (For more information check Prerequisites)
5. Check dxlclient.config for relative paths to brokercerts & certs not absolute
6. Build run container and start container 
7. Check Container is Running (on some systems sudo is not needed.)

## Connect To the Web Page Locally
http://127.0.0.1:5000/about?token=27612211994137900087

## Checking File Reputation by SHA1 Hash
http://127.0.0.1:5000/tie/getfile/?sha1=D4186881780D48BF55D4D59171B115634E3C7BA6?token=27612211994137900087

## Stopping Container
./scripts/stop.sh

## Troubleshooting Docker
sudo docker logs opendxl-webapi

#### Example Dockerfile.run
```
FROM sbrumley/opendxl-webapi:0.1.1
ADD brokercerts/ brokercerts/
ADD certs/ certs/
ADD dxlclient.config dxlclient.config
ADD monitor.config monitor.config
ENV FLASK_TOKEN="27612211994137900087"
```

#### Example dxlclient.config
```
[Certs]
BrokerCertChain=brokercerts/brokercerts.crt
CertFile=certs/client.crt
PrivateKey=certs/client.key

[Brokers]
{UUID From ePO}={UUID From ePO};8883;dxl server name;dxl server ip
```

## Successful Start
This will show all the testing as successful followed by the phrase All Test Successful

Example:
``` 
#### TEST: Test WannaCry 3f3a9dde96ec4107f67b0559b4e95f5f1bca1ec6cb204bfe5fea0230845e8301 ####
     Testing http://127.0.0.1:5000/tie/setfile/?sha256=3f3a9dde96ec4107f67b0559b4e95f5f1bca1ec6cb204bfe5fea0230845e8301&token=27612211994137900087 ####
TEST SUCCESS: Test WannaCry 3f3a9dde96ec4107f67b0559b4e95f5f1bca1ec6cb204bfe5fea0230845e8301
All Test Successful
```

