import RPi.GPIO as GPIO 
import time
import Queue as queue
from Adafruit_LED_Backpack import SevenSegment
 
GPIO.setmode(GPIO.BCM)

#GPIO Setup for the buttons
BUTTON_ONE = 25 
BUTTON_TWO = 26 
BUTTON_THREE = 19 

buzzer_pin = 18

GPIO.setup(BUTTON_ONE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_TWO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_THREE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Buzzer
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.output(buzzer_pin, GPIO.LOW)

segment = SevenSegment.SevenSegment(address=0x70)

# Initialize the display. Must be called once before using the display.
segment.begin()

floorQ = queue.Queue()

def updateNumeric(floorNumber):
    if floorNumber == 1:
         segment.set_digit(3, 1)
    elif floorNumber == 2:
         segment.set_digit(3, 2) 
    elif floorNumber == 3:
         segment.set_digit(3, 3) 
    segment.write_display()

def runBuzzer():
    # Make buzzer sound
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(0.3)
    # Stop buzzer sound
    GPIO.output(buzzer_pin, GPIO.LOW)
    time.sleep(0.3)
 
def switchfloor(floor, currentFloor):   
   
    while currentFloor != floor:
        if currentFloor < floor:
            currentFloor += 1
            time.sleep(3)
            updateNumeric(currentFloor)
        
        if currentFloor > floor:
            currentFloor -= 1
            time.sleep(3)
            updateNumeric(currentFloor)
   
    if currentFloor == floor:
         runBuzzer()
         return currentFloor
    

def main():
    try:
        currentFloor = 1
        updateNumeric(currentFloor)
        while True:
            input_state_one = GPIO.input(BUTTON_ONE)
            input_state_two = GPIO.input(BUTTON_TWO)
            input_state_three = GPIO.input(BUTTON_THREE)
            if input_state_one == False:
                print("One")
                floorQ.put(1)
                time.sleep(0.2)
            
            if input_state_two == False:
                print("Two")
                floorQ.put(2)
                time.sleep(0.2)
            
            if input_state_three == False:
                print("Three")
                floorQ.put(3)
                time.sleep(0.2)
        
            while not floorQ.empty():
                currentFloor = switchfloor(floorQ.get(), currentFloor)
    except KeyboardInterrupt:
         segment.clear()
         segment.write_display()
         GPIO.cleanup() 

if __name__ == "__main__":
    main()
