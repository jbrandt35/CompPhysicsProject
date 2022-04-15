import os
import OrbitAnalyzer
from astropy import constants
import matplotlib.pyplot as plt
import numpy as np


def create_files(objects):
    for object in objects:
        #Position Array to write to output file
        pos_history = object.position_history
        vel_history = object.velocity_history

        #create text file name
        filename = object.name + "_output.txt"
        filePath = os.path.join("OutputFiles",filename)

        #Other parameters included in the output
        Name = object.name
        Name = Name[0].upper() + Name[1:]

        outFile = open(filePath,'w')
        outFile.write(f"------------------------------------------------\nObject: {Name}\nMass: {object.mass} kg\nSemi-Major Axis: {object.semi_major} AU\nSemi-Minor Axis: {object.semi_minor} AU\nEccentricity: {object.eccentricity} \nRotation: {object.rotation} degrees\nInclination: {object.inclination} degrees\n")
        outFile.write("------------------------------------------------\nPosition History (x,y,z) AU\n\n")
        for i in range(0,len(pos_history),10):
            x_pos = meters_to_au(pos_history[i][0])
            y_pos = meters_to_au(pos_history[i][1])
            z_pos = meters_to_au(pos_history[i][2])

            x_pos = "{:.3f}".format(x_pos)
            y_pos = "{:.3f}".format(y_pos)
            z_pos = "{:.3f}".format(z_pos)

            outFile.write(f"X = {x_pos}  Y = {y_pos}  Z = {z_pos}\n")

        outFile.write("\n\n\nOutput File Completed")
        outFile.close()


def meters_to_au(float_num):
    return round(float_num / 1.496e11, 3)


def plot_orbits(objects):
    for object in objects:
        x_coords = OrbitAnalyzer.get_x(object.position_history)/constants.au.value
        y_coords = OrbitAnalyzer.get_y(object.position_history)/constants.au.value

        plt.plot(x_coords, y_coords, label = object.name)

    plt.legend()
    axes = plt.gca()
    axes.set_aspect(1)
    plt.title("Simulated Orbital Trajectories (AU)")
    plt.savefig("Figures/trajectory.png")


def plot_eccentricity(object, settings):

    orbit = object.position_history
    dt = settings["dt"]
    indexes = range(0, len(orbit), round(365*24*60*60/dt))
    orbits = []

    for i in range(len(indexes) - 1):
        cycle = orbit[indexes[i]:indexes[i+1]]
        orbits.append(cycle)

    eccentricities = []

    for orb in orbits:
        eccentricities.append(OrbitAnalyzer.get_ellipse_params(OrbitAnalyzer.fit_ellipse(orb))[3])

    plt.close()
    plt.plot(np.array(range(len(eccentricities))) + 1, eccentricities)
    plt.xlabel("Years")
    plt.ylabel("Eccentricity")
    plt.title("Without Jupiter")
    plt.savefig("Figures/eccentricity.png")


