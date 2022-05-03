from Objects import Body
import json
from astropy import constants
import os
import numpy as np
import requests
import ssl
import urllib3


####################################################################

class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)

# This code is from: https://stackoverflow.com/questions/71603314/ssl-error-unsafe-legacy-renegotiation-disabled
####################################################################


#Takes in a list of JSON Files, returns a list of "body" objects
def parse_objects(settings):
    files = settings["Planets"]
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

        if "<Find>" in data.values():

            api_call = call_api(data, settings)

            if data["iposition"] == "<Find>":
                print(f"{data['name']}'s initial position not provided, pulling from JPL.")
                data["iposition"] = np.array(get_initial_condition("position", api_call), float)

            if data["ivelocity"] == "<Find>":
                print(f"{data['name']}'s initial velocity not provided, pulling from JPL.")
                data["ivelocity"] = np.array(get_initial_condition("velocity", api_call), float)

            if data["mass"] == "<Find>":
                if data["name"] == "sun":
                    print("Sun's mass not provided, pulling from Astropy")
                    data["mass"] = constants.M_sun.value
                elif data["name"] == "earth":
                    print("Earth's mass not provided, pulling from Astropy")
                    data["mass"] = constants.M_earth.value
                else:
                    print(f"{data['name']}'s mass not provded, pulling from JPL")
                    data["mass"] = get_mass(api_call)

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

#type = "velocity" or "position"
def get_initial_condition(type, string):
    if type == "velocity":
        code_1, code_2 = "V", ""
    else:
        code_1, code_2 = "", " "

    #find index of first 'VX = '
    idx = string.find(f'{code_1}X{code_2}=')
    new_string = string[idx:-1]
    #find first new line
    idx = new_string.find('\n')
    new_string = new_string[0:idx]

    x_index = new_string.find(f'{code_1}X{code_2}=')
    y_index = new_string.find(f'{code_1}Y{code_2}=')
    z_index = new_string.find(f'{code_1}Z{code_2}=')

    xString = new_string[x_index:y_index].split('=')#might need to have conversion factor for units
    yString = new_string[y_index:z_index].split('=')
    zString = (new_string[z_index:-1] + new_string[-1]).split('=')

    return (10**3) * np.array([float(xString[1]), float(yString[1]), float(zString[1])])

def call_api(data, settings):
    date = settings["Ephemeris Date"]
    planetID = data["Horizon ID"]

    # make API call to find iposition
    url = "https://ssd.jpl.nasa.gov/api/horizons.api?"
    # define parameters
    start_time, stop_time = date, '-'.join(date.split("-")[:2]) + "-" + ("0" + str(int(date.split("-")[2]) + 1))[1:]
    # build url
    url += "format=json&EPHEM_TYPE=VECTORS&OBJ_DATA=YES&CENTER='500@0'"
    url += "&COMMAND='{}'&START_TIME='{}'&STOP_TIME='{}'".format(planetID, start_time, stop_time)

    ####################################################################

    session = requests.session()
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4
    session.mount('https://', CustomHttpAdapter(ctx))
    response = session.get(url).json()

    # This code is from: https://stackoverflow.com/questions/71603314/ssl-error-unsafe-legacy-renegotiation-disabled
    ####################################################################

    result = response['result']

    return result

def get_mass(data):
    data = data.splitlines()
    for line in data:
        if "Mass x" in line:
            mass_line = line

    if mass_line.index("Mass x") > 0.5 * len(mass_line):
        mass_line = mass_line[int(0.5*len(mass_line)):].strip()
    else:
        mass_line = mass_line[:int(0.5*len(mass_line))].strip()

    if "(kg)" in mass_line:
        power = int(mass_line.split("x")[1].strip().split("(kg)")[0].split("^")[1])
    elif "(g)" in mass_line:
        power = int(mass_line.split("x")[1].strip().split("(g)")[0].split("^")[1]) - 3

    base = float(mass_line.split("=")[1].strip("+-"))

    return base * 10**power



