from .Animal import Animal


class Fox(Animal):
    def __init__(self, position, world, age=0):
        super().__init__("Fox", position[0], position[1], 9, 5, world, age)
        print(f"Fox ({self.__y}, {self.__x}) was created")

    def copy(self, position):
        return Fox(position, self.__world)

    def action(self):
        pos = self.__world.check_cells_around(self.get_position(), False)
        for cell in pos:
            if cell is not None and cell.get_position()[0] == -1:
                return
            if cell.get_org() is None or (cell.get_org() is not None and self.__power >= cell.org().get_power()):
                self.set_position(*(cell.get_pos()), False)
                super().collision(cell.get_org())
                return

    def rebound_attack(self, org):
        return False
