from sense_hat import SenseHat
import time
sense = SenseHat()

r = 255
g = 0 
b = 255

sense.clear((r, g, b)) 
time.sleep(5)
sense.clear()
