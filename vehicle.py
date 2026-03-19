import random


class VehicleSimulator:
    def __init__(self, initial_speed=0.0, max_speed=120.0):
        self.speed = initial_speed
        self.max_speed = max_speed

    def update_speed(self, increment=0.0):
        self.speed += increment
        self.speed = max(0.0, min(self.speed, self.max_speed))
        return self.speed

    def random_fluctuation(self):
        change = random.choice([-5, 0, 5])
        return self.update_speed(change)

    def is_moving(self, threshold=5.0):
        return self.speed >= threshold