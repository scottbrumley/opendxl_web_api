#!/bin/bash

vagrant plugin install vagrant-vbguest

if [[ "{$OS}" =~ "Windows" ]]; then
    cmd //C del %userprofile%\\.vagrant.d\\insecure_private_key
fi

if [ "${1}" == "cuckoo" ]; then
    echo "Set Up Cuckoo"
    VAGRANT_VAGRANTFILE=Vagrantfile-cuckoo vagrant up --provider=virtualbox
else
   echo "Web API Only"
    vagrant up --provider=virtualbox
fi

vagrant ssh