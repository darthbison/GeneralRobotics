#!/usr/bin/python
import csv,json



def gp(directory):
	# Open the CSV  
        fileName=directory + "WeatherLog.csv"
        fieldnames=["time","temperature","humidity","pressure"]

        f = open( fileName, 'rU' )  
        # Change each fieldname to the appropriate field name. I know, so difficult.  
        reader = csv.DictReader(f, fieldnames)  

        # Parse the CSV into JSON  
        out = json.dumps( [ row for row in reader ] )  
        print "JSON parsed!"  
        # Save the JSON  
        f = open( "test.json", 'w')  
        f.write(out)  
        f.close()
        print "JSON saved!"  


if __name__ == "__main__":
    gp("/home/pi/telemetry/logs/")

