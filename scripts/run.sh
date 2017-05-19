#!/bin/bash

docker build -t mcafee:opendxl-webapi -f Dockerfile.run .

docker run -d -p 5000:5000 --name opendxl-webapi  -ti mcafee:opendxl-webapi /bin/bash
