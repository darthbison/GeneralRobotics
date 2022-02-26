#!/usr/bin/env python
 
import RPi.GPIO as GPIO, random, time 
 
DO_CALC_FREQ = 3      # move nodes every 3 seconds
GPIO.cleanup() 
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

PLAYER_ONE = 0
PLAYER_TWO = 0
PLAYER_THREE = 0
PLAYER_FOUR = 0
PLAYER_FIVE = 0
PLAYER_SIX = 0

ledDict = {0:17,1:22,2:18,3:23,4:24,5:25}

def generateMap(nodes):
	node = 0
        valueDict = {}
	for nodeValue in nodes:
	        valueDict[node] = nodeValue 	
		node = node + 1
 	checkStatus(valueDict)

def checkStatus(valueMap):
        pos = 0
        resultDict = {}
	for node in valueMap.keys():
            	curValue = valueMap[pos]
                neighbors = 0
		for nValue in valueMap.keys():
		    if pos != nValue:
                       otherValue = valueMap[nValue]
		       if (curValue - 1 == otherValue):
			  neighbors = neighbors + 1
                       elif (curValue + 1 == otherValue):
		          neighbors = neighbors + 1 
		       elif (otherValue == curValue):
			  neighbors = neighbors + 1
                print "Node: ",pos, " has ",neighbors," neighbors"        	
                resultDict[pos] = neighbors
                pos = pos + 1 
        activateLED(resultDict) 

def activateLED(resultMap):
   for node in resultMap.keys():
       result = resultMap[node]
       if (result < 2) | (result > 2):
         print "Node ", node, " is dead."
         gpValue = ledDict[node]
         GPIO.output(gpValue, False)  
       else:
         print "Node ", node, " is alive."
         gpValue = ledDict[node]
         GPIO.output(gpValue, True)
   print "***************************"

while True:
        PLAYER_ONE = random.randint(0,10)
	PLAYER_TWO = random.randint(0,10)
	PLAYER_THREE = random.randint(0,10)
	PLAYER_FOUR = random.randint(0,10)
	PLAYER_FIVE = random.randint(0,10)
	PLAYER_SIX = random.randint(0,10)
        myList=[PLAYER_ONE,PLAYER_TWO,PLAYER_THREE,PLAYER_FOUR,PLAYER_FIVE,PLAYER_SIX]
        generateMap(myList) 
        time.sleep(DO_CALC_FREQ)
