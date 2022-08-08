#!/usr/bin/env python

import RPi.GPIO as GPIO
import random
import time, sys

DO_CALC_FREQ = 2      # move nodes every 2 seconds

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)


PLAYER_ONE = 0
PLAYER_TWO = 0

ledDict = {0: 26, 1: 25}


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
        print("Node: ", pos, " has ", neighbors, " neighbors")
        resultDict[pos] = neighbors
        pos = pos + 1
        activateLED(resultDict)
    

def activateLED(resultMap):
    for node in resultMap.keys():
        result = resultMap[node]
        
        if (result < 1):
            #print("Node ", node, " is dead.")
            gpValue = ledDict[node]
            GPIO.output(gpValue, False)
        else:
            #print("Node ", node, " is alive.")
            gpValue = ledDict[node]
            GPIO.output(gpValue, True)
    

def main():
    while True:
        try:
            PLAYER_ONE = random.randint(0, 10)
            PLAYER_TWO = random.randint(0, 10)
            
            myList = [PLAYER_ONE, PLAYER_TWO]
            generateMap(myList)
            time.sleep(DO_CALC_FREQ)
        except KeyboardInterrupt:
            GPIO.cleanup()
            sys.exit()

if __name__ == "__main__":
    main()
