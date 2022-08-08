#!/usr/bin/env python
 
import RPi.GPIO as GPIO
import os, time
import csv
import dht11

temp_sensor = 18
sound_sensor = 12
motion_sensor = 26

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
  filename = "data/" + "mjbasement_" + str(namecounter) + ".csv"
  datafile = open(filename, "a+")

  filesize = os.stat(filename).st_size #in bytes
  if (filesize < threshold):
     datafile.write(message) 
  else:
     namecounter = namecounter + 1
     datafile.close()

def main():
  # Main program block
  
  instance = dht11.DHT11(pin = temp_sensor)
  motionValue = 0
  message = ""
  while True:
        #get DHT11 sensor value
        result = instance.read()
        current_milli_time = int(round(time.time() * 1000))
         
        if GPIO.input(motion_sensor):
              motionValue = 1
        else:
              motionValue = 0

        message = ""
        message += str(getTempInFarenheit(result.temperature)) + ","
        message += str(result.humidity) + ","
        message += str(motionValue) + ","
        message += str(current_milli_time) + "\n" 
        fileWrite(message)
        time.sleep(2)

if __name__ == '__main__':

  try:
    init()
    main()
  except KeyboardInterrupt:
    GPIO.cleanup()
    pass
