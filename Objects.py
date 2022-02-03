#Class for Objects in N-body Simulator

class body:
    def __init__(self,name,mass,iposition,ivelocity):
        self.name = name
        self.mass = mass
        self.position = iposition
        self.velocity = ivelocity
        self.position_history = [iposition]
        self.velocity_history = [ivelocity]
        self.kinetic_energy = []

    def get_position(self):
        return self.position

    def get_velocity(self):
        return self.velocity

    def get_mass(self):
        return self.mass

    def update_position(self,new_position):
        self.position = new_position
        self.position_history.append(new_position)

    def update_velocity(self,new_velocity):
        self.velocity = new_velocity
        self.velocity_history.append(new_velocity)
    