#!/usr/bin/env bash

# ensure script runs as root
if [[ $EUID -ne 0 ]]; then
   echo "Error: This script must be run as root." 
   exit 1
fi

# install necessary packages
rpm -Uvh ./packages/python36u-*
tar xzvf ./packages/scapy-python3-0.21.tar.gz -C ./packages
pushd packages/scapy-python3-0.21
python3.6 setup.py install
popd

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
