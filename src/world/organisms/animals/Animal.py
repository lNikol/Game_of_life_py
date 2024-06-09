from . import Antelope
from ..Organism import Organism

class Animal(Organism):
    def __init__(self, name, y, x, power, initiative, world, age=0):
        super().__init__(name, y, x, age, power, initiative, world)
        self.__old_y = y
        self.__old_x = x
    def get_old_position(self):
        return self.__old_y, self.__old_x
    def set_position(self, y, x, is_old):
        if(is_old):
            self.__old_y, self.__old_x = y, x
        else:
            self.__y, self.__x = y, x
    def move(self):
        self.__y, self.__x = self.__world.new_position(self, 1)
        self.set_position(self.__y, self.__x, False)

    def action(self):
        self.collision(self.__world.get_cell(*(super().get_position())).get_org)
        return None
    def collision(self, org):
        if(isinstance(org, Animal)):
            if type(self) == type(org):
                if not self.reproduction(org):
                    org.reproduction(self)
                self.set_position(*(super().get_position()), True)
            else:
                if(isinstance(org, Antelope)):
                    org.collision(self)
                    if(super().__is_alive):
                        super().__world.replace_organism(*(super().get_position()), self)
                        super().__world.replace_organism(*(super().get_old_position()), None)
                        self.set_position(*super().get_position(), True)
                    else:
                        super().__world.delete_organism(self)
                else:

