from Map import Map
from src.world.organisms.animals.Human import Human
from src.world.organisms.Organism import Organism
import random
import importlib.util
import re
import sys

class World:
    def __init__(self, w, h, read_file, file_name, is_hex):
        self.__width = w
        self.__height = h
        self.__read_file = read_file
        self.__file_name = file_name
        self.__is_hex = is_hex
        self.__map = Map(w, h, self)
        self.__organisms = []
        self.__organisms_in_game = []
        self.__children = []
        self.__human = None
        self.__key_pressed = False
        self.__human_is_alive = True
        self.__is_player_turn = False
        self.generate_world()

    def generate_world(self):
        if self.__read_file:
            self.read_from_file()
        else:
            if self.__is_hex:
                self.__width = self.__height
            self.__human = Human(0, 0, self)
            self.__organisms.append(self.__human)
            self.__map.set_organism([0, 0], self.__human)
            for i in range(self.__height):
                for j in range(self.__width):
                    if j % 4 == 1:
                        # Plant generate
                        rand_pos = self.random_position()
                        if rand_pos[0] == -1:
                            continue
                        try:
                            org_index = (i + j) % 5
                            org = self.get_organism_class(org_index)
                            if org not in self.__organisms_in_game:
                                self.__organisms_in_game.append(org)
                            new_org = org(rand_pos, self)
                            self.__map.set_organism(rand_pos, new_org)
                            self.__organisms.append(new_org)
                        except Exception as e:
                            print(e)
                    elif j % 4 == 0:
                        # Animal generate
                        rand_pos = self.random_position()
                        if rand_pos[0] == -1:
                            continue
                        try:
                            org_index = (i + j) % 5 + 5
                            org = self.get_organism_class(org_index)
                            if org not in self.__organisms_in_game:
                                self.__organisms_in_game.append(org)
                            new_org = org(rand_pos, self)
                            self.__map.set_organism(rand_pos, new_org)
                            self.__organisms.append(new_org)
                        except Exception as e:
                            print(e)

    def get_key_pressed(self):
        return self.__key_pressed

    def set_key_pressed(self, pressed):
        self.__key_pressed = pressed

    def set_key(self, s):
        self.__human.set_key(s)

    def get_key(self):
        return self.__human.get_key()

    def set_organism(self, position, org):
        if self.__map.get_cell(position).org is None:
            child = org.copy(position)
            self.__children.append(child)
            self.__map.set_organism(position, child)
            return True
        else:
            print(f"setOrganism in World: Cannot set organism, the place by (y,x) {position[0]}, {position[1]} isn't null")
            return False

    def get_organism_class(self, index):
        org_module = f"organisms.animals.Animal" if index < 5 else "organisms.plants.Plant"
        org_name = "Human" if index == 0 else f"Organism{index}"
        try:
            spec = importlib.util.find_spec(org_module)
            org_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(org_module)
            org_class = getattr(org_module, org_name)
            return org_class
        except Exception as e:
            raise RuntimeError(f"Error loading organism class: {e}")

    def read_from_file(self):
        try:
            with open(self.__file_name, "r") as file:
                lines = file.readlines()
                # Continue with file parsing
        except FileNotFoundError:
            print("File not found.")
            # Handle the exception

    def random_position(self):
        x = random.randint(0, self.__width - 1)
        y = random.randint(0, self.__height - 1)
        return [y, x]

    def update_organisms(self):
        children_size = len(self.__children)
        for i in range(children_size):
            if self.__children[i] is not None:
                self.__organisms.append(self.__children[i])
        self.__children.clear()

        i = len(self.__organisms) - 1
        while i >= 0:
            if not self.__organisms[i].is_alive():
                self.__organisms.pop(i)
            i -= 1

        self.__organisms.sort(key=lambda x: (x.initiative, -x.age), reverse=True)

    def take_a_turn(self):
        self.__human_is_alive = self.__human is not None and self.__human.is_alive()
        if self.__human_is_alive:
            for org in self.__organisms:
                org.age += 1
                org.has_moved = False
            self.update_organisms()
            for org in self.__organisms:
                if not org.has_moved and org.is_alive():
                    org.has_moved = True
                    org.action()
                    self.update_world()
        else:
            print("\n\nYou have died\n\n")

    def draw_world(self):
        s = ""
        for i in range(self.__height):
            for j in range(self.__width):
                org = self.__map.get_cell([i, j]).org
                if org is None:
                    s += " . "
                else:
                    sym = org.image[
                        0] if org.image != "Grass.png" and org.image != "Hogweed.png" and org.image != "Wolfberries.png" else \
                    org.image[0].lower()
                    s += f" {sym} "
            s += "\n"
        print(s)

    def update_world(self):
        for i in range(self.__height):
            for j in range(self.__width):
                c = self.__map.get_cell([i, j])
                if c.is_hex:
                    c.new_color = "white"
                else:
                    c.background = "white"
                c.children.clear()
                if c.org is not None:
                    label = c.org.name
                    if isinstance(c.org, Human):
                        if c.is_hex:
                            c.new_color = "red"
                        else:
                            c.background = "red"
                    elif isinstance(c.org, Plant):
                        if c.is_hex:
                            c.new_color = "green"
                        else:
                            c.background = "green"
                    c.children.append(label)

    def delete_organism(self, old_org):
        if old_org is None:
            return
        old_org.is_alive = False
        self.__map.delete_organism(old_org)
        self.__children.remove(old_org)

    def new_position(self, org, dist):
        w = self.__width - 1
        h = self.__height - 1
        pos = org.position
        y, x = pos[0], pos[1]

        if not self.__is_hex:
            if y == 0:
                if x == 0:
                    case = random.randint(1, 2)
                    if case == 1:  # right
                        x += dist
                    elif case == 2:  # right-down
                        x += dist
                        y += dist
                elif x == w:
                    case = random.randint(1, 3)
                    if case == 1:  # down
                        y += dist
                    elif case == 2:  # left
                        x -= dist
                    elif case == 3:  # left-down
                        if dist == 2:
                            x -= dist
                            y += dist
                else:
                    case = random.randint(1, 5)
                    if case == 1:  # down
                        y += dist
                    elif case == 2:  # right
                        x += dist if x + dist <= w else 1
                    elif case == 3:  # left
                        x -= dist if x - dist >= 0 else 1
                    elif case == 4:  # left-down
                        if x - dist >= 0:
                            x -= dist
                            y += dist
                        else:
                            x -= 1
                            y += 1
                    elif case == 5:  # right-down
                        if x + dist <= w:
                            x += dist
                            y += dist
                        else:
                            x += 1
                            y += 1
            elif y == h:
                if x == 0:
                    case = random.randint(1, 3)
                    if case == 1:  # top
                        y -= dist
                    elif case == 2:  # right
                        x += dist
                    elif case == 3:  # right-top
                        if dist == 2:
                            x += 1
                            y -= 1
                elif x == w:
                    case = random.randint(1, 2)
                    if case == 1:  # top
                        y -= 1
                    elif case == 2:  # left
                        x -= 1
                else:
                    case = random.randint(1, 5)
                    if case == 1:  # top
                        y -= 1
                    elif case == 2:  # left
                        x -= dist if x - dist >= 0 else 1
                    elif case == 3:  # right
                        x += dist if x + dist <= w else 1
                    elif case == 4:  # right-top
                        if x + dist <= w:
                            x += dist
                            y -= dist
                        else:
                            x += 1
                            y -= 1
                    elif case == 5:  # left-top
                        if x - dist >= 0:
                            x -= dist
                            y -= dist
                        else:
                            x -= 1
                            y -= 1
            elif x == w and 1 <= y < h:
                case = random.randint(1, 5)
                if case == 1:  # down
                    y += dist if y + dist <= h else 1
                elif case == 2:  # top
                    y -= dist if y - dist >= 0 else 1
                elif case == 3:  # left
                    x -= dist
                elif case == 4:  # left-top
                    if y - dist >= 0:
                        x -= dist
                        y -= dist
                    else:
                        x -= 1
                        y -= 1
                elif case == 5:  # left-down
                    if y + dist <= h:
                        x -= dist
                        y += dist
                    else:
                        x -= 1
                        y += 1
            elif x == 0 and 1 <= y < h:
                case = random.randint(1, 5)
                if case == 1:  # down
                    y += dist if y + dist <= h else 1
                elif case == 2:  # top
                    y -= dist if y - dist >= 0 else 1
                elif case == 3:  # right
                    x += dist
                elif case == 4:  # right-top
                    if y - dist >= 0:
                        x += dist
                        y -= dist
                    else:
                        x += 1
                        y -= 1
                elif case == 5:  # right-down
                    if y + dist <= h:
                        x += dist
                        y += dist
                    else:
                        x += 1
                        y += 1
            else:
                case = random.randint(1, 8)
                if case == 1:  # down
                    y += dist if y + dist <= h else 1
                elif case == 2:  # top
                    y -= dist if y - dist >= 0 else 1

    def get_width(self):
        return self.__width

    def get_human_is_alive(self):
        return self.__human_is_alive

    def get_height(self):
        return self.__height

    def get_is_hex(self):
        return self.__is_hex

    def get_map(self):
        return self.__map

    def get_organisms_in_game(self):
        return self.__organisms_in_game

    def set_is_hex(self, is_h):
        self.__is_hex = is_h

    def save_to_log(self):
        self.update_organisms()
        to_save = ""
        for i in range(len(self.__organisms)):
            to_save += self.__organisms[i].write_to_log()
        return to_save

    def read_from_file(self):
        try:
            with open(self.__file_name, 'r') as file:
                for line in file:
                    if not line.startswith("World:"):
                        first_word = line.split("(y,x): ")[0]
                        regex = r"\d+"
                        numbers = [0] * 5
                        index = 0
                        matcher = re.finditer(regex, line)
                        for match in matcher:
                            numbers[index] = int(match.group())
                            index += 1

                        for organism in Organism.organisms:
                            if first_word == organism.__name__:
                                pos = [numbers[0], numbers[1]]
                                if first_word == "Human":
                                    self.__human = Human(
                                        numbers[0], numbers[1], numbers[2], numbers[3], numbers[4], self
                                    )
                                    self.__map.set_organism(pos, self.__human)
                                    self.__organisms.append(self.__human)
                                else:
                                    self.set_organism(
                                        pos,
                                        organism(
                                            numbers[0], numbers[1], numbers[2], numbers[3], numbers[4], self
                                        ),
                                    )
                                    self.__organisms.append(self.__map.get_cell(pos).org)

                                    if organism not in self.__organisms_in_game:
                                        self.__organisms_in_game.append(organism)
        except IOError as e:
            print("Wystąpił błąd podczas odczytu pliku:", e)
