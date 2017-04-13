#!/bin/bash
sudo apt-get install -y python
sudo apt-get install -y mongodb
sudo apt-get install -y g++
sudo apt-get install -y python-dev python-dpkt python-jinja2 python-magic python-pymongo python-gridfs python-libvirt python-bottle python-pefile python-chardet python-pip
sudo apt-get install -y libxml2-dev libxslt1-dev
sudo pip2 install -y sqlalchemy yara
sudo pip2 install -y cybox==2.0.1.4
sudo pip2 install -y maec==4.0.1.0
sudo pip2 install -y python-dateutil

sudo apt-get install -y python-dev libfuzzy-dev
sudo pip2 install pydeep

sudo apt-get install tcpdump # If not installed
# Allow tcpdump to read raw TCP data without root:
sudo setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump

wget http://downloads.volatilityfoundation.org/releases/2.4/volatility-2.4.zip && unzip volatility-2.4.zip && cd volatility-2.4
sudo python setup.py install
# Install the libraries that volatility wants:
sudo pip2 install distorm3