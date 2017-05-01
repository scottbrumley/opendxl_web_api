#!/bin/bash

function installOpenDXLClient {
    ### Install Open DXL Client
    echo "Installing Open DXL Client"
    cd /vagrant
    sudo git clone https://github.com/opendxl/opendxl-client-python.git
    cd /vagrant/opendxl-client-python
    sudo python setup.py install
}

function installOpenDXLTIEClient {
    ### Install Open DXL TIE Client
    echo "Installing Open DXL TIE Client"
    cd /vagrant
    sudo git clone https://github.com/opendxl/opendxl-tie-client-python.git
    cd /vagrant/opendxl-tie-client-python
    sudo python setup.py install
}

function installePOClient {
    ### Install Open DXL TIE Client
    echo "Installing Open DXL ePO Client"
    cd /vagrant
    sudo git clone https://github.com/opendxl/opendxl-epo-client-python.git
    cd /vagrant/opendxl-epo-client-python
    sudo python setup.py install
}

function installMARClient {
    ### Install Open DXL MAR Client
    echo "Installing Open DXL TIE Client"
    cd /vagrant
    sudo git clone https://github.com/opendxl/opendxl-mar-client-python.git
    cd /vagrant/opendxl-mar-client-python
    sudo python setup.py install
}

function buildCertsFolders {
    ### Create Directories
    sudo mkdir -p /vagrant/brokercerts
    sudo mkdir -p /vagrant/certs
    sudo touch /vagrant/dxlclient.config
}
