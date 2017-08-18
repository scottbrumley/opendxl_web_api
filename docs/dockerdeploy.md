# Docker Build/Deploy

[Prerequisites](Prerequisites.md)

## Build Docker Container
* /vagrant/scripts/build.sh (To build a local container)
* /vagrant/scripts/build.sh push (To push to Docker Hub)

## Deploy Local on Docker (On a production Server)
``` 
1. mkdir open_web_api
2. copy brokercerts/ certs/ dxlclient.config to opendxl_web_api/
3. cd open_web_api/
4. Create Dockerfile.run
5. Copy monitor.config to directory
6. sudo docker build -t mcafee/opendxl-webapi:0.2.0 -f Dockerfile.run .
7. sudo docker run  -e FLASK_TOKEN='sometoken' -d --restart unless-stopped -p 5000:5000 --name opendxl-webapi-0-2-0  -ti mcafee/opendxl-webapi:0.2.0
```

1. Copy Configuration Files and Certs to local build directory (For more information check Prerequisites)
2. This will configure your container with your certs and site information.
3. Run Local Docker Container 

#### Example Dockerfile.run 
```
FROM sbrumley/opendxl-webapi:0.2.0
ADD ./brokercerts/ brokercerts/
ADD ./certs/ certs/
ADD dxlclient.config dxlclient.config
ADD monitor.config monitor.config
```
