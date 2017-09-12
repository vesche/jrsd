#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import configparser
import logging
import os
import re
import socket
import sys
import time

# supress scapy ipv6 warning
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

from scapy.all import arping

CONFIG_PATH = '/etc/jrsd.conf'
LOG_PATH = '/var/log/jrsd.log'


def _preflight_jrsd():
    # check for root
    if not os.geteuid() == 0:
        print('Error: This program needs to be run as root.\n')
        sys.exit(1)
    
    # ensure config file exists
    if not os.path.isfile(CONFIG_PATH):
        print('Error: Config file /etc/jrsd.conf was not found.\n')
        sys.exit(1)


def _validate_config(ip_space, interval, whitelist):
    # ensure ip_space is a valid subnet
    ip, cidr = ip_space.split('/')
    try:
        socket.inet_aton(ip)
        if not (8 <= int(cidr) <= 32):
            raise socket.error
    except (socket.error, ValueError):
        print('Error: Invalid ip_space "{}" specified in config.'.format(ip_space))

    # ensure interval is a valid float
    try:
        float(interval)
    except ValueError:
        print('Error: Invalid interval "{}" specified in config.'.format(interval))
        sys.exit(1)
    
    # ensure whitelist contains valid mac addresses
    for m in whitelist:
        if not re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", m):
            print('Error: Invalid MAC address "{}" specified in config.'.format(m))
            sys.exit(1)


def alert_and_log(message):
    # get current datetime
    dt = time.strftime('%a, %d %b %Y %H:%M:%S {}'.format(time.tzname[0]), time.localtime())

    # write alert to log file & send system wide
    log = '{} - {}'.format(dt, message)
    command = "echo {} | tee -a {} | wall".format(log, LOG_PATH)
    os.system(command)


# add arp spoofing later
def arp_scan(ip_space):
    macs = []
    
    ans_pkts, _ = arping(ip_space, verbose=0)
    for pkt in ans_pkts:
        m = pkt[1].sprintf("%Ether.src%")
        m = '-'.join(m.split(':')).lower()
        macs.append(m)
    
    return macs


def main():
    # ladies and gentlemen this is your captain speaking
    _preflight_jrsd()

    # load config file
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(CONFIG_PATH)
    ip_space = config['settings']['ip_space']
    interval = config['settings']['interval']

    # read in whitelist from config
    whitelist = []
    for mac, _ in config['whitelist'].items():
        whitelist.append(mac.lower())

    # error check config values
    _validate_config(ip_space, interval, whitelist)
    
    # jrsd main loop
    while True:
        # conduct arp scan
        macs = arp_scan(ip_space)
        
        # check if a mac isn't in the whitelist
        for m in macs:
            if m not in whitelist:
                alert_and_log('jrsd ALERT: {}'.format(m))

        # sleep for specified interval
        time.sleep(float(interval))


# remove later
if __name__ == '__main__':
    main()