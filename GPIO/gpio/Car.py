# import the necessary packages
from picamera import PiCamera
import RPi.GPIO as GPIO
import time, curses
import subprocess as sp, os


piccount = sp.check_output('ls -l ~/pics | grep -v ^l | wc -l', shell=True)
piccount = int(piccount) - 1
picname = "Pic"

#hardware work
GPIO.setmode(GPIO.BOARD)

MOTOR1B=18  #Left Motor
MOTOR1E=22

MOTOR2B=21  #Right Motor
MOTOR2E=19

GPIO.setup(MOTOR1B, GPIO.OUT)
GPIO.setup(MOTOR1E, GPIO.OUT)

GPIO.setup(MOTOR2B, GPIO.OUT)
GPIO.setup(MOTOR2E, GPIO.OUT)

def forward():
      GPIO.output(MOTOR1B, GPIO.HIGH)
      GPIO.output(MOTOR1E, GPIO.LOW)
      GPIO.output(MOTOR2B, GPIO.HIGH)
      GPIO.output(MOTOR2E, GPIO.LOW)
     
def reverse():
      GPIO.output(MOTOR1B, GPIO.LOW)
      GPIO.output(MOTOR1E, GPIO.HIGH)
      GPIO.output(MOTOR2B, GPIO.LOW)
      GPIO.output(MOTOR2E, GPIO.HIGH)
     
def rightturn():
      GPIO.output(MOTOR1B,GPIO.LOW)
      GPIO.output(MOTOR1E,GPIO.HIGH)
      GPIO.output(MOTOR2B,GPIO.HIGH)
      GPIO.output(MOTOR2E,GPIO.LOW)
     
def leftturn():
      GPIO.output(MOTOR1B,GPIO.HIGH)
      GPIO.output(MOTOR1E,GPIO.LOW)
      GPIO.output(MOTOR2B,GPIO.LOW)
      GPIO.output(MOTOR2E,GPIO.HIGH)

def stop():
      GPIO.output(MOTOR1E,GPIO.LOW)
      GPIO.output(MOTOR1B,GPIO.LOW)
      GPIO.output(MOTOR2E,GPIO.LOW)
      GPIO.output(MOTOR2B,GPIO.LOW)
      
def activateStream():
    #Stream video for VLC
    sp.call("raspivid -o - -t 0 -n --hflip --vflip | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' :demux=h264", shell=True)
    # allow the camera to warmup
    time.sleep(0.001)
 
def deactivateStream():
    sp.call("pkill vlc", shell=True);
    
def takePhoto():
    print piccount 
    picture = picname + str(piccount) + ".jpg"
    os.system("raspistill -q 100 -t 3000 -o ~/pics/" + picture)
    os.system("/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload ~/pics/" + picture + " " + picture) 
    piccount = piccount + 1



stdscr = curses.initscr()    #initialize the curses object
curses.cbreak()            #to get special key characters 
stdscr.keypad(1)        #for getting values such as KEY_UP
key = ''

while key != ord('q'):
    try:
        key = stdscr.getch()    #get a character from terminal
        if key == curses.KEY_UP :
            print "Running Forward"
            forward()
        elif key == curses.KEY_DOWN :
            print "Running Reverse"
            reverse()
        elif key == curses.KEY_RIGHT :
            print "Turning Right"
            rightturn()
        elif key == curses.KEY_LEFT :
            print "Turning Left"
            leftturn()
        elif key == ord('c') :
            activateStream()
        elif key == ord('d') :
            deactivateStream()
         
    except KeyboardInterrupt:            #Triggered by pressing Ctrl+C
        running = False                #Stop theread1
        print "Bye"
        break
    time.sleep(.1)    #pause for 100 ms

curses.endwin()
GPIO.cleanup() #free all the GPIO pins