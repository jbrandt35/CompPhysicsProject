from Equations import *
from time import time

def RunSim(objects, settings):
   dt = settings["dt"]
   start_time = time()
   while time() - start_time < settings["Runtime"]:
       clear_forces(objects)
       update_forces(objects)
       update_position_and_velocity(objects, dt)

       print(objects[0].position)


def update_position_and_velocity(objects, dt):
    for object in objects:
        dr = object.velocity * dt + (1/2) * object.acceleration * dt**2
        object.add_position(dr)

        dv = object.acceleration * dt
        object.add_velocity(dv)


def update_forces(objects):
    for primary_object in objects:
        for secondary_object in objects[objects.index(primary_object) + 1:]:
            force = gravitational_force(primary_object, secondary_object)
            primary_object.add_force(force)
            secondary_object.add_force(-force)

def clear_forces(objects):
    for object in objects:
        object.clear_force()