#!/bin/bash

source scripts/vars.sh

#!/bin/bash

if [ "${1}" == "push" ]; then
    echo "Building and Pushing Container to Docker Hub"
    docker build -t ${LOCAL_BUILD} .
    docker login
    docker tag ${LOCAL_BUILD} ${REMOTE_BUILD}
    docker push ${REMOTE_BUILD}
else
   echo "Building Locally"
   docker build -t ${LOCAL_BUILD} .
fi