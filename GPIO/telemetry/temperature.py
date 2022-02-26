
def getTempInCelsius(sense):
  temp = sense.get_temperature()
  return temp

def getTempInKelvin(sense):
  temp = sense.get_temperature()
  KTemp = temp + 273
  return KTemp

def getTempInFarenheit(sense):
  temp = sense.get_temperature()
  FTemp = (temp * (9/5)) + 32
  return FTemp
