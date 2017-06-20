# Docker Swarm Deploy

[Prerequisites](Prerequisites.md)


## Deploy Into Docker Swarm for Production
```
1. Add Files/Directories for configuration: brokercerts/ , certs/ , dxlclient.config , monitor.config
2. sudo docker build -t mcafee/opendxl-webapi:0.1.1 -f Dockerfile.run .  (This will configure your container with your certs and site information.)
3. sudo docker service create --name opendxl-webapi --replicas 3 --publish 5000:5000
```
1. Copy Configuration Files and Certs to local build directory (For more information check Prerequisites)
2. This will configure your container with your certs and site information.
3. Run Docker Swarm Service

#### Example Dockerfile for Run
```
FROM sbrumley/opendxl-webapi:0.1.1
ADD brokercerts/ brokercerts/
ADD certs/ certs/
ADD dxlclient.config dxlclient.config
ADD monitor.config monitor.config
ENV FLASK_TOKEN="27612211994137900087"
```