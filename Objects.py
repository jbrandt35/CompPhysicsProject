import numpy as np
from Equations import kinetic_energy

#Class for Objects in N-body Simulator
class Body:
    def __init__(self,name,mass,iposition,ivelocity):
        self.name = name
        self.mass = mass
        self.position = np.array(iposition)
        self.velocity = np.array(ivelocity)
        self.position_history = np.array([iposition])
        self.velocity_history = np.array([ivelocity])
        self.kinetic_energy = kinetic_energy(self)
        self.net_force = np.zeros(3)

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def add_force(self, force):
        self.net_force += force

    def get_acceleration(self):
        return self.net_force/self.mass

    def clear_force(self):
        self.net_force = np.zeros(3)

    def update_position(self,new_position):
        self.position = new_position
        np.append(self.position_history, new_position)

    def update_velocity(self,new_velocity):
        self.velocity = new_velocity
        np.append(self.velocity_history, new_velocity)
        self.kinetic_energy = kinetic_energy(self)
    