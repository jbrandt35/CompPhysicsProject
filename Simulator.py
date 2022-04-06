from Equations import *
from time import time
import OrbitAnalyzer
import matplotlib.pyplot as plt
import os


def RunSim(objects, settings):
    dt = settings["dt"]
    start_time = time()

    #Note the call for the forces is neccasary to get the first half step velocities.
    update_forces(objects)
    for object in objects:
        object.hstep_velocity = object.velocity + 0.5 * dt * object.acceleration

    while time() - start_time < settings["Runtime"]:

        update_position(objects, dt)
        update_forces(objects)
        update_velocity(objects, dt)

    print("Simulation ended. See Figures for trajectory plot and printing orbital data below.")
    OrbitAnalyzer.get_orbit_params(objects)
    #Plot the orbits
    plot_orbits(objects)
    #create output files
    create_files(objects)



def update_position(objects, dt):
    for object in objects:
        #Calculate change in position using the time half-step velocity
        dr = dt * object.hstep_velocity
        object.add_position(dr)

def update_velocity(objects, dt):
    for object in objects:
        dv = dt * object.acceleration

        # Calculate Veclocity for full dt incriment
        object.set_velocity(object.hstep_velocity + 0.5 * dv)

        # Calculate change in time half-step velocity for next generation
        object.hstep_velocity += dv


def update_forces(objects):
    clear_forces(objects)
    for primary_object in objects:
        for secondary_object in objects[objects.index(primary_object) + 1:]:
            force = gravitational_force(primary_object, secondary_object)
            primary_object.add_force(force)
            secondary_object.add_force(-force)


def clear_forces(objects):
    for object in objects:
        object.clear_force()

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
        outFile.write(f"------------------------------------------------\nObject: {Name}\nMass: {object.mass} kg\nSemi-Major Axis: {object.semi_major} AU\nSemi-Minor Axis: {object.semi_minor} AU\nEccentricity: {object.eccentricity} AU\nRotation: {object.rotation} degrees\n")
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
    return round(float_num / 1.496e11,3)