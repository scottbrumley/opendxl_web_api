#!/usr/bin/env bash

REQ_PY_VER="2.7.9"
REQ_SSL_VER="1.0.1"

PY_VER=$(python -c 'import sys; print(sys.version)')

### Install Python 2.7.9
if [[ "${PY_VER}" =~ "${REQ_PY_VER}" ]]; then
    echo "Already Version ${REQ_PY_VER}"
else
    sudo echo 'deb http://httpredir.debian.org/debian trusty main' >> python-trusty.list
    sudo echo 'deb-src http://httpredir.debian.org/debian trusty main' >> python-trusty.list
    sudo echo 'deb http://httpredir.debian.org/debian trusty-updates main' >> python-trusty.list
    sudo echo 'deb-src http://httpredir.debian.org/debian trusty-updates main' >> python-trusty.list
    sudo echo 'deb http://security.debian.org/ trusty/updates main' >> python-trusty.list
    sudo echo 'deb-src http://security.debian.org/ trusty/updates main' >> python-trusty.list
    sudo mv python-trusty.list /etc/apt/sources.list.d/python-trusty.list

    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8B48AD6246925553
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7638D0442B90D010
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 9D6D8F6BC857C906
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys CBF8D6FD518E17E1

    sudo echo 'Package: *' >> python-trusty-pin
    sudo echo 'Pin: release o=Debian' >> python-trusty-pin
    sudo echo 'Pin-Priority: -10' >> python-trusty-pin
    sudo mv python-trusty-pin /etc/apt/preferences.d/python-trusty-pin

    sudo apt-get -y upgrade
    sudo apt-get update
    sudo apt-get install -y -t trusty python2.7
fi

sudo apt-get install -y libssl-dev
sudo apt-get install -y mongodb
sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test
sudo apt-get update
sudo apt-get install -y gcc-4.9 g++-4.9
sudo update-alternatives --remove-all gcc
sudo update-alternatives --remove-all g++
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.9 20
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.9 20
sudo update-alternatives --config gcc
sudo update-alternatives --config g++
sudo rm /usr/bin/x86_64-linux-gnu-gcc
sudo ln -s /usr/bin/gcc-4.9 /usr/bin/x86_64-linux-gnu-gcc
sudo rm /usr/bin/x86_64-linux-gnu-g++
sudo ln -s /usr/bin/gcc-4.9 /usr/bin/x86_64-linux-gnu-g++

### Install Git
sudo apt-get install -y git

### Install Pip
echo "Installing Pip"
sudo apt-get install -y python-pip

## Cuckoo Dependencies
#sudo apt-get install -y python python-dev libxml2-dev libffi-dev libssl-dev libxslt1-dev
sudo apt-get install build-essential libxml2-dev libxslt1-dev
sudo apt-get install python-dev libffi-dev libssl-dev
sudo apt-get install -y mongodb

### Get Cuckoo
echo "Installing Cuckoo"
cd /vagrant
sudo git clone git://github.com/cuckoosandbox/cuckoo.git
sudo pip install -r /vagrant/cuckoo/requirements.txt
