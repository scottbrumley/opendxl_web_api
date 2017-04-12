# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
    config.vm.define "web" do |web|
            web.vm.box = "ubuntu/trusty64"
            web.vm.hostname = "web"
            web.vm.network "forwarded_port", host_ip: "127.0.0.1", guest_ip: "127.0.0.1", guest: 5000, host: 5000
            web.vm.provision "shell", path: "scripts/bootstrap-webapi.sh"
            web.vm.provider :virtualbox do |v|
                v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
                v.customize ["modifyvm", :id, "--memory", 512]
                v.customize ["modifyvm", :id, "--name", "web"]
            end
        end
end