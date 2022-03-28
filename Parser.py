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

        if data["mass"] == "<Find>":
            if data["name"] == "earth":
                print("Earth's mass not provided, pulling from Astropy")
                data["mass"] = constants.M_earth.value
            elif data["name"] == "sun":
                print("Sun's mass not provided, pulling from Astropy")
                data["mass"] = constants.M_sun.value

        if data["iposition"] == "<Find>":
            #Find the bodies name
            BodyName = data["name"]
            #get tupe of position and velocity for the body
            BodyInstance = get_body_barycentric_posvel(BodyName,t)
            #get position array
            BodyCoords = np.array(BodyInstance[0].get_xyz(),float)
            data["iposition"] = BodyCoords * 10e3 #10e3 is added because ephemeris gives value in km

        if data["ivelocity"] == "<Find>":
            BodyName = data["name"]
            BodyInstance = get_body_barycentric_posvel(BodyName,t)
            #get velocity array
            BodyVel = np.array(BodyInstance[1].get_xyz(),float)
            data["ivelocity"] = BodyVel * 0.011574074 #float value is conversion factor from km/day to m/s

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