#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 26 10:09:22 2018

@author: sercinci
"""
import time, requests

BASE_URL = "http://0.0.0.0:8000/"

def main():
    run_action('bwready')
    run_action('fwready')
    go_forward()

def go_forward():
    run_action('fwstraight')
    run_action('forward')
    run_speed(100)
    time.sleep(5)
    run_action('stop')
    run_action('bwready')
    run_action('fwready')

def __request__(url, times=10):
	for x in range(times):
		try:
			requests.get(url)
			return 0
		except :
			print("Connection error, try again")
	print("Abort")
	return -1

def run_action(cmd):
	"""Ask server to do sth, use in running mode

	Post requests to server, server will do what client want to do according to the url.
	This function for running mode

	Args:
		# ============== Back wheels =============
		'bwready' | 'forward' | 'backward' | 'stop'

		# ============== Front wheels =============
		'fwready' | 'fwleft' | 'fwright' |  'fwstraight'

		# ================ Camera =================
		'camready' | 'camleft' | 'camright' | 'camup' | 'camdown'
	"""
	# set the url include action information
	url = BASE_URL + 'run/?action=' + cmd
	print('url: %s'% url)
	# post request with url 
	__request__(url)
    
def run_speed(speed):
	"""Ask server to set speed, use in running mode

	Post requests to server, server will set speed according to the url.
	This function for running mode.

	Args:
		'0'~'100'
	"""
	# Set set-speed url
	url = BASE_URL + 'run/?speed=' +str(speed)
	print('url: %s'% url)
	# Set speed
	__request__(url)

main()