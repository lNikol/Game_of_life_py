from .Animal import Animal

class Antelope(Animal):
    def __init__(self, position, world, age=0):
        super().__init__("Antelope", position[0], position[1], 4, 4, world, age)
        print(f"Antelope ({self.__y}, {self.__x}) was created\n")

    def copy(self, position):
        return Antelope(position, self.__world)
    def action(self):
        y, x = self.__world.new_position(self, 2)
        self.set_position(y, x, False)
        super().collision(self.__world.get_cell(y, x).org)
    def rebound_attack(self, org):
        return False
