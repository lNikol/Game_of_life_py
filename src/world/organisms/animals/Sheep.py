from .Animal import Animal


class Sheep(Animal):
    def __init__(self, position, world, power=4, initiative=4, age=0):
        super().__init__("Sheep", position[0], position[1], power, initiative, world, age)
        self._world.add_message(f"Sheep ({self._y}, {self._x}) was created\n")

    def copy(self, position):
        return Sheep(position, self._world)

    def rebound_attack(self, org):
        return False
