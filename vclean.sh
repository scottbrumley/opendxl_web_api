#!/usr/bin/env bash

vagrant destroy -f web
vagrant destroy -f cuckoo
vagrant destroy -f cuckoo1
rm -rf opendxl-client-python
rm -rf cuckoo