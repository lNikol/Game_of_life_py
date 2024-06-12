from .Plant import Plant
from ..animals.Animal import Animal


class Hogweed(Plant):
    def __init__(self, position, world, power=10, initiative=0, age=0):
        super().__init__("Hogweed", position[0], position[1], power, initiative, world, age)
        print(f"Hogweed ({self._y}, {self._x}) was created")

    def copy(self, position):
        return Hogweed(position, self._world)

    def action(self):
        neighbors = self._world.check_cells_around(self.get_position(), False)
        from ..animals.CyberSheep import CyberSheep
        for cell in neighbors:
            if isinstance(cell.get_org(), Animal) and not isinstance(cell.get_org(), CyberSheep):
                    print(f"{self._name}: I killed {cell.get_org().get_name()} at {cell.get_position()}")
                    self._world.delete_organism(cell.get_org())

    def collision(self, org):
        from ..animals.CyberSheep import CyberSheep
        self._world.delete_organism(self)
        if not isinstance(org, CyberSheep): # not isinstance(cell.get_org(), CyberSheep
            print("To nie cyberowca")
            print(f"{self._name}: Organism ({org.get_name()}) ate me, and I killed it")
            self._world.delete_organism(org)
        else:
            print(f"{self._name}: Organism ({org.get_name()}) ate me, and I didn't kill it")