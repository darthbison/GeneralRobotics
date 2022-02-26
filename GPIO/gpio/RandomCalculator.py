#!/usr/bin/env python
 
import RPi.GPIO as GPIO, random, time 
 
DEBUG = 1
 
 
DO_CALC_FREQ = 3      # check mail every 10 seconds
GPIO.cleanup() 
GPIO.setmode(GPIO.BCM)
GREEN_LED = 23
RED_LED = 18
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)

RESULT = 0
 
while (RESULT < 1000):

        VALUE_ONE = random.randint(10,20)
        VALUE_TWO = random.randint(10,50) 
        RESULT = VALUE_ONE * VALUE_TWO
        print "Result of Value One:", VALUE_ONE, " and Value Two:", VALUE_TWO, "is: ", RESULT 
        if RESULT < 200 and RESULT > 100:
		print "Green"
                GPIO.output(GREEN_LED, True)
                GPIO.output(RED_LED, False)
        elif RESULT < 400 and RESULT > 300:
		print "Red"
                GPIO.output(GREEN_LED, False)
                GPIO.output(RED_LED, True)
        else:
		print "Off"
		GPIO.output(GREEN_LED, False)
                GPIO.output(RED_LED, False)

        if RESULT > 1000:
        	print "Done!" 
        	GPIO.output(GREEN_LED, False)
        	GPIO.output(RED_LED, False)
        
        time.sleep(DO_CALC_FREQ)
