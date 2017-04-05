# Miscellaneous

## Remove Environment
If you want to burn the whole thing to the ground just exit the guest and use this command.
```
exit
./vclean.ssh
```

## How to SSH into vagrant guest
```
vagrant ssh
```

## How to exit vagrant guest
```
exit
```

### About Flask
  http://flask.pocoo.org/
 
Flask Uses and Environment variable to locate the python program.  It is set in the scripts/bootstrap.sh upon build of the vagrant environment.
  ```
  sudo echo 'export FLASK_APP=/vagrant/tie_rep_api.py' >> /etc/bash.bashrc
  ```

### About Vagrant
https://www.vagrantup.com/

Vagrant uses the Vagrantfile to build environment.  Important lines:
```
config.vm.box = "ubuntu/trusty64"
config.vm.network "forwarded_port", guest: 5000, host: 5000
config.vm.provision "shell", path: "scripts/bootstrap.sh"
```

### About Git
https://git-scm.com

Git is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency.
