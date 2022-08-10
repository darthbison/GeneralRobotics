#!/usr/bin/env python
 
import RPi.GPIO as GPIO, random, time 
from Adafruit_LED_Backpack import SevenSegment
 
DEBUG = 1
 
DO_CALC_FREQ = 3    
GPIO.setmode(GPIO.BCM)

segment = SevenSegment.SevenSegment(address=0x70)

# Initialize the display. Must be called once before using the display.
segment.begin()

RESULT = 0

stored_values_thousandths = {
  1: 0, # ones spot
  2: 0, # tens spot
  3: 0, # hundreds spot
  4: 0 # thousandths spot
}

def main():
        try:
                while True:

                        VALUE_ONE = random.randint(10,20)
                        VALUE_TWO = random.randint(10,20) 
                        RESULT = VALUE_ONE * VALUE_TWO
                        
                        for enum, value in enumerate(str(RESULT)[::-1], 1):
                                stored_values_thousandths[enum] = int(value)


                        print ("Result of Value One:", VALUE_ONE, " and Value Two:", VALUE_TWO, "is: ", RESULT)
                        
                        segment.set_digit(1 , stored_values_thousandths[3])
                        segment.set_digit(2 , stored_values_thousandths[2])
                        segment.set_digit(3 , stored_values_thousandths[1])

                        segment.write_display()
                        
                        time.sleep(DO_CALC_FREQ)
        except KeyboardInterrupt:
                segment.clear()
                segment.write_display()
                GPIO.cleanup() 

if __name__ == "__main__":
    main()
