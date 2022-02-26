from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import sys      # import sys for sys.exit()
import curses #curses library is used to get realtime keypress and time for sleep function
import AutoClaw
import threading


BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
PORT_MOTOR_LATERAL = BP.PORT_B
PORT_MOTOR_VERTICAL  = BP.PORT_C

stdscr = curses.initscr()	#initialize the curses object
curses.cbreak()			#to get special key characters 
stdscr.keypad(1)		#for getting values such as KEY_UP

BP.offset_motor_encoder(PORT_MOTOR_LATERAL, BP.get_motor_encoder(PORT_MOTOR_LATERAL))
BP.offset_motor_encoder(PORT_MOTOR_VERTICAL, BP.get_motor_encoder(PORT_MOTOR_VERTICAL))

def runArm():
    key = ''
    while key != ord('q'):		#press 'q' to quit from program
               
        key = stdscr.getch()	#get a character from terminal
        stdscr.refresh()
        
        #change the motor speed based on key value
        if key == curses.KEY_LEFT : 
            setMotorPower(PORT_MOTOR_LATERAL, -45)
        elif key == curses.KEY_RIGHT : 
            setMotorPower(PORT_MOTOR_LATERAL, 45)
        elif key == curses.KEY_UP :
            setMotorPower(PORT_MOTOR_VERTICAL , 45)
        elif key == curses.KEY_DOWN :
            setMotorPower(PORT_MOTOR_VERTICAL , -45)
    
        #After setting the motor speeds, send values to BrickPi
        time.sleep(.1)	#pause for 100 ms
    curses.endwin()
    BP.reset_all()

def setMotorPower(motor, speed):
    BP.set_motor_power(motor, speed)
    time.sleep(1) #Hold for 1 second before shutting off the motor
    BP.set_motor_power(motor, 0)

if __name__ == "__main__":
    ac = AutoClaw.AutoClaw()
    x = threading.Thread(target=runArm, args=())
    y = threading.Thread(target=ac.runClaw, args=())
    try:
          x.start()
          y.start()
    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
          BP.reset_all()
          curses.endwin()
