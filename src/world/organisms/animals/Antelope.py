from .Animal import Animal
import random


class Antelope(Animal):
    def __init__(self, position, world, age=0):
        super().__init__("Antelope", position[0], position[1], 4, 4, world, age)
        print(f"Antelope ({self._y}, {self._x}) was created\n")

    def copy(self, position):
        return Antelope(position, self._world)

    def action(self):
        y, x = self._world.new_position(self, 2)
        self.set_position(y, x, False)
        super().collision(self._world.get_cell([y, x]).org)

    def rebound_attack(self, org):
        return False

    def collision(self, other):
        if other:
            if random.random() > 0.5:
                neighbors = self._world.check_cells_around(*self.get_position(), False)
                for neighbor in neighbors:
                    if not neighbor.org:
                        self.set_position(*neighbor.get_position(), False)
                        super().collision(neighbor.org)
                        return
                super().collision(other)
            else:
                super().collision(other)
        else:
            super().collision(other)
