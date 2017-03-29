#!/usr/bin/env bash
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