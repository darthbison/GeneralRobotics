from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import numpy as np

class AutoClaw:
    def __init__(self):
        self.BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
        self.PORT_MOTOR_CLAW = self.BP.PORT_A
        self.threshold = 0
        self.hasItem = False
        
    
    def runClaw(self):
        self.BP.offset_motor_encoder(self.PORT_MOTOR_CLAW, self.BP.get_motor_encoder(self.PORT_MOTOR_CLAW))
        self.BP.set_sensor_type(self.BP.PORT_1, self.BP.SENSOR_TYPE.NXT_LIGHT_ON)
        while True:
            try:
                    lightvalue = self.BP.get_sensor(self.BP.PORT_1)

                    if self.threshold == 0:
                        self.threshold = self.getLightAverage(lightvalue)
                    
                    if lightvalue >= self.threshold:
                        self.hasItem = False

                    if self.hasItem == False:
                        if lightvalue < self.threshold:
                            self.BP.set_motor_power(self.PORT_MOTOR_CLAW , 25)
                            time.sleep(2) #Hold item for two seconds
                            self.hasItem = True
                        elif lightvalue > self.threshold:
                            self.BP.set_motor_power(self.PORT_MOTOR_CLAW , -25)
                        
                    if self.hasItem & lightvalue < self.threshold:
                        self.BP.set_motor_power(self.PORT_MOTOR_CLAW , -25)

            except brickpi3.SensorError as error:
                    print(error)

    def getLightAverage(self, lightvalue):
        count = 0
        lightValues = []
        while count <= 10:
            if count == 10:
                return np.average(lightValues) - 200  
            else:  
                lightValues.append(lightvalue)
                count = count + 1
  
