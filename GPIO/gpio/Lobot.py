import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

GPIO.setup(11, GPIO.IN)
GPIO.setup(5, GPIO.IN)

while True:
    input_state1 = GPIO.input(11)
    input_state2 = GPIO.input(5)
    if input_state1 == True:
        print('Option 1')
        time.sleep(0.2)
    if input_state2 == True:
        print('Option 2')
        time.sleep(0.2)