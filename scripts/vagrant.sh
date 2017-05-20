#!/bin/bash

source /vagrant/scripts/vars.sh
source /vagrant/scripts/common.sh

installSudo
installFlask
installDocker
/vagrant/scripts/bootstrap.sh


