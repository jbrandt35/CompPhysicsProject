import json
import requests


url = "https://ssd.jpl.nasa.gov/api/horizons.api?"
#define parameters
start_time = '2022-01-01'
stop_time = '2022-01-02'
planetID = 'MB'
#built url
url += "format=json&EPHEM_TYPE=VECTORS&OBJ_DATA=YES&CENTER='500@0'"
url += "&COMMAND='{}'&START_TIME='{}'&STOP_TIME='{}'".format(planetID,start_time,stop_time)

response = requests.get(url).json()
print(response)