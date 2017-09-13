#!/usr/bin/env bash

# ensure script runs as root
if [[ $EUID -ne 0 ]]; then
   echo "Error: This script must be run as root." 
   exit 1
fi

# put jrsd in place
mkdir /root/.bin
cp ./jrsd.py /root/.bin
chmod 755 /root/.bin/jrsd.py

# put unit file in place
cp ./jrsd.service /etc/systemd/system
chmod 644 /etc/systemd/system/jrsd.service

# put config file in place
cp ./jrsd.conf /etc

# create empty log file
touch /var/log/jrsd.log
