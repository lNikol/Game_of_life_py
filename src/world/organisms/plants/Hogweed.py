from .Plant import Plant
from src.world.organisms.animals.Animal import Animal
from src.world.organisms.animals.CyberSheep import CyberSheep


class Hogweed(Plant):
    def __init__(self, position, world, age=0, power=10, initiative=0):
        super().__init__("Hogweed", position[0], position[1], power, initiative, world, age)
        print(f"Hogweed ({self.__y}, {self.__x}) was created")

    def copy(self, position):
        return Hogweed(position, self.__world)

    def action(self):
        neighbors = self.__world.check_cells_around(self.get_position(), False)
        for cell in neighbors:
            if isinstance(cell.org, Animal) and not isinstance(cell.org, CyberSheep):
                self.__world.delete_organism(cell.org)

    def collision(self, org):
        print(f"{self.__name}: Organism ({org.get_name()}) ate me, and I kill it")
        if not isinstance(org, CyberSheep):
            self.__world.delete_organism(org)
            self.__world.delete_organism(self)
