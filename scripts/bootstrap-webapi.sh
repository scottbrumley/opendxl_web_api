#!/bin/bash

REQ_PY_VER="2.7.9"
REQ_SSL_VER="1.0.1"

PY_VER=$(python -c 'import sys; print(sys.version)')

source ./common.sh

installPython
installGit
installPip
installPythonCommon
installOpenDXLClient
installOpenDXLTIEClient
installMARClient
installePOClient
installOpenSSL
buildCertsFolders
installFlask

## Setup Flask Environment
sudo echo 'export FLASK_APP=/vagrant/opendxl_web_api.py' >> /etc/bash.bashrc