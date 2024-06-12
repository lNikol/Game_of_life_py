from abc import abstractmethod
from src.world.organisms.Organism import Organism
from src.world.organisms.plants.Plant import Plant


class Animal(Organism):
    def __init__(self, name, y, x, power, initiative, world, age=0):
        super().__init__(name, y, x, power, initiative, world, age)
        self._old_y = y
        self._old_x = x

    def get_old_position(self):
        return self._old_y, self._old_x

    def set_position(self, y, x, is_old=False):
        if is_old:
            self._old_y, self._old_x = y, x
        else:
            super().set_position(y, x)

    @abstractmethod
    def rebound_attack(self, attacker):
        pass

    def reproduction(self):
        if self.__age <= 2:
            return False
        else:
            return self.check_reproduction()

    def move(self):
        new_y, new_x = self.__world.new_position(self, 1)
        self.set_position(self.__y, self.__x, is_old=True)
        self.set_position(new_y, new_x, is_old=False)

    def action(self):
        self.move()
        cell = self.__world.get_cell(*self.get_position())
        if cell:
            self.collision(cell.get_org())

    def collision(self, org):
        if isinstance(org, Animal):
            if type(self) == type(org):
                if not self.reproduction():
                    org.reproduction()
                self.set_position(self._old_y, self._old_x, is_old=False)
            else:
                from Antelope import Antelope
                if isinstance(org, Antelope):
                    org.collision(self)
                    if self.__is_alive:
                        self.__world.replace_organism(self.get_position(), self)
                        self.__world.replace_organism(self._old_y, self._old_x, None)
                        self.set_position(self._old_y, self._old_x, is_old=True)
                    else:
                        self.__world.delete_organism(self)
                else:
                    if org.rebound_attack(self):
                        self.set_position(self._old_y, self._old_x)
                        self.__world.delete_organism(org)
                    else:
                        if self.__power >= org.get_power():
                            new_y, new_x = org.get_position()
                            self.__world.delete_organism(org)
                            self.__world.replace_organism(self.get_old_position(), None)
                            self.__world.replace_organism((new_y, new_x), self)
                            self.set_position(self._old_y, self._old_x, is_old=True)
                        else:
                            self.__world.delete_organism(self)
        elif isinstance(org, Plant):
            org.collision(self)
            self.set_position(self._old_y, self._old_x, is_old=True)
        else:
            self.__world.replace_organism(self.get_position(), self)
            self.__world.replace_organism(self.get_old_position(), None)
            self.set_position(self._old_y, self._old_x, is_old=True)
