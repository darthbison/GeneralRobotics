#!/usr/bin/env python
 
import RPi.GPIO as GPIO, time 
 
GPIO.setmode(GPIO.BCM)
BUTTON_IN = 22
GPIO.setup(BUTTON_IN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

 
while True:
	input_state = GPIO.input(BUTTON_IN)
	if input_state == False:
		print('Button Pressed')
	  	time.sleep(0.2)

	
