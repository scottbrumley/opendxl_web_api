#!/bin/bash

if [[ -d "/vagrant" ]]; then
    ROOT_DIR="/vagrant/"
else
    ROOT_DIR="$(pwd)/"
fi

function ubuntuUpgrade {
    sudo apt-get install -y unattended-upgrades
    sudo apt-get -y upgrade
}

function ubuntuUpdate {
    sudo apt-get update
}

function cleanUp {
    sudo apt-get -y autoremove
    sudo apt-get -y clean
}

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

function installDocker(){
    ${SUDO}apt-get remove -y docker-engine
    ${SUDO}apt-get install -y linux-image-extra-$(uname -r) linux-image-extra-virtual
    ${SUDO}apt-get install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    # Verify  sudo apt-key fingerprint 0EBFCD88
    ${SUDO}add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    ${SUDO}apt-get update
    ${SUDO}apt-get install -y docker-ce
    ${SUDO}gpasswd -a vagrant docker
    ${SUDO}service docker restart
}

installSudo(){
    if ! [ -x "$(command -v sudo)" ]; then
        echo 'Error: sudo is not installed.' >&2
        SUDO=""
        ${SUDO}apt-get install -y sudo
    else
        SUDO="sudo "
    fi

}

installFlask(){
    ## Setup Flask
    ## Use flask run --host=0.0.0.0 to start Flask
    ${SUDO}pip install Flask
    ## Setup Flask Environment
    ${SUDO}echo 'export FLASK_APP=/${ROOT_DIR}/opendxl_web_api.py' >> /etc/bash.bashrc
}