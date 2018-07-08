#!/bin/bash

source scripts/vars.sh
source scripts/common.sh

echo "Checking Sudo ... "
installSudo

sudo apt-get -y install python3-pip

sudo pip3 install -r requirements.txt

#echo "Installing Flask ... "
#installFlask
#echo "Installing OpenDXL TIE"
#installOpenDXLTIEClient
#installFlaskSockets

#installMARClient
#installePOClient
#buildCertsFolders

echo "Cleanup"
cleanUp

