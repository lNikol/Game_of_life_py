from .Plant import Plant


class Wolfberries(Plant):
    def __init__(self, position, world, age=0):
        super().__init__("Wolfberries", position[0], position[1], 99, 0, world, age)
        print(f"Wolfberries ({self._x}, {self._y}) was created")

    def copy(self, position):
        return Wolfberries(position, self._world)

    def collision(self, org):
        print(f"{self._name}: Organism ({org.get_name()}) ate me, and I kill it")
        self._world.delete_organism(org)
        self._world.delete_organism(self)
