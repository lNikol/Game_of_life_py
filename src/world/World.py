import random
import re

from .Cell import Cell


class World:
    def __init__(self, width, height, read_file=False, is_hex=False, file_name="log.log"):
        self.__width = width
        self.__height = height
        self.__read_file = read_file
        self.__file_name = file_name
        self.__is_hex = is_hex
        from .Map import Map
        self.__map = Map(width, height, self)
        self.__organisms = []
        self.__organisms_in_game = []
        self.__human = None
        self.__human_is_alive = True
        self.__is_player_turn = False
        self.__key_pressed = False
        self.__turn_count = 0
        self.generate_world()

    def generate_world(self):
        if not self.__read_file:
            if self.__is_hex:
                self.__width = self.__height
            from .organisms.animals.Human import Human
            self.__human = Human([0, 0], self)
            self.__organisms.append(self.__human)
            self.__map.set_organism([0, 0], self.__human)

            for i in range(self.__height):
                for j in range(self.__width):
                    if j % 4 == 1:
                        #plant generate
                        rand_pos = self.random_position()
                        if rand_pos == [-1, -1]:
                            continue
                        from .organisms.Organisms import all_organisms
                        org = all_organisms[(i + j) % 5]

                        if org not in self.__organisms_in_game:
                            self.__organisms_in_game.append(org)
                        new_org = org(rand_pos, self)
                        self.__map.set_organism(rand_pos, new_org)
                        self.__organisms.append(new_org)
                    elif j % 4 == 0:
                        # animal generate
                        rand_pos = self.random_position()
                        if rand_pos == [-1, -1]:
                            continue
                        from .organisms.Organisms import all_organisms
                        org = all_organisms[(i + j) % 6 + 5]
                        if org not in self.__organisms_in_game:
                            self.__organisms_in_game.append(org)
                        new_org = org(rand_pos, self)
                        self.__map.set_organism(rand_pos, new_org)
                        self.__organisms.append(new_org)
        else:
            self.read_from_file()

    def random_position(self):
        counter = 0
        while counter < 300:
            x = random.randint(0, self.__width - 1)
            y = random.randint(0, self.__height - 1)
            if self.__map.get_cell([y, x]).get_org() is None:
                return [y, x]
            counter += 1
        return [-1, -1]

    def read_from_file(self):
        from .organisms.Organisms import all_organisms
        try:
            with open(self.__file_name, "r") as file:
                for line in file:
                    if not line.startswith("World:"):
                        data = re.findall(r'\d+', line)
                        if data:
                            numbers = list(map(int, data))
                            first_word = line.split("(y,x):")[0].strip()
                            for organism in all_organisms:
                                if first_word == organism.__name__:
                                    pos = [numbers[0], numbers[1]]
                                    if first_word == "Human":
                                        self.__human = all_organisms[len(all_organisms) - 1](pos, self, numbers[2], numbers[3], numbers[4])
                                        self.__map.set_organism(pos, self.__human)
                                        self.__organisms.append(self.__human)
                                    else:
                                        org = organism(pos, self, numbers[2], numbers[3], numbers[4])
                                        self.__organisms.append(org)
                                        self.__map.set_organism(pos, org)
                                        if organism not in self.__organisms_in_game:
                                            self.__organisms_in_game.append(organism)
        except FileNotFoundError:
            print("File not found:", self.__file_name)

    def check_cells_around(self, position, only_one):
        neighbors = []
        y, x = position

        if not self.__is_hex:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    new_y = y + i
                    new_x = x + j
                    if 0 <= new_x < self.__width and 0 <= new_y < self.__height:
                        cell = self.__map.get_cell([new_y, new_x])
                        if only_one and cell.get_org() is None:
                            return [cell]
                        neighbors.append(cell)

            if only_one:
                if neighbors:
                    return [neighbors[0]]
                else:
                    neighbors.append(Cell(-1, -1, None))
                    return neighbors
            return neighbors
        else:
            # For hexagonal grid
            d_lines = [0, 0, -1, 1, 1, -1]
            d_poses = [-1, 1, 1, -1, 0, 0]

            for i in range(6):
                new_y = y + d_lines[i]
                new_x = x + d_poses[i]
                if 0 <= new_y < self.__height and 0 <= new_x < self.__width:
                    cell = self.__map.get_cell([new_y, new_x])
                    if only_one and cell.get_org() is None:
                        return [cell]
                    neighbors.append(cell)

            if only_one:
                if neighbors:
                    return [neighbors[0]]
                else:
                    neighbors.append(Cell(-1, -1, None))
                    return neighbors
            return neighbors

    def save_to_log(self):
        self.update_organisms()
        to_save = f"World: height: {self.__height}, width: {self.__width}\n"
        for org in self.__organisms:
            to_save += org.save_to_log()
        return to_save

    def update_organisms(self):

        i = len(self.__organisms) - 1
        while i >= 0:
            # czy wszystkich usunie?
            if not self.__organisms[i].get_is_alive():
                self.__organisms.pop(i)
            i -= 1

        self.__organisms.sort(key=lambda x: (-x.get_initiative(), -x.get_age()))

    def take_a_turn(self):
        self.__human_is_alive = self.__human is not None and self.__human.get_is_alive()
        if self.__human_is_alive:
            for org in self.__organisms:
                org.set_age(org.get_age() + 1)
                org.set_has_moved(False)
            self.update_organisms()
            self.draw_world()
            for org in self.__organisms:
                if not org.get_has_moved() and org.get_is_alive():
                    org.set_has_moved(True)
                    org.action()
                    self.draw_world()
            self.__turn_count += 1

        else:
            print("\n\nYou have died\n\n")
            return False

    def draw_world(self):
        s = ""
        for i in range(self.__height):
            for j in range(self.__width):
                org = self.__map.get_cell([i, j]).get_org()
                if org is None:
                    s += " . "
                else:
                    sym = ""
                    if org.get_name() == "Grass":
                        sym = "g"
                    elif org.get_name() == "Hogweed":
                        sym = "h"
                    elif org.get_name() == "Wolfberries":
                        sym = "w"
                    elif org.get_name() == "CyberSheep":
                        sym = "C"
                    else:
                        sym = org.get_name()[0]
                    s += " " + sym + " "
            s += "\n"
        print(s)

    # def update_world(self):
    #     for i in range(self.__height):
    #         for j in range(self.__width):
    #             c = self.get_cell([i, j])
    #             if c.is_hex:
    #                 c.set_new_color(Color.white)
    #             else:
    #                 c.set_background(Color.white)
    #             c.remove_all()
    #             if c.org is not None:
    #                 label = JLabel(c.org.get_name())
    #                 if isinstance(c.org, Animal):
    #                     if c.is_hex:
    #                         c.set_new_color(Color.red)
    #                     else:
    #                         c.set_background(Color.red)
    #                 elif isinstance(c.org, Plant):
    #                     if c.is_hex:
    #                         c.set_new_color(Color.green)
    #                     else:
    #                         c.set_background(Color.green)
    #                 c.add(label)
    #                 c.revalidate()
    #             c.repaint()

    def replace_organism(self, position, new_org):
        self.__map.replace_organism(position, new_org)

    def delete_organism(self, old_org):
        if old_org is None:
            return
        old_org.set_is_alive(False)
        self.__map.delete_organism(old_org)
        if old_org in self.__organisms:
            self.__organisms.remove(old_org)

    def set_is_player_turn(self, is_player_turn):
        self.__is_player_turn = is_player_turn

    def get_is_player_turn(self):
        return self.__is_player_turn

    def set_key_pressed(self, pressed):
        self.__key_pressed = pressed

    def get_key_pressed(self):
        return self.__key_pressed

    def set_key(self, s):
        self.__human.set_key(s)

    def get_key(self):
        return self.__human.get_key()

    def set_organism(self, position, org):
        if self.__map.get_cell(position).get_org() is None:
            child = org.copy(position)
            self.__organisms.append(child)
            self.__map.set_organism([*position], child)
            return True
        else:
            print("setOrganism in World: Cannot set organism, the place by (y,x)", position[0], ",", position[1],
                  "isn't null")
            return False

    def set_is_hex(self, is_hex):
        self.__is_hex = is_hex

    def get_is_hex(self):
        return self.__is_hex

    def get_cell(self, position):
        return self.__map.get_cell(position)
    def get_human_is_alive(self):
        return self.__human_is_alive
    def get_human(self):
        return self.__human
    def get_is_player_turn(self):
        return self.__is_player_turn
    def get_map(self):
        return self.__map

    def get_organisms_in_game(self):
        return self.__organisms_in_game

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_turn_count(self):
        return self.__turn_count

    def new_position(self, org, dist):
            w = self.__width - 1
            h = self.__height - 1
            pos = org.get_position()
            y, x = pos

            if not self.__is_hex:
                if y == 0:
                    if x == 0:
                        direction = random.randint(1, 2)
                        if direction == 1:
                            x += dist  # right
                        elif direction == 2:
                            x += dist  # right-down
                            y += dist
                    elif x == w:
                        direction = random.randint(1, 4)
                        if direction == 1:
                            y += dist  # down
                        elif direction == 2:
                            x -= dist  # left
                        elif direction == 3:
                            x -= dist  # left-down
                            y += dist
                    else:
                        direction = random.randint(1, 5)
                        if direction == 1:
                            y += dist  # down
                        elif direction == 2:
                            x = x + dist if x + dist <= w else x + 1  # right
                        elif direction == 3:
                            x = x - dist if x - dist >= 0 else x - 1  # left
                        elif direction == 4:
                            if x - dist >= 0:
                                x -= dist
                                y += dist  # left-down
                            else:
                                x -= 1
                                y += 1
                        elif direction == 5:
                            if x + dist <= w:
                                x += dist
                                y += dist  # right-down
                            else:
                                x += 1
                                y += 1
                elif y == h:
                    if x == 0:
                        direction = random.randint(1, 3)
                        if direction == 1:
                            y -= dist  # top
                        elif direction == 2:
                            x += dist  # right
                        elif direction == 3:
                            x += dist  # right-top
                            y -= dist
                    elif x == w:
                        direction = random.randint(1, 3)
                        if direction == 1:
                            y -= dist  # top
                        elif direction == 2:
                            x -= dist  # left
                        elif direction == 3:
                            x -= dist  # left-top
                            y -= dist
                    else:
                        direction = random.randint(1, 5)
                        if direction == 1:
                            y -= dist  # top
                        elif direction == 2:
                            x = x - dist if x - dist >= 0 else x - 1  # left
                        elif direction == 3:
                            x = x + dist if x + dist <= w else x + 1  # right
                        elif direction == 4:
                            if x + dist <= w:
                                x += dist
                                y -= dist  # right-top
                            else:
                                x += 1
                                y -= 1
                        elif direction == 5:
                            if x - dist >= 0:
                                x -= dist
                                y -= dist  # left-top
                            else:
                                x -= 1
                                y -= 1
                elif x == w and 1 <= y < h:
                    direction = random.randint(1, 5)
                    if direction == 1:
                        y = y + dist if y + dist <= h else y + 1  # down
                    elif direction == 2:
                        y = y - dist if y - dist >= 0 else y - 1  # top
                    elif direction == 3:
                        x -= dist  # left
                    elif direction == 4:
                        if y - dist >= 0:
                            x -= dist
                            y -= dist  # left-top
                        else:
                            x -= 1
                            y -= 1
                    elif direction == 5:
                        if y + dist <= h:
                            x -= dist
                            y += dist  # left-down
                        else:
                            x -= 1
                            y += 1
                elif x == 0 and 1 <= y < h:
                    direction = random.randint(1, 5)
                    if direction == 1:
                        y = y + dist if y + dist <= h else y + 1  # down
                    elif direction == 2:
                        y = y - dist if y - dist >= 0 else y - 1  # top
                    elif direction == 3:
                        x += dist  # right
                    elif direction == 4:
                        if y - dist >= 0:
                            x += dist
                            y -= dist  # right-top
                        else:
                            x += 1
                            y -= 1
                    elif direction == 5:
                        if y + dist <= h:
                            x += dist
                            y += dist  # right-down
                        else:
                            x += 1
                            y += 1
                else:
                    direction = random.randint(1, 8)
                    if direction == 1:
                        y = y + dist if y + dist <= h else y + 1  # down
                    elif direction == 2:
                        y = y - dist if y - dist >= 0 else y - 1  # top
                    elif direction == 3:
                        x = x + dist if x + dist <= w else x + 1  # right
                    elif direction == 4:
                        x = x - dist if x - dist >= 0 else x - 1  # left
                    elif direction == 5:
                        if y - dist >= 0 and x - dist >= 0:
                            x -= dist
                            y -= dist  # left-top
                        else:
                            x -= 1
                            y -= 1
                    elif direction == 6:
                        if y + dist <= h and x - dist >= 0:
                            x -= dist
                            y += dist  # left-down
                        else:
                            x -= 1
                            y += 1
                    elif direction == 7:
                        if y - dist >= 0 and x + dist <= w:
                            x += dist
                            y -= dist  # right-top
                        else:
                            x += 1
                            y -= 1
                    elif direction == 8:
                        if y + dist <= h and x + dist <= w:
                            x += dist
                            y += dist  # right-down
                        else:
                            x += 1
                            y += 1

            return [y, x]

    def check_cells_in_radius(self, position, radius):
        cells = []
        x, y = position
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx != 0 or dy != 0:
                    neighbor_position = (x + dx, y + dy)
                    if self.is_position_valid(neighbor_position):
                        cells.append(self.get_cell(neighbor_position))
        return cells

    def is_position_valid(self, position):
        from .organisms.plants.Hogweed import Hogweed
        x, y = position
        return 0 <= x < self.__width and 0 <= y < self.__height and (isinstance(self.get_cell(position).get_org(), Hogweed) or self.get_cell(position).get_org() is None)

