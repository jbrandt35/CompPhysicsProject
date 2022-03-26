from Equations import *
from time import time
import OrbitAnalyzer


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

    OrbitAnalyzer.get_orbit_params(objects[0].position_history)


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