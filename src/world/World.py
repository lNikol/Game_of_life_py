import random
import re



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
        self.__children = []
        self.__human = None
        self.__human_is_alive = True
        self.__is_player_turn = False
        self.__key_pressed = False

        self.generate_world()

    def generate_world(self):
        #self.read_from_file()
        #else:

        if not self.__read_file:
            if self.__is_hex:
                self.__width = self.__height
            from .organisms.animals.Human import Human
            self.__human = Human(0, 0, self)
            self.__organisms.append(self.__human)
            self.__map.set_organism([0, 0], self.__human)

            for i in range(self.__height):
                for j in range(self.__width):
                    if j % 4 == 1:
                        rand_pos = self.random_position()
                        print(f"rand_pos: {rand_pos}")
                        if rand_pos == [-1, -1]:
                            continue
                        # zamienić Organism.organisms na inną tablicę
                        from src.world.organisms.Organisms import all_organisms
                        org_index = (i + j) % 6
                        org = all_organisms[org_index]
                        if org not in self.__organisms_in_game:
                            self.__organisms_in_game.append(org)
                        new_org = org(rand_pos, self)
                        self.__map.set_organism(rand_pos, new_org)
                        self.__organisms.append(new_org)
                    elif j % 4 == 0:
                        rand_pos = self.random_position()
                        print(f"rand_pos: {rand_pos}")
                        if rand_pos == [-1, -1]:
                            continue
                        from src.world.organisms.Organisms import all_organisms
                        org_index = i + j % 5 + 5
                        org = all_organisms[org_index]
                        print(f"Org: {org}")
                        if org not in self.__organisms_in_game:
                            self.__organisms_in_game.append(org)
                        new_org = org(rand_pos, self)
                        self.__map.set_organism(rand_pos, new_org)
                        self.__organisms.append(new_org)

    def random_position(self):
        counter = 0
        while counter < 300:
            x = random.randint(0, self.__width - 1)
            y = random.randint(0, self.__height - 1)
            if self.__map.get_cell(y, x).get_org() is None:
                return [y, x]
            counter += 1
        return [-1, -1]

    # def read_from_file(self):
    #     try:
    #         with open(self.__file_name, "r") as file:
    #             for line in file:
    #                 if not line.startswith("World:"):
    #                     data = re.findall(r'\d+', line)
    #                     if data:
    #                         numbers = list(map(int, data))
    #                         first_word = line.split("(y,x):")[0].strip()
    #                         for organism in Organism.organisms:
    #                             if first_word == organism.__name__:
    #                                 pos = [numbers[0], numbers[1]]
    #                                 if first_word == "Human":
    #                                     from organisms.animals.Human import Human
    #                                     self.__human = Human(numbers[0], numbers[1], numbers[2], numbers[3], numbers[4],
    #                                                        self)
    #                                     self.__map.set_organism(pos, self.__human)
    #                                     self.__organisms.append(self.__human)
    #                                 else:
    #                                     self.set_organism(pos, organism(numbers[0], numbers[1], numbers[2], numbers[3],
    #                                                                     numbers[4], self))
    #                                     self.__organisms.append(self.__map.get_cell(pos).org)
    #                                     if organism not in self.__organisms_in_game:
    #                                         self.__organisms_in_game.append(organism)
    #     except FileNotFoundError:
    #         print("File not found:", self.__file_name)

    def save_to_log(self):
        self.update_organisms()
        to_save = f"World({self.__width}_{self.__height}) "
        for org in self.__organisms:
            to_save += org.write_to_log()
        return to_save

    def update_organisms(self):
        children_size = len(self.__children)
        for i in range(children_size):
            if self.__children[i] is not None:
                self.__organisms.append(self.__children[i])
        self.__children.clear()

        i = len(self.__organisms) - 1
        while i >= 0:
            # czy wszystkich usunie?
            if not self.__organisms[i].get_is_alive():
                self.__organisms.pop(i)
            i -= 1

        self.__organisms.sort(key=lambda x: (x.get_initiative(), -x.get_age()))

    def take_a_turn(self):
        self.__human_is_alive = self.__human is not None and self.__human.get_is_alive()
        if self.__human_is_alive:
            for org in self.__organisms:
                org.set_age(org.get_age() + 1)
                org.set_has_moved(False)
            self.update_organisms()
            for org in self.__organisms:
                if not org.get_has_moved() and org.get_is_alive():
                    org.set_has_moved(True)
                    org.action()
                    #self.update_world()
        else:
            print("\n\nYou have died\n\n")
            return False

    def draw_world(self):
        s = ""
        for i in range(self.__height):
            for j in range(self.__width):
                org = self.__map.get_cell(i, j).org
                if org is None:
                    s += " . "
                else:
                    sym = ""
                    if org.get_name() == "Grass":
                        sym = "g"
                    elif org.get_name() == "Hogweed":
                        sym = "h"
                    elif org.get_name() == "Wolfberries":
                        sym = "W"
                    elif org.get_name() == "CyberSheep":
                        sym = "CS"
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
        self.__children.remove(old_org)

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
        if self.__map.get_cell(position).org is None:
            child = org.copy(position)
            self.__children.append(child)
            self.__map.set_organism(position, child)
            return True
        else:
            print("setOrganism in World: Cannot set organism, the place by (y,x)", position[0], ",", position[1],
                  "isn't null")
            return False

    def set_is_hex(self, is_hex):
        self.__is_hex = is_hex

    def get_is_hex(self):
        return self.__is_hex

    def get_human_is_alive(self):
        return self.__human_is_alive

    def get_map(self):
        return self.__map

    def get_organisms_in_game(self):
        return self.__organisms_in_game

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height
