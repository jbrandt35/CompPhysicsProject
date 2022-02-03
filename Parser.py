from Objects import Body
import json
from astropy import constants
import os

#Takes in a list of JSON Files, returns a list of "body" objects
def parse_objects(files):
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

        if data["mass"] == "<Find>" and data["name"] == "Earth":
            print("Earth's mass not provided, pulling from Astropy")
            data["mass"] = constants.M_earth.value

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