#!/usr/bin/env python
 
import RPi.GPIO as GPIO
import os, time
import sys
import csv
import Adafruit_DHT 

temp_sensor = 11
sound_sensor = 24 
motion_sensor = 23 

pin = 4

namecounter = 0
threshold = 1024 * (10 ^ 3) #1 megabyte

def init():
         GPIO.setwarnings(False)
         GPIO.setmode(GPIO.BCM)
         GPIO.setup(sound_sensor,GPIO.IN,pull_up_down=GPIO.PUD_UP)
         GPIO.setup(motion_sensor,GPIO.IN)
         pass

def getTempInFarenheit(celsius):
  FTemp = (celsius * 1.8) + 32
  return FTemp

def fileWrite(message):
  global namecounter
  filename = "/mnt/pnydisk/data/" + "mjbasement_" + str(namecounter) + ".csv"
  datafile = open(filename, "a+")

  filesize = os.stat(filename).st_size #in bytes
  if (filesize < threshold):
     datafile.write(message) 
  else:
     namecounter = namecounter + 1
     datafile.close()

def main():
  # Main program block
  
  motionValue = 0
  soundValue = 0
  message = ""
  print("Collecting sound and motion data...")
  while True:
        #humidity, temperature = Adafruit_DHT.read_retry(temp_sensor,pin) 

        current_milli_time = int(round(time.time() * 1000))
         
        if (GPIO.input(motion_sensor) == 1):
              motionValue = 1
        else:
              motionValue = 0

        if (GPIO.input(sound_sensor)==GPIO.LOW):
              soundValue = 1
        else:
              soundValue = 0 
        time.sleep(0.1)

        message = ""
        #message += str(getTempInFarenheit(temperature)) + ","
        #message += str(humidity) + ","
        message += str(motionValue) + ","
        message += str(soundValue) + ","
        message += str(current_milli_time) + "\n" 
        #print(message)

        fileWrite(message)
        time.sleep(2)

if __name__ == '__main__':

  try:
    init()
    main()
  except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
