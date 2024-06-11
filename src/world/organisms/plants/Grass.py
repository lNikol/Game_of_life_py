from .Plant import Plant


class Grass(Plant):
    def __init__(self, position, world, age=0, power=0, initiative=0):
        super().__init__("Grass", position[0], position[1], power, initiative, world, age)
        print(f"Grass ({self.__y}, {self.__x}) was created\n")

    def copy(self, position):
        return Grass(position, self.__world)
