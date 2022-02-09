from Equations import *
from time import time

def RunSim(objects, settings):
   dt = settings["dt"]
   start_time = time()
   while time() - start_time < settings["Runtime"]:
       clear_forces(objects)
       update_forces(objects)
       update_position_and_velocity(objects, dt)


def update_position_and_velocity(objects, dt):
    for object in objects:
        dr = object.velocity * dt + (1/2)*object.get_acceleration() * dt**2
        object.update_position(object.position + dr)

        dv = object.get_acceleration() * dt
        object.update_velocity(object.velocity + dv)


def update_forces(objects):
    for primary_object in objects:
        for secondary_object in objects[objects.index(primary_object) + 1:]:
            force = gravitational_force(primary_object, secondary_object)
            primary_object.add_force(force)
            secondary_object.add_force(-force)

def clear_forces(objects):
    for object in objects:
        object.clear_force()