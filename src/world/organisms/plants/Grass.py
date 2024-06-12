from .Plant import Plant


class Grass(Plant):
    def __init__(self, position, world, power=0, initiative=0, age=0):
        super().__init__("Grass", position[0], position[1], power, initiative, world, age)
        print(f"Grass ({self._y}, {self._x}) was created")

    def copy(self, position):
        return Grass(position, self._world)
