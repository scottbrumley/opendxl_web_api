#!/bin/bash

source scripts/vars.sh
source scripts/common.sh

echo "Checking Sudo ... "
installSudo
echo "Installing Flask ... "
installFlask
echo "Installing OpenDXL TIE"
installOpenDXLTIEClient
#installMARClient
#installePOClient
#buildCertsFolders
echo "Cleanup"
cleanUp

