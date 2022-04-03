from Objects import Body
import json
from astropy import constants
import os
import numpy as np
import requests
import ssl, urllib3


class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)

#creates Dict that has the planets ID's to make the API call
planet_names = ["earth", "sun", "mercury", "jupiter", "mars", "venus", "saturn", "uranus", "neptune","moon"]
planet_commands = [399,10,199,599,499,299,699,799,899,301]
Planets = dict(zip(planet_names,planet_commands))


#Takes in a list of JSON Files, returns a list of "body" objects
def parse_objects(files):
    print(files)
    bodies = []
    for file in files:
        file = os.path.join("SimObjects", file + ".JSON")
        try:
            file_handler = open(file)
            data = json.load(file_handler)
            file_handler.close()
            print(f"Sucessfully opened {file}")
        except:
            print(f"Can't load {file}.")

        if data["mass"] == "<Find>":
            if data["name"] == "earth":
                print("Earth's mass not provided, pulling from Astropy")
                data["mass"] = constants.M_earth.value
            elif data["name"] == "sun":
                print("Sun's mass not provided, pulling from Astropy")
                data["mass"] = constants.M_sun.value

        if data["iposition"] == "<Find>":
            print(f"{data['name']}'s initial position not provided, pulling from JPL.")
            #determine planet ID
            planetID = Planets[data["name"]]
            #make API call to find iposition
            url = "https://ssd.jpl.nasa.gov/api/horizons.api?"
            #define parameters
            start_time = '2022-01-01'
            stop_time = '2022-01-02'
            #built url
            url += "format=json&EPHEM_TYPE=VECTORS&OBJ_DATA=YES&CENTER='500@10'"
            url += "&COMMAND='{}'&START_TIME='{}'&STOP_TIME='{}'".format(planetID,start_time,stop_time)

            session = requests.session()
            ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            ctx.options |= 0x4
            session.mount('https://', CustomHttpAdapter(ctx))
            response = session.get(url).json()
            result = response['result']
            data["iposition"] = np.array(initial_position(result),float)

        if data["ivelocity"] == "<Find>":
            print(f"{data['name']}'s initial velocity not provided, pulling from JPL.")
            #determine planet ID
            planetID = Planets[data["name"]]
            #make API call to find iposition
            url = "https://ssd.jpl.nasa.gov/api/horizons.api?"
            #define parameters
            start_time = '2022-01-01'
            stop_time = '2022-01-02'
            #built url
            url += "format=json&EPHEM_TYPE=VECTORS&OBJ_DATA=YES&CENTER='500@10'"
            url += "&COMMAND='{}'&START_TIME='{}'&STOP_TIME='{}'".format(planetID,start_time,stop_time)

            session = requests.session()
            ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            ctx.options |= 0x4
            session.mount('https://', CustomHttpAdapter(ctx))
            response = session.get(url).json()
            result = response['result']
            data["ivelocity"] = initial_velocity(result)

        ###################################################################################
        body = Body(data["name"], data["mass"], data["iposition"], data["ivelocity"])

        print(f"Successfully parsed {body.name}")

        bodies.append(body)

    return bodies

def parse_config(file):
    try:
        file_handler = open(file)
        data = json.load(file_handler)
        file_handler.close()
        print(f"Successfully loaded {file}")
    except:
        print(f"Couldn't load {file}")

    return data


#functions to parse the API output result string
def initial_position(string):
    #find index of first 'X = '
    idx = string.find('X =')
    new_string = string[idx:-1]
    #find first new line
    idx = new_string.find('\n')
    new_string = new_string[0:idx]

    #find starting index's for position values
    x_index = new_string.find('X =')
    y_index = new_string.find('Y =')
    z_index = new_string.find('Z =')
    

    xString = new_string[x_index:y_index].split('=')#might need to have conversion factor for units
    yString = new_string[y_index:z_index].split('=')
    zString = (new_string[z_index:-1] + new_string[-1]).split('=')

    xVal = float(xString[1]) * 10e2
    yVal = float(yString[1]) * 10e2
    zVal = float(zString[1]) * 10e2

    return [xVal,yVal,zVal]

def initial_velocity(string):
    #find index of first 'VX = '
    idx = string.find('VX=')
    new_string = string[idx:-1]
    #find first new line
    idx = new_string.find('\n')
    new_string = new_string[0:idx]

    #find starting index's for velocity values
    x_index = new_string.find('VX=')
    y_index = new_string.find('VY=')
    z_index = new_string.find('VZ=')

    xString = new_string[x_index:y_index].split('=')#might need to have conversion factor for units
    yString = new_string[y_index:z_index].split('=')
    zString = (new_string[z_index:-1] + new_string[-1]).split('=')

    xVal = float(xString[1]) * 10e2
    yVal = float(yString[1]) * 10e2
    zVal = float(zString[1]) * 10e2

    return [xVal,yVal,zVal]