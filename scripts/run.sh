#!/bin/bash

source scripts/vars.sh

docker build -t ${LOCAL_BUILD} -f Dockerfile.run .

docker run -d -p 5000:5000 --name opendxl-webapi  -ti ${LOCAL_BUILD}
