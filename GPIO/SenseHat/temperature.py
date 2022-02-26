from sense_hat import SenseHat

sense = SenseHat()
sense.clear()

temp = sense.get_temperature()
FTemp = (temp * (9/5)) + 32

print(FTemp)
