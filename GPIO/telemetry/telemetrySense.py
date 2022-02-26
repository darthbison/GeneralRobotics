#!/usr/bin/python
from sense_hat import SenseHat
import os,sys
import time
import gpsd, movement
import temperature as temp
import humidity as hum
import datetime  

sense = SenseHat()
sense.show_message("starting...")
sense.clear()  # Blank the LED matrix

seaLevelPressure = 1013.25
coefficient = 0.0065


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

    temperature = str(temp.getTempInFarenheit(sense))
    humidity = str(hum.getHumidity(sense))

    tmp = sense.get_temperature()
    pressure = sense.get_pressure()
    pressure = round(pressure, 1)

    #Hyposometric equation
    try:
        baromAltitude = ((seaLevelPressure/pressure)**(1/5.257) - 1) * (tmp + 273.15)/ coefficient
    except ZeroDivisionError:
        baromAltitude = 0.0

    message += time[1] + "," + speedVal + "," 
    message += altVal + "," + latVal + "," + longVal 
    message += "," + str(movement.getRoll(sense)) + "," + str(movement.getPitch(sense))
    message += "," + str(movement.getYaw(sense))
    message += "," + temperature
    message += "," + humidity
    message += "," + str(baromAltitude)
    return message

def gp(directory):
        ts = time.time()
        dateFileString = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M')
        fileName=directory + dateFileString + "_TelemetryLog.csv"

        fd = open(fileName, "w+")
        fd.write("time,speed,gpsAltitude,latitude,longitude,roll,pitch,yaw,temperature,humidity,barometricAltitude\n")
        fd.close()

        while True:        
           message = ""
           message = generateData(message)

           with open(fileName, "a") as myfile:
             myfile.write(message +"\n")


gp("/home/pi/telemetry/logs/")

