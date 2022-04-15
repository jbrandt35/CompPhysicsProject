from Equations import *
from time import time
import OrbitAnalyzer
import Output


def RunSim(objects, settings):
    dt = settings["dt"]
    start_time = time()

    barycenters = []

    #Note the call for the forces is neccasary to get the first half step velocities.
    update_forces(objects)
    for object in objects:
        object.hstep_velocity = object.velocity + 0.5 * dt * object.acceleration

    while time() - start_time < settings["Runtime"]:

        update_position(objects, dt, barycenters)
        update_forces(objects)
        update_velocity(objects, dt)

    print("Simulation ended.")

    OrbitAnalyzer.get_orbit_params(objects)
    #Plot the orbits
    Output.plot_orbits(objects)
    #create output files
    Output.create_files(objects)

    Output.plot_eccentricity(objects[0], settings)

    Output.plot_barycenter(barycenters)


def update_position(objects, dt, barycenters):
    barycenter = get_barycenter(objects)
    barycenters.append(magnitude(barycenter))
    for object in objects:
        #Calculate change in position using the time half-step velocity
        dr = dt * object.hstep_velocity
        object.add_position(dr, barycenter)


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

