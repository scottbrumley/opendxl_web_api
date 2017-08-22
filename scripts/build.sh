#!/bin/bash

source scripts/vars.sh

rm -rf opendxl-tie-client-python

if [ "${1}" == "push" ]; then
    echo "Building and Pushing Container ${LOCAL_BULD} to Docker Hub"
    docker build -t ${LOCAL_BUILD} -f Dockerfile .
    docker login
    echo "Tagging Container ${LOCAL_BUILD} to ${REMOTE_BUILD} for Shipping"
    docker tag ${LOCAL_BUILD} ${REMOTE_BUILD}
    docker push ${REMOTE_BUILD}
else
   echo "Tagging Container ${LOCAL_BUILD} to ${REMOTE_BUILD} for Shipping"
   docker tag ${LOCAL_BUILD} ${REMOTE_BUILD}
   echo "Building Local Image ${LOCAL_BUILD}"
   docker build -t ${LOCAL_BUILD} -f Dockerfile .
fi