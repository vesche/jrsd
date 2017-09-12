#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys

LOG_PATH = '/var/log/jrsd.log'


def _preflight_jrsd():
    # check for root
    if not os.geteuid() == 0:
        print('Error: This program needs to be run as root.\n')
        sys.exit(1)


def alert_and_log(message):
    command = "echo {} | tee -a {} | wall".format(message, LOG_PATH).split()
    os.system(command)

def arp_scan():
    pass

def check_whitelist():
    pass

def get_parser():
    parser = argparse.ArgumentParser(description='Jackson\'s Rogue System Detection')
    parser.add_argument('-i', '--interval',
                        help='scan interval in seconds (default 60 sec)',
                        default=60, type=float)
    return parser


def main():
    parser = get_parser()
    args = vars(parser.parse_args())
    
    scan_interval = args['interval']
    
    # ladies and gentlemen this is your captain speaking
    _preflight_jrsd()
    
    # todo - meat, dameon?
    arp_scan()
    check_whitelist()
    
    # alert_and_log('hello, world!')


# remove later
if __name__ == '__main__':
    main()