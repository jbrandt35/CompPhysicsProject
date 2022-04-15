from astropy import constants
import numpy as np


def gravitational_force(body1, body2):

    r = body2.position - body1.position

    r_hat = r/magnitude(r)

    return r_hat * constants.G.value * body1.mass * body2.mass / magnitude(r)**2


def kinetic_energy(body):
    return (1/2) * body.mass * magnitude(body.velocity)**2


#Rapper for norm() from numpy
def magnitude(vector):
    return np.linalg.norm(vector)


def distance(p1, p2):
    return magnitude(p1 - p2)


def get_barycenter(bodies):

    weighted_position = np.zeros(3, float)
    total_mass = 0.0

    for body in bodies:
        weighted_position += body.mass * body.position
        total_mass += body.mass

    return weighted_position / total_mass

