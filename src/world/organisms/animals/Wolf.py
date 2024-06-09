from .Animal import Animal

class Wolf(Animal):
    def __init__(self, position, world, age=0):
        super().__init__("Wolf", position[0], position[1], 9, 5, world, age)
        print(f"Wolf ({self.__y}, {self.__x}) was created")

    def copy(self, position):
        return Wolf(position, self.__world)

    def rebound_attack(self, org):
        return False