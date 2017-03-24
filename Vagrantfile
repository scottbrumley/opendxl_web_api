# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
    #config.vm.define "web" do |web|
    #    web.vm.box = "trusty64"
    #    web.vm.hostname = "web"
    #    web.vm.box_url = "ubuntu/trusty64"
    #    web.vm.network "forwarded_port", guest: 5000, host: 5000
    #    web.vm.provision "shell", path: "scripts/bootstrap-webapi.sh"
    #    web.vm.provider :virtualbox do |v|
    #        v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    #        v.customize ["modifyvm", :id, "--memory", 512]
    #        v.customize ["modifyvm", :id, "--name", "web"]
    #    end
    #end
    #    config.vm.define "cuckoo" do |cuckoo|
    #        cuckoo.vm.box = "ubuntu/xenial64"
    #        #cuckoo.vm.hostname = "cuckoo"
    #        cuckoo.vm.network "forwarded_port", guest: 5001, host: 5001
    #        cuckoo.vm.synced_folder ".", "/vagrant", create: true
    #        cuckoo.vm.provision "shell", path: "scripts/bootstrap-cuckoo.sh"
    #            cuckoo.vm.provider :virtualbox do |v|
    #                v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    #                v.customize ["modifyvm", :id, "--memory", 2048]
    #                v.customize ["modifyvm", :id, "--name", "cuckoo"]
    #            end
    #    end
        config.vm.define "cuckoo1" do |cuckoo1|
                    cuckoo1.vm.box = "designerror/windows-7"
                    cuckoo1.vm.hostname = "cuckoo1"
                    #cuckoo1.vm.network "forwarded_port", guest: 5001, host: 5001
                    cuckoo1.vm.synced_folder ".", "/vagrant", create: true
                    #cuckoo1.vm.provision "shell", path: "scripts/bootstrap-cuckoo-guest.ps1"
                    cuckoo1.vm.provision "shell", path: "scripts/bootstrap-cuckoo-guest.ps1", privileged: true
                        cuckoo1.vm.provider :virtualbox do |v|
                            v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
                            v.customize ["modifyvm", :id, "--memory", 2048]
                            v.customize ["modifyvm", :id, "--name", "cuckoo1"]
                        end
                end
end