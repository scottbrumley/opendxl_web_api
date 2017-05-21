#!/bin/bash

source scripts/vars.sh

if [ "${1}" == "push" ]; then
    echo "Building and Pushing Container ${LOCAL_BULD} to Docker Hub"
    docker build -t ${LOCAL_BUILD} -f Dockerfile.build .
    docker login
    echo "Tagging Container ${LOCAL_BUILD} to ${REMOTE_BUILD} for Shipping"
    docker tag ${LOCAL_BUILD} ${REMOTE_BUILD}
    docker push ${REMOTE_BUILD}
else
   echo "Building Local Image ${LOCAL_BUILD}"
   docker build -t ${LOCAL_BUILD} -f Dockerfile.build .
fi