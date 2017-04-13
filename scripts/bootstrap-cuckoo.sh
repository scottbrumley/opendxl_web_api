#!/bin/bash

REQ_PY_VER="2.7.9"
REQ_SSL_VER="1.0.1"

PY_VER=$(python -c 'import sys; print(sys.version)')

### Xenial hostname fix in Vagrant
sudo apt-get install libnss-myhostname
sudo echo '127.0.0.1 ubuntu-xenial' >> /etc/hosts
sudo hostnamectl set-hostname

### Install Python 2.7.9
if [[ "${PY_VER}" =~ "${REQ_PY_VER}" ]]; then
    echo "Already Version ${REQ_PY_VER}"
else
    #sudo echo 'deb http://httpredir.debian.org/debian xenial main' >> python-xenial.list
    #sudo echo 'deb-src http://httpredir.debian.org/debian xenial main' >> python-xenial.list
    #sudo echo 'deb http://httpredir.debian.org/debian xenial-updates main' >> python-xenial.list
    #sudo echo 'deb-src http://httpredir.debian.org/debian xenial-updates main' >> python-xenial.list
    #sudo echo 'deb http://security.debian.org/ xenial/updates main' >> python-xenial.list
    #sudo mv python-xenial.list /etc/apt/sources.list.d/python-xenial.list

    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8B48AD6246925553
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7638D0442B90D010
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 9D6D8F6BC857C906
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys CBF8D6FD518E17E1

    ### Virtual Box
    echo "deb-src http://security.debian.org/ xenial/updates main" | sudo tee -a /etc/apt/sources.list.d/virtualbox.list
    wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -
    wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | sudo apt-key add -

    #sudo echo 'Package: *' >> python-xenial-pin
    #sudo echo 'Pin: release o=Debian' >> python-xenial-pin
    #sudo echo 'Pin-Priority: -10' >> python-xenial-pin
    #sudo mv python-xenial-pin /etc/apt/preferences.d/python-xenial-pin

    sudo apt-get -y upgrade
    sudo apt-get update
    sudo apt-get install -y -t xenial python2.7
fi

### Install VirtualBox
sudo apt-get install virtualbox
sudo virtualbox

### Install Git
sudo apt-get install -y git

### Install Pip
echo "Installing Pip"
sudo apt-get install -y python-pip
sudo pip install --upgrade pip

## Cuckoo Dependencies
#sudo apt-get install -y python python-dev libxml2-dev libffi-dev libssl-dev libxslt1-dev

sudo apt-get install -y python3-dev python-pip python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev libjpeg-dev
sudo apt-get install -y mongodb

### Get Cuckoo
echo "Installing Cuckoo"
cd /vagrant
sudo git clone git://github.com/cuckoosandbox/cuckoo.git
sudo pip install -r /vagrant/cuckoo/requirements.txt

### Install TCPDump
sudo apt-get -y install tcpdump
sudo setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump




