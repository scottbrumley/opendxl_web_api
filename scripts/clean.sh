#!/bin/bash

## Stop and Remove Containers
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)

## Remove All Images
docker rm -f $(docker ps -a -q)
docker rmi -f $(docker images -q)
