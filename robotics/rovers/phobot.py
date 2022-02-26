#!/usr/bin/env python

import requests

#Code for handling the data sent from the webpage
class WSHandler():
    
    def open(self):
        print ("connection opened...")
        
    def check_origin(self,origin):
        return True
    def execute_message(self, message):      # receives the data from the webpage and is stored in the variable message
        
        accessToken = ""
        deviceID = ""
        controlURL = "https://api.spark.io/v1/devices/" + deviceID + "/control"
        
        # prints the revived from the webpage 
        if message == "u":                # checks for the received data and assigns different values to c which controls the movement of robot.
            c = "8"
        if message == "d":
            c = "2"
        if message == "l":
            c = "6"
        if message == "r":
            c = "4"
        if message == "s":
            c = "5"
        
        if c == '8' :
            requests.post(controlURL, data = {'params':'F-100', 'access_token' : accessToken})
            
        elif c == '2' :
            requests.post(controlURL, data = {'params':'B-75', 'access_token' : accessToken})
            
        elif c == '6' :
            requests.post(controlURL, data = {'params':'L-50', 'access_token' : accessToken})
            
        elif c == '4' :
            requests.post(controlURL, data = {'params':'R-50', 'access_token' : accessToken})
        
        elif c == '5' :
            requests.post(controlURL, data = {'params':'S', 'access_token' : accessToken})
     
    def on_close(self):
        print ("connection closed...")

      

  

