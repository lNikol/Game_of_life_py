from .Plant import Plant
from src.world.organisms.animals.Animal import Animal


class Hogweed(Plant):
    def __init__(self, position, world, age=0):
        super().__init__("Hogweed", position[0], position[1], 10, 0, world, age)
        print(f"Hogweed ({self._y}, {self._x}) was created")

    def copy(self, position):
        return Hogweed(position, self._world)

    def action(self):
        neighbors = self._world.check_cells_around(self.get_position(), False)
        for cell in neighbors:
            from ..animals.CyberSheep import CyberSheep
            if isinstance(cell.get_org(), Animal) and not isinstance(cell.get_org(), CyberSheep):
                self._world.delete_organism(cell.get_org())

    def collision(self, org):
        print(f"{self._name}: Organism ({org.get_name()}) ate me, and I kill it")
        from src.world.organisms.animals.CyberSheep import CyberSheep
        if not isinstance(org, CyberSheep):
            self._world.delete_organism(org)
            self._world.delete_organism(self)
