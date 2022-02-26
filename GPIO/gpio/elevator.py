import RPi.GPIO as GPIO 
import time, Queue

 
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

#GPIO Setup for the buttons
BUTTON_ONE = 4
BUTTON_TWO = 17
BUTTON_THREE = 18

GPIO.setup(BUTTON_ONE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_TWO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_THREE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#GPIO setup for the LEDs
LED_ONE = 27
LED_TWO = 22
LED_THREE = 23

GPIO.setup(27, GPIO.OUT) #Floor 1
GPIO.setup(22, GPIO.OUT) #Floor 2
GPIO.setup(23, GPIO.OUT) #Floor 3

#GPIO setup for the alphanumeric LED
GPIO.setup(5, GPIO.OUT) #Top 
GPIO.setup(6, GPIO.OUT) #Top
GPIO.setup(13, GPIO.OUT) #Top
GPIO.setup(12, GPIO.OUT) #Bottom
GPIO.setup(19, GPIO.OUT) #Bottom
GPIO.setup(16, GPIO.OUT) #Bottom
GPIO.setup(26, GPIO.OUT) #Bottom

#Buzzer
GPIO.setup(21, GPIO.OUT)

floorQ = Queue.Queue()


oneNumeric=[[0,0,0,1],[0,0,0,1]]
twoNumeric=[[0,1,1,1],[1,1,1,0]]
threeNumeric=[[0,1,1,1],[0,1,1,1]]


def activateNumericLED(numeric):
    GPIO.output(5, numeric[0][1])
    GPIO.output(6, numeric[0][2])
    GPIO.output(13, numeric[0][3])
   
    GPIO.output(12, numeric[1][0])
    GPIO.output(19, numeric[1][1])
    GPIO.output(16, numeric[1][2])
    GPIO.output(26, numeric[1][3]) 

def updateNumeric(floorNumber):
    if floorNumber == 1:
        activateNumericLED(oneNumeric)
    elif floorNumber == 2:
        activateNumericLED(twoNumeric)
    elif floorNumber == 3:
        activateNumericLED(threeNumeric)

def updateLED(floorNumber):
    if floorNumber == 1:
        GPIO.output(LED_ONE, 1) 
        GPIO.output(LED_TWO, 0) 
        GPIO.output(LED_THREE, 0) 
    elif floorNumber == 2:
        GPIO.output(LED_ONE, 0)
        GPIO.output(LED_TWO, 1) 
        GPIO.output(LED_THREE, 0)  
    elif floorNumber == 3:
        GPIO.output(LED_ONE, 0)
        GPIO.output(LED_TWO, 0) 
        GPIO.output(LED_THREE, 1)  

def runBuzzer():
    period = 1.0 / 400     #the period (sec/cyc) is the inverse of the frequency (cyc/sec)
    delay = period / 2     #calcuate the time for half of the wave

    cycles = int(1 * 400)  #the number of waves to produce is the duration(in seconds) times the frequency

    for num in range(cycles):
       GPIO.output(21, True)   #set pin 18 to high
       time.sleep(delay)    #wait with pin 18 high
       GPIO.output(21, False)    #set pin 18 to low
       time.sleep(delay)    #wait with pin 18 low

 
def switchfloor(floor, currentFloor):   
   
    while currentFloor != floor :
        if currentFloor < floor:
            currentFloor += 1
            time.sleep(3)
            updateLED(currentFloor)
            updateNumeric(currentFloor)
        
        if currentFloor > floor:
            currentFloor -= 1
            time.sleep(3)
            updateLED(currentFloor)
            updateNumeric(currentFloor)
   
    if currentFloor == floor:
	runBuzzer()

    return currentFloor
    
    
currentFloor = 1    
updateLED(currentFloor)
updateNumeric(currentFloor)


while True:
    input_state_one = GPIO.input(BUTTON_ONE)
    input_state_two = GPIO.input(BUTTON_TWO)
    input_state_three = GPIO.input(BUTTON_THREE)
    if input_state_one == False:
        floorQ.put(1)
        time.sleep(0.2)
     
    if input_state_two == False:
        floorQ.put(2)
        time.sleep(0.2)
     
    if input_state_three == False:
	floorQ.put(3)
        time.sleep(0.2)
    
    while not floorQ.empty():
        currentFloor = switchfloor(floorQ.get(), currentFloor)
