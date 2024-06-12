from .Plant import Plant


class Guarana(Plant):
    def __init__(self, position, world, age=0):
        super().__init__("Guarana", position[0], position[1], 0, 0, world, age)
        print(f"Guarana ({self._y}, {self._x}) was created\n")

    def copy(self, position):
        return Guarana(position, self._world)

    def collision(self, org):
        print(f"{self._name}: Organism ({org.get_name()}) ate me, and I boost its power")
        org.set_power(org.get_power() + 3)
        self._world.delete_organism(self)
        self._world.replace_organism([*org.get_old_position()], None)
        self._world.replace_organism([*org.get_position()], org)
