from .Plant import Plant


class Grass(Plant):
    def __init__(self, position, world, age=0):
        super().__init__("Grass", position[0], position[1], 0, 0, world, age)
        print(f"Grass ({self._y}, {self._x}) was created\n")

    def copy(self, position):
        return Grass(position, self._world)
