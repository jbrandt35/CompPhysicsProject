import numpy as np
from Equations import kinetic_energy

#Class for Objects in N-body Simulator
class Body:
    def __init__(self,name,mass,iposition,ivelocity):
        self.name = name
        self.mass = mass
        self.position = np.array(iposition, float)
        self.velocity = np.array(ivelocity, float)
        self.position_history = [iposition]
        self.velocity_history = [ivelocity]
        self.kinetic_energy = kinetic_energy(self)
        self.net_force = np.zeros(3, float)
        self.acceleration = np.zeros(3, float)
        self.hstep_velocity = 0.0
        self.semi_major = 0.0
        self.semi_minor = 0.0
        self.eccentricity = 0.0
        self.rotation = 0.0
        self.inclination = 0.0

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def add_force(self, force):
        self.net_force += force
        self.acceleration = self.net_force / self.mass

    def clear_force(self):
        self.net_force = np.zeros(3, float)

    def add_position(self,new_position):
        self.position += new_position
        self.position_history.append(np.copy(self.position))

    def add_velocity(self,new_velocity):
        self.velocity += new_velocity
        self.velocity_history.append(np.copy(self.velocity))
        self.kinetic_energy = kinetic_energy(self)

    def set_velocity(self,new_velocity):
        self.velocity = new_velocity
        self.velocity_history.append(np.copy(self.velocity))
        self.kinetic_energy = kinetic_energy(self)
    