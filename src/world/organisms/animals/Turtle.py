import random

from .Animal import Animal


class Turtle(Animal):
    def __init__(self, position, world, power=2, initiative=1, age=0):
        super().__init__("Turtle", position[0], position[1], power, initiative, world, age)
        print(f"Turtle ({self._y}, {self._x}) was created")

    def copy(self, position):
        return Turtle(position, self._world)

    def rebound_attack(self, org):
        return org.get_power() < 5

    def action(self):
        if random.random() < 0.25:
            super().action()
