from abc import ABC, abstractmethod
from src.world.organisms.plants import *
from src.world.organisms.animals import *


class Organism(ABC):
    organisms = [
        Guarana,
        Hogweed,
        Grass,
        Dandelion,
        Wolf,
        Fox,
        CyberSheep,
        Sheep,
        Turtle,
        Antelope,
        Human
    ]

    def __init__(self, name="", y=-1, x=-1, power=-1, initiative=-1, world=None, age=0):
        self.__name = name
        self.__y = y
        self.__x = x
        self.__age = age
        self.__power = power
        self.__initiative = initiative
        self.__world = world
        self.__has_moved = False
        self.__is_alive = True

    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def collision(self):
        pass

    @abstractmethod
    def copy(self, position):
        pass

    def get_name(self):
        return self.__name

    def get_power(self):
        return self.__power

    def set_power(self, power):
        self.__power = power
        return None

    def get_initiative(self):
        return self.__initiative

    def get_position(self):
        return self.__y, self.__x

    def get_world(self):
        return self.__world

    def get_has_moved(self):
        return self.__has_moved

    def set_has_moved(self, hasMoved):
        self.__has_moved = hasMoved
        return None

    def get_is_alive(self):
        return self.__has_moved

    def set_is_alive(self, is_alive):
        self.__is_alive = is_alive
        return None

    def set_position(self, y, x):
        self.__y, self.__x = y, x
        return None

    def get_age(self):
        return self.__age

    def set_age(self, age):
        self.__age = age
        return None

    def write_to_log(self):
        return (f"{self.__name}(y,x): ({self.__y}, {self.__x}), "
                f"power: {self.__power}, initiative: {self.__initiative}, age: {self.__age}\n")

    def check_reproduction(self):
        neighbors = self.__world.check_cells_around(self.get_position(), False)
        empty_place = -1
        similar_neighbors = 0
        for index, neighbor in enumerate(neighbors):
            if neighbor.get_org() is not None and isinstance(neighbor.get_org(), self):
                similar_neighbors += 1
            elif neighbor.get_org() is None:
                empty_place = index

        if similar_neighbors >= 2:
            self.__world.delete_organism(self)
            return False
        elif empty_place != -1 and neighbors[empty_place].get_pos()[0] != -1:
            self.__world.set_organism(self, neighbors[empty_place].get_pos())
            return True
        else:
            return False
