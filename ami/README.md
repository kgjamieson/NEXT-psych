# Startup script for Ubuntu

The `next.conf` script can be used to start NEXT with frontend at startup time on an Ubuntu machine with the following things 
installed:

* python2.7
* pip
* docker
* docker-compose

If you place `next.conf` in `/etc/init/` and reboot, it will clone this repository and run `/local/docker_up.sh` at HEAD in the 
master branch.  
