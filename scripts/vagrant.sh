#!/bin/bash

source /vagrant/scripts/vars.sh
source /vagrant/scripts/common.sh

ubuntuUpdate
/vagrant/scripts/bootstrap.sh
installDocker
#installD3
#installEventDrops
