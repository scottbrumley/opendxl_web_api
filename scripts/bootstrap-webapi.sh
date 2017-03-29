#!/usr/bin/env bash

REQ_PY_VER="2.7.9"
REQ_SSL_VER="1.0.1"

PY_VER=$(python -c 'import sys; print(sys.version)')

### Install Python 2.7.9
if [[ "${PY_VER}" =~ "${REQ_PY_VER}" ]]; then
    echo "Already Version ${REQ_PY_VER}"
else
    sudo apt-get update
    sudo apt-get -y upgrade

    echo "deb http://httpredir.debian.org/debian trusty main" | sudo tee -a /etc/apt/sources.list.d/python-trusty.list
    echo "deb-src http://httpredir.debian.org/debian trusty main" | sudo tee -a /etc/apt/sources.list.d/python-trusty.list
    echo "deb http://httpredir.debian.org/debian trusty-updates main" | sudo tee -a /etc/apt/sources.list.d/python-trusty.list
    echo "deb-src http://httpredir.debian.org/debian trusty-updates main" | sudo tee -a /etc/apt/sources.list.d/python-trusty.list
    echo "deb http://security.debian.org/ trusty/updates main" | sudo tee -a /etc/apt/sources.list.d/python-trusty.list
    echo "deb-src http://security.debian.org/ trusty/updates main" | sudo tee -a /etc/apt/sources.list.d/python-trusty.list

    #sudo mv python-trusty.list /etc/apt/sources.list.d/python-trusty.list

    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8B48AD6246925553
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7638D0442B90D010
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 9D6D8F6BC857C906

    sudo echo 'Package: *' >> python-trusty-pin
    sudo echo 'Pin: release o=Debian' >> python-trusty-pin
    sudo echo 'Pin-Priority: -10' >> python-trusty-pin
    sudo mv python-trusty-pin /etc/apt/preferences.d/python-trusty-pin

    sudo apt-get update
    sudo apt-get install -y -t trusty python2.7 vsudo apt-get install -y python-dev
fi

### Install Git
sudo apt-get install -y git

### Install Pip
echo "Installing Pip"
sudo apt-get install -y python-pip

### Install Common
echo "Install Common for Python"
sudo pip install common

### Install Open DXL Client
echo "Installing Open DXL Client"
cd /vagrant
sudo git clone https://github.com/opendxl/opendxl-client-python.git
cd /vagrant/opendxl-client-python
sudo python setup.py install

### Check OpenSSL
SSL_VER=$(python -c 'import ssl; print(ssl.OPENSSL_VERSION)')

if [[ "${SSL_VER}" =~ "${REQ_SSL_VER}" ]]; then
    echo "Already Version ${REQ_SSL_VER}"
else
    echo "Need OpenSSL version ${REQ_SSL_VER} or higher"
fi

### Create Directories
sudo mkdir -p /vagrant/brokercerts
sudo mkdir -p /vagrant/certs
sudo touch /vagrant/dxlclient.config

## Setup Flask
## Use flask run --host=0.0.0.0 to start Flask
sudo pip install Flask
sudo echo 'export FLASK_APP=/vagrant/open_web_api.py' >> /etc/bash.bashrc