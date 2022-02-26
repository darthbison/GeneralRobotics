from sense_hat import SenseHat
import math

def runTempHumidity():

	sense = SenseHat()
	sense.clear()

	temp = sense.get_temperature()
	FTemp = (temp * (9/5)) + 32
	FTemp = math.ceil(FTemp)


	humidity = sense.get_humidity()
	humidity = math.ceil(humidity)

	sense.show_message("Temp: " + str(FTemp) + " degrees F - Humidity: " + str(humidity) + "%")

