#!/usr/bin/env bash

REQ_PY_VER="2.7.9"
REQ_SSL_VER="1.0.1"

PY_VER=$(python -c 'import sys; print(sys.version)')

source /vagrant/scripts/common.sh

installPython
installGit
installPip
installPythonCommon
installOpenDXLClient
installOpenDXLTIEClient
installePOClient
installOpenSSL
buildCertsFolders
installFlask