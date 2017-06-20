# Docker Build/Deploy

[Prerequisites](Prerequisites.md)

## Build Docker Container
* /vagrant/scripts/build.sh (To build a local container)
* /vagrant/scripts/build.sh push (To push to Docker Hub)

## Deploy Local on Docker (On a production Server or Vagrant Dev Environment)
``` 
1. Add Files/Directories for configuration: brokercerts/ , certs/ , dxlclient.config , monitor.config
2. sudo docker build -t mcafee/opendxl-webapi:0.1.1 -f Dockerfile.run .   
3. /vagrant/scripts/run.sh
```

1. Copy Configuration Files and Certs to local build directory (For more information check Prerequisites)
2. This will configure your container with your certs and site information.
3. Run Local Docker Container 

#### Example Dockerfile for Run
```
FROM sbrumley/opendxl-webapi:0.1.1
ADD brokercerts/ brokercerts/
ADD certs/ certs/
ADD dxlclient.config dxlclient.config
ADD monitor.config monitor.config
ENV FLASK_TOKEN="27612211994137900087"
```
