from time import sleep
import gpsdSocket

def getGPS():
	
        the_connection = gpsdSocket.GPSDSocket()
	the_fix = gpsdSocket.Fix()

	finalLat = 0
	finalLong = 0

	try:
    	   for new_data in the_connection:
              if new_data:
                the_fix.refresh(new_data)
              if not isinstance(the_fix.TPV['lat'], str):  #data check

                return the_fix
                #sleep(1)
	except KeyboardInterrupt:
           the_connection.close()
           print("\nTerminated by user\nGood Bye.\n")
