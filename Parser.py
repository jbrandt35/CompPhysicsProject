from Objects import Body
import json
from astropy import constants


#Takes in JSON File, returns "body" object
def parse_object(file):
    try:
        file_handler = open(file)
        data = json.load(file_handler)
        file_handler.close()
        print(f"Opening {file} to parse object")
    except:
        print(f"Can't load {file}.")

    if data["mass"] == "<Find>" and data["name"] == "Earth":
        print("Earth's mass not provided, pulling from Astropy")
        data["mass"] = constants.M_earth.value

    body = Body(data["name"], data["mass"], data["iposition"], data["ivelocity"])

    print(f"Successfully parsed {body.name}")

    return body

def parse_config(file):
    pass