from Equations import *
from time import time

import matplotlib.pyplot as plt

def RunSim(objects, settings):
    dt = settings["dt"]
    start_time = time()

    dist = []
    t = []
    n=0

    #Note the call for the forces is neccasary to get the first half step velocities. 
    clear_forces(objects)
    update_forces(objects)
    for object in objects:
        object.hstep_velocity = object.velocity + 0.5 * dt * object.acceleration

    while time() - start_time < settings["Runtime"]:
        clear_forces(objects)
        update_forces(objects)
        update_position_and_velocity(objects, dt)

        print(magnitude(objects[0].net_force))
        dist.append(magnitude(objects[0].position)/1000.0)
        t.append(n*dt)
        n += 1


    plt.plot(t, dist)
    plt.xlabel("Time (s)")
    plt.ylabel("Distance to Sun (km)")
    plt.title("dt = 100")
    plt.savefig("distance.png")


# def update_position_and_velocity(objects, dt):
#     for object in objects:

#         dv = object.acceleration * dt
#         object.add_velocity(dv)

#         dr = object.velocity * dt
#         object.add_position(dr)

def update_position_and_velocity(objects,dt):
    for object in objects:
        #Calculate change in position using the time half-step velocity
        dr = dt * object.hstep_velocity
        object.add_position(dr)

        #Calculate Veclocity for full dt incriment
        new_velocity = object.hstep_velocity + 0.5 * dt * object.acceleration
        object.add_velocity(new_velocity)

        #Calculate change in time half-step velocity for next generation
        dv = dt * object.acceleration
        object.hstep_velocity += dv

def update_forces(objects):
    for primary_object in objects:
        for secondary_object in objects[objects.index(primary_object) + 1:]:
            force = gravitational_force(primary_object, secondary_object)
            primary_object.add_force(force)
            secondary_object.add_force(-force)

def clear_forces(objects):
    for object in objects:
        object.clear_force()