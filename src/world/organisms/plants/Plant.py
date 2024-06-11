import random
from abc import ABC

from src.world.organisms.Organism import Organism
from src.world.organisms.animals.Animal import Animal


class Plant(Organism, ABC):
    def __init__(self, name, y, x, power, initiative, world, age=0):
        super().__init__(name, y, x, power, initiative, world, age)

    def action(self):
        if self.__age > 2:
            if self.check_reproduction():
                rand = random.randint(0, 9) + 1
                if rand == 1:
                    new_position = self.__world.new_position(self, 1)
                    self.__world.set_organism(new_position, self)

    def collision(self, org):
        self.__world.delete_organism(self)
        self.__world.replace_organism(org.get_position(), org)
        if isinstance(org, Animal):
            self.__world.replace_organism(org.get_old_position(), None)
