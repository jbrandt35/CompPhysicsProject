from Equations import *
from time import time

import matplotlib.pyplot as plt

def RunSim(objects, settings):
    dt = settings["dt"]
    start_time = time()

    dist = []
    t = []
    n=0

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


def update_position_and_velocity(objects, dt):
    for object in objects:

        dv = object.acceleration * dt
        object.add_velocity(dv)

        dr = object.velocity * dt
        object.add_position(dr)



def update_forces(objects):
    for primary_object in objects:
        for secondary_object in objects[objects.index(primary_object) + 1:]:
            force = gravitational_force(primary_object, secondary_object)
            primary_object.add_force(force)
            secondary_object.add_force(-force)

def clear_forces(objects):
    for object in objects:
        object.clear_force()