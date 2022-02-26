#!/usr/bin/python
from sense_hat import SenseHat
import os,sys
import temperature as temp
import humidity as hum
import csv,json
import datetime  
from time import gmtime, strftime


sense = SenseHat()
sense.show_message("starting...")
sense.clear()  # Blank the LED matrix


def generateCSVData(message):


    temperature = str(temp.getTempInFarenheit(sense))
    humidity = str(hum.getHumidity(sense))

    tmp = sense.get_temperature()
    pressure = sense.get_pressure()
    pressure = round(pressure, 1)

    message = []
    message.append(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ",")
    message.append(str(temperature) + ",")
    message.append(str(humidity) + ",")
    message.append(str(pressure))

    return "".join(message)


def gp(directory):
        dateFileString = strftime('%Y%m%d_%H%M', gmtime())
        fileName=directory + "WeatherLog.csv"

        while True:        
           csvData = ""
           csvData = generateCSVData(csvData)
           #writeJson(csv, fileName, "")   

           with open(fileName, "a") as myfile:
             myfile.write(csvData+"\n")


if __name__ == "__main__":
    gp("/home/pi/logs/")

