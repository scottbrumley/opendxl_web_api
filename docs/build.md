# Build Development Environment

[Prerequisites](Prerequisites.md)

## Build In Vagrant

1. git clone https://github.com/scottbrumley/opendxl_web_api
2. cd opendxl_web_api/
3. ./vssh.sh (On Windows Launch from Git Bash)
4. cd /vagrant
5. Copy broker certificates to brokercerts/ directory
6. Copy client certificates to the certs/ directory
7. Copy dxlclient.config to your / root directory
8. Configure your monitor.config for DXL Monitoring Service

## Run
* /vagrant/scripts/service.sh **start** (other options **stop** and **status**)

## Test
* **Automated Tests:** /vagrant/tests/urltests.sh (Runs all tests that run on start)
* **Manual Test:** Connect http://127.0.0.1:5000/about?token=<security token> to Test


## Default Security Token
**Please Change:**
27612211994137900087

"Lives in the function called authenticate"

# Docker Build/Deploy

## Build Docker Container
* /vagrant/scripts/build.sh (To build a local container)
* /vagrant/scripts/build.sh push (To push to Docker Hub)

## Deploy Local on Docker (On a production Server or Vagrant Dev Environment)
* Add Files/Directories for configuration: brokercerts/ , certs/ , [dxlclient.config](Prerequisites.md) , monitor.config
* sudo docker build -t mcafee/opendxl-webapi:0.1.1 -f Dockerfile.run .  (This will configure your container with your certs and site information.) 
* /vagrant/scripts/run.sh

## Deploy Into Docker Swarm for Production
* Add Files/Directories for configuration: brokercerts/ , certs/ , [dxlclient.config](Prerequisites.md) , monitor.config
* sudo docker build -t mcafee/opendxl-webapi:0.1.1 -f Dockerfile.run .  (This will configure your container with your certs and site information.)
* sudo docker service create --name opendxl-webapi --replicas 3 --publish 5000:5000

#### Example Dockerfile for Run
```
FROM sbrumley/opendxl-webapi:0.1.1
ADD brokercerts/ brokercerts/
ADD certs/ certs/
ADD dxlclient.config dxlclient.config
ADD monitor.config monitor.config
ENV FLASK_TOKEN="27612211994137900087"
```

## More Documentation
[Miscellaneous](misc.md)