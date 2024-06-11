from .Plant import Plant


class Dandelion(Plant):
    def __init__(self, position, world, age=0, power=0, initiative=0):
        super().__init__("Dandelion", position[0], position[1], power, initiative, world, age)
        print(f"Dandelion ({self.__y}, {self.__x}) was created\n")

    def copy(self, position):
        return Dandelion(position, self.__world)

    def action(self):
        for _ in range(3):
            super().action()
