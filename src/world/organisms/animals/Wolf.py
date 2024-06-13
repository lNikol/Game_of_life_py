from .Animal import Animal


class Wolf(Animal):
    def __init__(self, position, world, power=9, initiative=5, age=0):
        super().__init__("Wolf", position[0], position[1], power, initiative, world, age)
        self._world.add_message(f"Wolf ({self._y}, {self._x}) was created")

    def copy(self, position):
        return Wolf(position, self._world)

    def rebound_attack(self, org):
        return False
