import random
from abc import ABC

from ..Organism import Organism


class Plant(Organism, ABC):
    def __init__(self, name, y, x, power, initiative, world, age=0):
        super().__init__(name, y, x, power, initiative, world, age)

    def action(self):
        #self._world.add_message(f"Action in {self._name}:")
        if self._age > 2:
            if self.check_reproduction():
                rand = random.randint(0, 9) + 1
                if rand == 1:
                    new_position = self._world.new_position(self, 1)
                    self._world.set_organism([*new_position], self)

    def collision(self, org):
        #self._world.add_message(f"Collision in {self._name}:")
        self._world.delete_organism(self)
        self._world.replace_organism([*org.get_position()], org)
        from ..animals.Animal import Animal
        if isinstance(org, Animal):
            self._world.replace_organism([*org.get_old_position()], None)
