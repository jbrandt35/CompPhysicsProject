from Equations import *
from time import time

def RunSim(objects, settings):
   start_time = time()
   dt = settings["dt"]
   while time() - start_time < settings["Runtime"]:
       clear_forces(objects)
       update_forces(objects)


def update_forces(objects):
    for primary_object in objects:
        for secondary_object in objects[objects.index(primary_object) + 1:]:
            force = gravitational_force(primary_object, secondary_object)
            primary_object.add_force(force)
            secondary_object.add_force(-force)

def clear_forces(objects):
    for object in objects:
        object.clear_force()