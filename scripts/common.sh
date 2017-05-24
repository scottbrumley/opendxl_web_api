#!/bin/bash

if [[ -d "/vagrant" ]]; then
    ROOT_DIR="/vagrant/"
else
    ROOT_DIR="$(pwd)/"
fi

function ubuntuUpgrade {
    ${SUDO}apt-get install -y unattended-upgrades
    ${SUDO}apt-get -y upgrade
}

function ubuntuUpdate {
    ${SUDO}apt-get update
}

function cleanUp {
    ${SUDO}apt-get -y autoremove
    ${SUDO}apt-get -y clean
}

function installOpenDXLClient {
    ### Install Open DXL Client
    echo "Installing Open DXL Client"
    cd /${ROOT_DIR}
    ${SUDO}git clone https://github.com/opendxl/opendxl-client-python.git
    cd /${ROOT_DIR}/opendxl-client-python
    ${SUDO}python setup.py install
}

function installOpenDXLTIEClient {
    if [[ -d "${ROOT_DIR}/opendxl-tie-client-python" ]]; then
        ${SUDO}rm -rf ${ROOT_DIR}/opendxl-tie-client-python
    fi

    ### Install Open DXL TIE Client
    echo "Installing Open DXL TIE Client"
    cd ${ROOT_DIR}
    ${SUDO}git clone https://github.com/opendxl/opendxl-tie-client-python.git
    cd ${ROOT_DIR}/opendxl-tie-client-python
    ${SUDO}python setup.py install
}

function installePOClient {
    ### Install Open DXL TIE Client
    echo "Installing Open DXL ePO Client"
    cd /${ROOT_DIR}
    ${SUDO}git clone https://github.com/opendxl/opendxl-epo-client-python.git
    cd /${ROOT_DIR}/opendxl-epo-client-python
    ${SUDO}python setup.py install
}

function installMARClient {
    ### Install Open DXL MAR Client
    echo "Installing Open DXL TIE Client"
    cd /${ROOT_DIR}
    ${SUDO}git clone https://github.com/opendxl/opendxl-mar-client-python.git
    cd /${ROOT_DIR}/opendxl-mar-client-python
    ${SUDO}python setup.py install
}

function buildCertsFolders {
    ### Create Directories
    ${SUDO}mkdir -p /${ROOT_DIR}/brokercerts
    ${SUDO}mkdir -p /${ROOT_DIR}/certs
    ${SUDO}touch /${ROOT_DIR}/dxlclient.config
}

function installDocker(){
    ${SUDO}apt-get remove -y docker-engine
    ${SUDO}apt-get install -y linux-image-extra-$(uname -r) linux-image-extra-virtual
    ${SUDO}apt-get install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | ${SUDO}apt-key add -
    # Verify  ${SUDO}apt-key fingerprint 0EBFCD88
    ${SUDO}add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    ${SUDO}apt-get update
    ${SUDO}apt-get install -y docker-ce
    ${SUDO}gpasswd -a vagrant docker
    ${SUDO}service docker restart
}

installSudo(){
    if ! [ -x "$(command -v sudo)" ]; then
        echo 'Error: ${SUDO}is not installed.' >&2
        SUDO=""
        #${SUDO}apt-get install -y sudo
    else
        SUDO="${SUDO}"
    fi

}

installFlask(){
    ## Setup Flask
    ## Use flask run --host=0.0.0.0 to start Flask
    ${SUDO}pip install Flask
    ## Setup Flask Environment
    echo "${SUDO}echo 'export FLASK_APP=/${ROOT_DIR}/opendxl_web_api.py' >> /etc/bash.bashrc"
    ${SUDO}echo 'export FLASK_APP=/${ROOT_DIR}/opendxl_web_api.py' >> /etc/bash.bashrc
}

installD3(){
    ${SUDO}apt-get install -y unzip
    mkdir -p static/d3
    wget https://github.com/d3/d3/releases/download/v4.9.1/d3.zip
    ${SUDO}unzip d3.zip -d static/d3
    ${SUDO}rm -f d3.zip
}

installEventDrops(){
    cd static
    git clone https://github.com/marmelab/EventDrops.git
    cd ..
}