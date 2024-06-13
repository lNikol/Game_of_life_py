from .Animal import Animal
import random

class CyberSheep(Animal):
    def __init__(self, position, world, power=11, initiative=4, age=0):
        super().__init__("CyberSheep", position[0], position[1], power, initiative, world, age)
        self._world.add_message(f"CyberSheep ({self._y}, {self._x}) was created")

    def copy(self, position):
        return CyberSheep(position, self._world)

    def rebound_attack(self, org):
        return False

    def action(self):
        hogweed_position = self.find_nearest_hogweed()

        if hogweed_position:
            self.move_towards(hogweed_position)
        else:
            super().action()

    def find_nearest_hogweed(self):
        from ..plants.Hogweed import Hogweed

        current_position = self.get_position()
        cells_in_radius = self._world.check_cells_in_radius(current_position, 1 if self._world.get_is_hex() else 2)
        nearest_hogweed = None
        min_distance = float('inf')

        for cell in cells_in_radius:
            if isinstance(cell.get_org(), Hogweed):
                distance = self.calculate_distance(current_position, cell.get_position())
                if distance < min_distance:
                    min_distance = distance
                    nearest_hogweed = cell.get_position()

        return nearest_hogweed

    def calculate_distance(self, pos1, pos2):
        return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))

    def move_towards(self, target_position):
        current_position = self.get_position()
        dx = target_position[0] - current_position[0]
        dy = target_position[1] - current_position[1]

        if abs(dx) > 1 or abs(dy) > 1:
            dx = 1 if dx > 0 else (-1 if dx < 0 else 0)
            dy = 1 if dy > 0 else (-1 if dy < 0 else 0)

        new_position = (current_position[0] + dx, current_position[1] + dy)

        if self._world.is_position_valid(new_position):
            self.set_position(self._y, self._x, is_old=True)
            self.set_position(*new_position, is_old=False)
            self.collision(self._world.get_cell(new_position).get_org())
            return True
        else:
            valid_moves = self.get_possible_moves(current_position)
            if valid_moves:
                new_position = random.choice(valid_moves)
                self.set_position(self._y, self._x, is_old=True)
                self.set_position(*new_position, is_old=False)
                self.collision(self._world.get_cell(new_position).get_org())
                return True

    def get_possible_moves(self, position):
        x, y = position
        possible_moves = [
            (x + dx, y + dy)
            for dx in [-1, 0, 1]
            for dy in [-1, 0, 1]
            if not (dx == 0 and dy == 0)
        ]
        valid_moves = [pos for pos in possible_moves if self._world.is_position_valid(pos)]
        return valid_moves

