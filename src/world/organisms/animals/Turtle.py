import random

from .Animal import Animal

class Turtle(Animal):
    def __init__(self, position, world, age=0):
        super().__init__("Turtle", position[0], position[1], 2, 1, world, age)
        print(f"Turtle ({self.__y}, {self.__x}) was created\n")

    def copy(self, position):
        return Turtle(position, self.__world)

    def rebound_attack(self, org):
        return org.get_power() < 5

    def action(self):
        if random.random() < 0.25:
            super().action()