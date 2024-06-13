from abc import ABC, abstractmethod


class Organism(ABC):
    def __init__(self, name="", y=-1, x=-1, power=-1, initiative=-1, world=None, age=0):
        self._name = name
        self._y = y
        self._x = x
        self._age = age
        self._power = power
        self._initiative = initiative
        self._world = world
        self._has_moved = True
        self._is_alive = True

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
        return self._name

    def get_power(self):
        return self._power

    def set_power(self, power):
        self._power = power
        return None

    def get_initiative(self):
        return self._initiative

    def get_position(self):
        return self._y, self._x

    def get_world(self):
        return self._world

    def get_has_moved(self):
        return self._has_moved

    def set_has_moved(self, has_moved):
        self._has_moved = has_moved
        return None

    def get_is_alive(self):
        return self._is_alive

    def set_is_alive(self, is_alive):
        self._is_alive = is_alive
        from .animals.Human import Human
        if isinstance(self, Human):
            self._world.add_message("\n\nYou have died\n\n")
        return None

    def set_position(self, y, x):
        self._y, self._x = y, x
        return None

    def get_age(self):
        return self._age

    def set_age(self, age):
        self._age = age
        return None

    def save_to_log(self):
        return (f"{self._name}(y,x): ({self._y}, {self._x}), "
                f"power: {self._power}, initiative: {self._initiative}, age: {self._age}\n")

    def check_reproduction(self):
        neighbors = self._world.check_cells_around(self.get_position(), False)
        empty_place = -1
        similar_neighbors = 0
        for index, neighbor in enumerate(neighbors):
            if neighbor.get_org() is not None and type(neighbor.get_org()) == type(self):
                    similar_neighbors += 1
            elif neighbor.get_org() is None:
                empty_place = index

        if similar_neighbors >= 2:
            self._world.delete_organism(self)
            return False
        elif empty_place != -1 and neighbors[empty_place].get_position()[0] != -1:
            self._world.set_organism([*neighbors[empty_place].get_position()], self)
            return True
        else:
            return False
