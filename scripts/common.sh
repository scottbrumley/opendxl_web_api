#!/bin/bash

if [[ -d "/vagrant" ]]; then
    ROOT_DIR="/vagrant/"
else
    ROOT_DIR="$(pwd)/"
fi

function installOpenDXLClient {
    ### Install Open DXL Client
    echo "Installing Open DXL Client"
    cd /${ROOT_DIR}
    sudo git clone https://github.com/opendxl/opendxl-client-python.git
    cd /${ROOT_DIR}/opendxl-client-python
    sudo python setup.py install
}

function installOpenDXLTIEClient {
    ### Install Open DXL TIE Client
    echo "Installing Open DXL TIE Client"
    cd /${ROOT_DIR}
    sudo git clone https://github.com/opendxl/opendxl-tie-client-python.git
    cd /${ROOT_DIR}/opendxl-tie-client-python
    sudo python setup.py install
}

function installePOClient {
    ### Install Open DXL TIE Client
    echo "Installing Open DXL ePO Client"
    cd /${ROOT_DIR}
    sudo git clone https://github.com/opendxl/opendxl-epo-client-python.git
    cd /${ROOT_DIR}/opendxl-epo-client-python
    sudo python setup.py install
}

function installMARClient {
    ### Install Open DXL MAR Client
    echo "Installing Open DXL TIE Client"
    cd /${ROOT_DIR}
    sudo git clone https://github.com/opendxl/opendxl-mar-client-python.git
    cd /${ROOT_DIR}/opendxl-mar-client-python
    sudo python setup.py install
}

function buildCertsFolders {
    ### Create Directories
    sudo mkdir -p /${ROOT_DIR}/brokercerts
    sudo mkdir -p /${ROOT_DIR}/certs
    sudo touch /${ROOT_DIR}/dxlclient.config
}

installDocker(){
    if ! [ -x "$(command -v docker)" ]; then
        sudo apt-get remove -y docker-engine
        sudo apt-get install -y linux-image-extra-$(uname -r) linux-image-extra-virtual
        sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
        # Verify  sudo apt-key fingerprint 0EBFCD88
        sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
        sudo apt-get update
        sudo apt-get install -y docker-ce
        sudo gpasswd -a vagrant docker
        sudo service docker restart
    fi
}