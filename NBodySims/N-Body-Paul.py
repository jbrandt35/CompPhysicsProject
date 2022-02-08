#Import 
import Equations.py as eq


#Get Acceleration Value - use as callable function that takes a planets name, and returns the net acceleration due to all other
#bodies in the system

def get_acc(planet):
    planet_pos = planet.position

    #Generate array of position vectors, indexed parrallel to a list/array of their names
    planet_names = []
    planet_positions = []

    net_force = [0,0,0]
    for body in body_positions:
        force = gravitational_force(planet,body)
        net_force = net_force + force  #Array arithmetic to find net force due to all bodies in the system

    net_acceleration = net_force / planet.mass

    return net_acceleration

#Not sure if we want to make a callable kinematics function, or call get_acc() in main and input there
#Also update functionality probobly want to build into the main function

def next_velocity(body):
    current_velocity = body.velocity
    acceleration = get_acc(body)
    new_velocity = current_velocity + (acceleration * time_step) #time step can be something we define in the config file, as one of the run parameters

    return new_velocity
