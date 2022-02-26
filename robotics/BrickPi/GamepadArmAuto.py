import time,pygame,math,sys	
import brickpi3 # import the BrickPi3 drivers
import AutoClaw
import threading

pygame.init()

# Initialize the joysticks
pygame.joystick.init()

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.


PORT_MOTOR_LATERAL = BP.PORT_B
PORT_MOTOR_VERTICAL  = BP.PORT_C
#PORT_MOTOR_CLAW = BP.PORT_A

BP.offset_motor_encoder(PORT_MOTOR_LATERAL, BP.get_motor_encoder(PORT_MOTOR_LATERAL))
BP.offset_motor_encoder(PORT_MOTOR_VERTICAL, BP.get_motor_encoder(PORT_MOTOR_VERTICAL))
#BP.offset_motor_encoder(PORT_MOTOR_CLAW, BP.get_motor_encoder(PORT_MOTOR_CLAW))


def runArm():
    while True:

        #BP.reset_all()

        # EVENT PROCESSING STEP
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop

        # Get count of joysticks
        joystick_count = pygame.joystick.get_count()

        # For each joystick:
        for k in range(joystick_count):
            joystick = pygame.joystick.Joystick(k)
            joystick.init()

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other.
            axes = joystick.get_numaxes()

            for i in range( axes ):
                axis = joystick.get_axis( i )
                realAxis = math.ceil(axis);
                if i == 0 :
                    if realAxis == -1 :
                        setMotorPower(PORT_MOTOR_LATERAL, -45)
                    if realAxis == 1 :
                        setMotorPower(PORT_MOTOR_LATERAL, 45)
                elif i == 1 :
                    if realAxis == -1 :
                        setMotorPower(PORT_MOTOR_VERTICAL , 45)
                    if realAxis == 1 :
                        setMotorPower(PORT_MOTOR_VERTICAL , -45)

            buttons = joystick.get_numbuttons()
            for j in range( buttons ):
                button = joystick.get_button( j )
                if j == 3 :
                    if button == 1 :
                        BP.reset_all()
                        sys.exit(0)


        #After setting the motor speeds, send values to BrickPi
        time.sleep(.1)    #pause for 100 ms

        
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
          
    
