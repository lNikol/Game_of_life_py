from .Plant import Plant


class Dandelion(Plant):
    def __init__(self, position, world, age=0):
        super().__init__("Dandelion", position[0], position[1], 0, 0, world, age)
        print(f"Dandelion ({self._y}, {self._x}) was created\n")

    def copy(self, position):
        return Dandelion(position, self._world)

    def action(self):
        for _ in range(3):
            super().action()
