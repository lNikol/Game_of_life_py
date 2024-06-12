from .Animal import Animal
from src.world.organisms.plants.Hogweed import Hogweed
#from Sheep import Sheep

class CyberSheep(Animal):
    def __init__(self, position, world, age=0):
        super().__init__("CyberSheep", position[0], position[1], 11, 4, world, age)
        print(f"CyberSheep ({self.__y}, {self.__x}) was created\n")

    def copy(self, position):
        return CyberSheep(position, self.__world)

    def find_hogweed(self):
        return None

    def move_to_hogweed(self):
        return None

    def action(self):
        y, x = self.find_hogweed()
        if y != -1:
            self.move_to_hogweed()
        else:
            super().action()

        return None

    def rebound_attack(self, org):
        return False
