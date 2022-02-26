from sense_hat import SenseHat

import time

sense = SenseHat()

sense.load_image("/home/pi/pics/Kirby.png")
time.sleep(6)
sense.clear()
