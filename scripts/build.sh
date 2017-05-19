#!/bin/bash

if [ "${1}" == "push" ]; then
    echo "Building and Pushing Container to Docker Hub"
    docker build -t "mcafee:opendxl-webapi" .
    docker login
    docker tag mcafee:opendxl-webapi sbrumley/opendxl-webapi
    docker push sbrumley/opendxl-webapi
else
   echo "Building Locally"
   docker build -t "mcafee:opendxl-webapi" .
fi
