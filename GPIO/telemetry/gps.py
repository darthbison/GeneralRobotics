import serial
import time, datetime, os

firstFixFlag = False # this will go true after the first GPS fix.
firstFixDate = ""
firstFixTime = ""



def getGPSData(directory, data):
   
   ts = time.time()
   dateFileString = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M')

   while True:
                with open(directory + dateFileString + "_GPSLog.txt", "a") as myfile:
                    myfile.write(data +"\n")

