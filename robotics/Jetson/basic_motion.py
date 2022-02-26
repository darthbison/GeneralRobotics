#!/usr/bin/env python

from jetbot import Robot
import time
from jetbot import Heartbeat


robot = Robot()
heartbeat = Heartbeat()

# this function will be called when heartbeat 'alive' status changes
def handle_heartbeat_status(change):
    if change['new'] == Heartbeat.Status.dead:
        robot.stop()
        
heartbeat.observe(handle_heartbeat_status, names='status')

robot.left(speed=0.3)
robot.stop()


robot.left(0.3)
time.sleep(0.5)
robot.stop()



robot.set_motors(0.3, 0.6)
time.sleep(1.0)
robot.stop()



robot.left_motor.value = 0.3
robot.right_motor.value = 0.6
time.sleep(1.0)
robot.left_motor.value = 0.0
robot.right_motor.value = 0.0