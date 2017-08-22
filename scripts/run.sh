#!/bin/bash

source scripts/vars.sh

docker build -t ${LOCAL_BUILD} -f Dockerfile.run .

sudo docker run  -e FLASK_TOKEN='sometoken' -d -p 5000:5000 --name opendxl-webapi -ti ${LOCAL_BUILD}
