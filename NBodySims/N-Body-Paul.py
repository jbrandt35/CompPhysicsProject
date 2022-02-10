#Import 
import Equations.py as eq


#Get Acceleration Value - use as callable function that takes a planets name, and returns the net acceleration due to all other
#bodies in the system

def get_acc(planet):
    planet_position = planet.position
    planet_name = planet.name

    net_force = [0,0,0]
    for body in bodies:
        if body.name != planet_name:
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

def next_position(body):
    current_position = body.position
    new_position = body.velocity * dt + 0.5 * get_acc(body) * dt ** 2
    return new_position

def generation_update():
    for body in bodies:
        body.position = next_position(body)
        body.velocity = next_velocity(body)
        body.position_history.append(body.position)
        body.velocity_history.append(body.velocity)
        body.time_history += dt