from .Plant import Plant


class Guarana(Plant):
    def __init__(self, position, world, age=0, power=0, initiative=0):
        super().__init__("Guarana", position[0], position[1], power, initiative, world, age)
        print(f"Guarana ({self.__y}, {self.__x}) was created\n")

    def copy(self, position):
        return Guarana(position, self.__world)

    def collision(self, org):
        print(f"{self.__name}: Organism ({org.get_name()}) ate me, and I boost its power")
        org.set_power(org.get_power() + 3)
        self.__world.delete_organism(self)
        self.__world.replace_organism(org.get_old_position(), None)
        self.__world.replace_organism(org.get_position(), org)
