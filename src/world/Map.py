from src.world.Cell import Cell
from src.world.organisms.animals.Animal import Animal
class Map:
    def __init__(self, width, height, world):
        self.__map = []
        self.__width = width
        self.__height = height
        self.__is_hex = world.get_is_hex()

        for i in range(height):
            row = []
            for j in range(width):
                row.append(Cell(i, j, self.__is_hex))
            self.__map.append(row)

    def set_organism(self, position, organism):
        self.__map[position[0]][position[1]].set_organism(organism, self.__is_hex)

    def replace_organism(self, position, new_org):
        self.__map[position[0]][position[1]].set_organism(new_org, self.__is_hex)

    def delete_organism(self, old_org):
        if old_org is None:
            return
        if isinstance(old_org, Animal):
            if old_org.get_is_alive():
                old_pos = old_org.get_position()
            else:
                old_pos = old_org.get_old_position()
        else:
            old_pos = old_org.get_position()

        self.replace_organism(old_pos, None)

    def get_cell(self, position):
        return self.__map[position[0]][position[1]]

    def get_cell(self, y, x):
        return self.__map[y][x]
