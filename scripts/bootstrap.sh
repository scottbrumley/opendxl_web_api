#!/bin/bash

source scripts/vars.sh
source scripts/common.sh

installSudo
installFlask
installOpenDXLTIEClient
#installMARClient
#installePOClient
#buildCertsFolders
cleanUp

