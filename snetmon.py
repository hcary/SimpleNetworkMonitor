#!/usr/bin/env python3

import re
import sys
import os
import requests
import time
import subprocess
import logging
import configparser

from urllib.error import HTTPError
from optparse import OptionParser

def print_tl(msg):
    print(" ", msg)

def print_sub(msg):
    print("    ", msg)

def print_head(msg):

    stdout.info('=====================================================================')
    stdout.info(msg)
    stdout.info('=====================================================================')

def check_url(url):

    global error_count
    global ok_count
    global iteration
    global gen_error
    global ok_status

    stdout.info('Connecting to: ' + url)

    iteration += 1

    try:
        r = requests.get(url)
        r.raise_for_status()

        if gen_error:
            r.status_code = 100

        if r.status_code != 200:
            msg = 'Status code: ' + str(r.status_code) + ' Unable to connect to ' + url
            stdout.critical(msg)
            error_count += 1
            ok_count = 0
            ok_status = False
        else:
            ok_count += 1
            error_count = 0
            ok_status = True
            
    except requests.exceptions.HTTPError as err:
        error_count += 1
        return "Error: {}".format(err)
        ok_status = True

    except requests.ConnectionError as e:
        msg = 'Connection Error: ' + str(e) + ' Unable to connect to ' + url
        stdout.critical(msg)
        ok_status = True

    if ok_status and ok_count % ok_int_report == 0:
        seconds = ok_count * sleep_time
        stdout.info('No Errors for ' + str(iteration) + ' iterations')

    return ok_status

def check_ping(host):

    global error_count
    global ok_count
    global gen_error
                 
    stdout.info('TESTING: Sending ping request to: ' + str(host))
    r = subprocess.run(['ping', '-c3', '-W1', host], capture_output=True, text=True)

    if gen_error:
        r.returncode = 1

    if r.returncode != 0:
        # stdout.error(r.returncode)
        stdout.error(' FAILED: Ping returned error code: ' + str(r.returncode))

        ping_output=r.stdout.split('\n')
        for line in ping_output:
            stdout.critical('  ' + line)
    else:
        stdout.info(' PASSED: Host ' + host + ' responded...')

    return r.returncode


def main():

    try:
        while True:

            check_url(url)

            if not ok_status:
                
                hosts = ping_ips.split(",")
                for host in hosts:

                    check_ping(host)
                
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print_head('SimpleNetworkMonitor Exiting...')


def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(file_handler)
    l.addHandler(stream_handler)


if __name__ == '__main__':

    error_count = 0 
    ok_count    = 0
    iteration   = 0
    ok_status   = True

    config = configparser.ConfigParser()
    config.read('snetmon.cfg')
    
    # Read config values
    debug               = config.getboolean('debug', 'debug')
    gen_error           = config.getboolean('devel', 'gen_error')
    ok_int_report       = config.getint('default', 'ok_int_report')
    sleep_time_default  = config.getint('default', 'sleep_time_default')
    sleep_time_error    = config.getint('default', 'sleep_time_error')
    minutes             = config.getint('default', 'minutes')
    url                 = config.get('default', 'url')
    stdout_log          = config.get('default', 'stdout_log')
    ping_ips            = config.get('default', 'ping_ips')

    sleep_time = sleep_time_default

    setup_logger('stdout', stdout_log)
    stdout = logging.getLogger('stdout')

    # function calling
    print_head('SimpleNetworkMonitor Starting')    

    stdout.info(' ----------------------- SETTINGS -----------------------')
    stdout.info('        ok_count: ' + str(ok_count))
    stdout.info('   ok_int_report: ' + str(ok_int_report))
    stdout.info('     error_count: ' + str(error_count))
    stdout.info('      sleep_time: ' + str(sleep_time) + ' Seconds')
    stdout.info('sleep_time_error: ' + str(sleep_time_error) + ' Seconds')
    stdout.info('             url: ' + url)
    stdout.info('      stdout_log: ' + stdout_log)
    stdout.info('        ping_ips: ' + ping_ips)

    stdout.info(' ----------------- TESTING CONNECTIVTY ------------------')
    hosts = ping_ips.split(",")
    for host in hosts:
        check_ping(host)

    main()
