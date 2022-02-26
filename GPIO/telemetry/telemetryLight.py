#!/usr/bin/python
import os,sys
import time
import gpsd, movement
import temperature as temp
import humidity as hum
import datetime  

def hmsToSeconds(time):
  actualTime = time.split(".")
  h, m, s = [int(i) for i in actualTime[0].split(':')]
  return 3600*h + 60*m + s

def generateData(message):
    fix = gpsd.getGPS()
    
    t = str(fix.TPV["time"])
    time = t.split("T") 

    speedVal = str(fix.TPV["speed"])
    altVal = str(fix.TPV["alt"])
    latVal = str(fix.TPV["lat"])
    longVal = str(fix.TPV["lon"])

    message += time[1] + "," + speedVal + "," 
    message += altVal + "," + latVal + "," + longVal 
    return message

def gp(directory):
        ts = time.time()
        dateFileString = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M')
        fileName=directory + dateFileString + "_TelemetryLog.csv"

        fd = open(fileName, "w+")
        fd.write("time,speed,altitude,latitude,longitude\n")
        fd.close()

        while True:        
           message = ""
           message = generateData(message)

           with open(fileName, "a") as myfile:
             myfile.write(message +"\n")


gp("/home/pi/telemetry/logs/")

