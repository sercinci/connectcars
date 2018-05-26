#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import time, requests
import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BCM)
 
# Declaration of the input pin which is connected with the sensor.
GPIO_PIN = 20
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
 
# Break between the results will be defined here (in seconds)
delayTime = 0.1

BASE_URL = "http://0.0.0.0:8000/"

 # Set speed content, and speed level content
MAX_SPEED = 100
MIN_SPEED = 40
SPEED_LEVEL_1 = MIN_SPEED
SPEED_LEVEL_2 = (MAX_SPEED - MIN_SPEED) / 4 * 1 + MIN_SPEED
SPEED_LEVEL_3 = (MAX_SPEED - MIN_SPEED) / 4 * 2 + MIN_SPEED
SPEED_LEVEL_4 = (MAX_SPEED - MIN_SPEED) / 4 * 3 + MIN_SPEED
SPEED_LEVEL_5 = MAX_SPEED
SPEED = [0, SPEED_LEVEL_1, SPEED_LEVEL_2, SPEED_LEVEL_3, SPEED_LEVEL_4, SPEED_LEVEL_5]

LED_ROUGE = 5
LED_VERTE = 9
LED_BLEUE = 10
   
GPIO.setup(LED_ROUGE, GPIO.OUT, initial= GPIO.LOW)
GPIO.setup(LED_VERTE, GPIO.OUT, initial= GPIO.LOW)
GPIO.setup(LED_BLEUE, GPIO.OUT, initial= GPIO.LOW)

distance_btw_cars = 50
def main():
    run_action('bwready')
    run_action('fwready')
    go_forward(2)
    turn_right()
    time.sleep(1)
    run_action('stop')
    run_action('bwready')
    run_action('fwready')
    GPIO.output(LED_ROUGE,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(LED_ROUGE,GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(LED_ROUGE,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(LED_ROUGE,GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(LED_ROUGE,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(LED_ROUGE,GPIO.LOW)
    GPIO.cleanup()
    
def go_forward(duration):
    """
    Takes into argument the duration of the going forward movement
    """
    """
    t0 = time.clock()
    now = t0
    diff = now -t0
    run_action('fwstraight')
    run_action('forward')
    while (diff < duration):
        now = time.clock()
        diff = now - t0
    """
    # main program loop
    run_action('fwstraight')
    run_speed(50)
    run_action('forward')
    run_speed(50)
    while (GPIO.input(GPIO_PIN) == True):
            time.sleep(delayTime)
 

def increase_speed(i):
    run_speed(SPEED[i])
    """ 
    Send Broadcast Message
    """
    run_action('forward')
    time.sleep(3)
    #run_action('stop')
    
def turn_right():
    run_speed(MAX_SPEED)
    run_action('fwright')
    time.sleep(1)
    run_action('fwright')
    #run_speed(MIN_SPEED)
    run_action('fwleft')
    time.sleep(1)
    run_action('fwleft')
    run_action('fwright')
    run_action('fwright')
    run_action('fwstraight')
    #run_action('forward')
    #run_action('stop')


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
