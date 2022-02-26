from flask import Flask
import csv,json

app = Flask(__name__)


def gp(directory):
        # Open the CSV
        fileName=directory + "WeatherLog.csv"
        fieldnames=["time","temperature","humidity","pressure"]

        f = open( fileName, 'rU' )
        # Change each fieldname to the appropriate field name. I know, so difficult.
        reader = csv.DictReader(f, fieldnames)

        # Parse the CSV into JSON
        out = json.dumps( [ row for row in reader ] )
        return out 


@app.route('/tempJSON')
def tempJSON():
    json = gp("/home/pi/logs/")
    return json 

if __name__ == '__main__': 
   app.run(host='0.0.0.0',debug=True)
