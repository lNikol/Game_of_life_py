from .Animal import Animal


class Fox(Animal):
    def __init__(self, position, world, power=3, initiative=7, age=0):
        super().__init__("Fox", position[0], position[1], power, initiative, world, age)
        print(f"Fox ({self._y}, {self._x}) was created")

    def copy(self, position):
        return Fox(position, self._world)

    def action(self):
        pos = self._world.check_cells_around([*self.get_position()], False)
        s = f"{self._name} ({self._old_y}, {self._old_x} -> "
        for cell in pos:
            if cell is not None and cell.get_position()[0] == -1:
                return
            if cell.get_org() is None or (cell.get_org() is not None and self._power >= cell.get_org().get_power()):
                self.set_position(*(cell.get_position()), False)
                super().collision(cell.get_org())
                s += f"{self._y}, {self._x})"
                print(s)
                return

    def rebound_attack(self, org):
        return False
