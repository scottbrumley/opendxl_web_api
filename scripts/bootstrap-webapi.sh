#!/bin/bash

source scripts/common.sh

installOpenDXLTIEClient
installMARClient
installePOClient
buildCertsFolders

## Setup Flask Environment
sudo echo 'export FLASK_APP=/${ROOT_DIR}/opendxl_web_api.py' >> /etc/bash.bashrc