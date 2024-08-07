from .Plant import Plant


class Dandelion(Plant):
    def __init__(self, position, world, power=0, initiative=0, age=0):
        super().__init__("Dandelion", position[0], position[1], power, initiative, world, age)
        self._world.add_message(f"Dandelion ({self._y}, {self._x}) was created")

    def copy(self, position):
        return Dandelion(position, self._world)

    def action(self):
        for _ in range(3):
            super().action()
