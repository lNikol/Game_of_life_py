from .Animal import Animal
import random


class Human(Animal):
    def __init__(self, position, world, power=5, initiative=4, age=0):
        super().__init__("Human", position[0], position[1], power, initiative, world, age)
        self.__is_ability_on = False
        self.__is_ability_active = False
        self.__ability_key_pressed = False
        self.__last_key_pressed = " "
        self.__counter_after_ability = 0
        self.__ability_counter = -1
        self._world.add_message(f"Human ({self._y},{self._x}) was created")

    def copy(self, position):
        return Human(position, self._world)

    def action(self):
        self._world.add_message("\n\nYour turn\n")
        self._world.set_is_player_turn(True)
        self.move_system()
        self._world.set_is_player_turn(False)

    def set_key(self, key):
        self.__last_key_pressed = key
        if key == 'o':
            self.__ability_key_pressed = True
            self.__is_ability_on = True

    def get_key(self):
        return self.__last_key_pressed

    def set_ability_key_pressed(self, pressed):
        self.__ability_key_pressed = pressed

    def rebound_attack(self, org):
        return False

    def set_ability_active(self):
        if self.__ability_key_pressed:
            self.__ability_counter += 1
            if self.__ability_counter <= 2:
                self.__is_ability_active = True
            elif self.__ability_counter <= 4:
                self.__is_ability_active = random.choice([True, False])
            if self.__ability_counter >= 5:
                self.__counter_after_ability += 1
                self.__is_ability_active = False
                self.__is_ability_on = False
                if self.__counter_after_ability >= 5:
                    self.__counter_after_ability = 0
                    self.__ability_counter = 0
                    self.__ability_key_pressed = False
                else:
                    self._world.add_message("The ability cannot be activated")

    def move_system(self):
        s = f"{self._name} ({self._y}, {self._x} -> "

        if not self._world.get_is_hex():
            if self.__last_key_pressed == 'w':
                if self._y >= 1 and self._y < self._world.get_height():
                    self.set_ability_active()
                    if self.__is_ability_on and self.__is_ability_active:
                        if self._y - 2 >= 0:
                            self._y -= 2
                        else:
                            self._y -= 1
                            self._world.add_message(
                                "You cannot move two squares (you will move one square) because there is a border there \n")
                    else:
                        self._y -= 1
                    self.collision(self._world.get_cell(self.get_position()).get_org())
                    self._world.set_is_player_turn(False)
                else:
                    self._world.add_message("You cannot move to the top")
            elif self.__last_key_pressed == 's':
                if self._y >= 0 and self._y < self._world.get_height() - 1:
                    self.set_ability_active()
                    if self.__is_ability_on and self.__is_ability_active:
                        if self._y + 2 < self._world.get_height():
                            self._y += 2
                        else:
                            self._y += 1
                            self._world.add_message(
                                "You cannot move two squares (you will move one square) because there is a border there \n")
                    else:
                        self._y += 1
                    self.collision(self._world.get_cell([*self.get_position()]).get_org())
                    self._world.set_is_player_turn(False)
                else:
                    self._world.add_message("You cannot move to the bottom")
            elif self.__last_key_pressed == 'a':
                if self._x >= 1 and self._x < self._world.get_width():
                    self.set_ability_active()
                    if self.__is_ability_on and self.__is_ability_active:
                        if self._x - 2 >= 0:
                            self._x -= 2
                        else:
                            self._x -= 1
                            self._world.add_message(
                                "You cannot move two squares (you will move one square) because there is a border there \n")
                    else:
                        self._x -= 1
                    self.collision(self._world.get_cell([*self.get_position()]).get_org())
                    self._world.set_is_player_turn(False)
                else:
                    self._world.add_message("You cannot move to the left")
            elif self.__last_key_pressed == 'd':
                if self._x >= 0 and self._x < self._world.get_width() - 1:
                    self.set_ability_active()
                    if self.__is_ability_on and self.__is_ability_active:
                        if self._x + 2 < self._world.get_width():
                            self._x += 2
                        else:
                            self._x += 1
                            self._world.add_message(
                                "You cannot move two squares (you will move one square) because there is a border there \n")
                    else:
                        self._x += 1
                    self.collision(self._world.get_cell([*self.get_position()]).get_org())
                    self._world.set_is_player_turn(False)
                else:
                    self._world.add_message("You cannot move to the right")

        else:
            if self.__last_key_pressed == 'q':
                if 1 <= self._y < self._world.get_height():
                    self.set_ability_active()
                    # top
                    self._y -= 1
                    self._world.add_message("You cannot move two squares (you will move one square) because there is a border there \n")
                    self.collision(self._world.get_cell(self.get_position()).get_org())
                    self._world.set_is_player_turn(False)
                else:
                    self._world.add_message("You cannot move to the top")
            elif self.__last_key_pressed == 's':
                # down
                if 0 <= self._y < self._world.get_height() and 1 <= self._x < self._world.get_height():
                    self.set_ability_active()
                    self._y += 1
                    self.collision(self._world.get_cell(self.get_position()).get_org())
                    self._world.set_is_player_turn(False)
                else:
                    self._world.add_message("You cannot move to the down-down")
            elif self.__last_key_pressed == 'w':
                # góra-prawo
                if 1 <= self._y < self._world.get_height() and 0 <= self._x < self._world.get_height():
                    self.set_ability_active()
                    if self.__is_ability_on:
                        self._x += 1
                        self._y -= 1
                        self._world.set_is_player_turn(False)
                        self.collision(self._world.get_cell(self.get_position()).get_org())
                        self._world.set_is_player_turn(False)
                    else:
                        self._world.add_message("You cannot move to the top-top, please activate the ability")
                else:
                    self._world.add_message("You cannot move to the top-top, please activate the ability")
            elif self.__last_key_pressed == 'a':
                # left
                if 1 <= self._x < self._world.get_width():
                    self.set_ability_active()
                    if self.__is_ability_on:
                        if self._x - 2 >= 0:
                            self._x -= 2
                        else:
                            self._x -= 1
                            self._world.add_message(
                                "You cannot move two squares (you will move one square) because there is a border there \n")
                    else:
                        self._x -= 1
                    self.collision(self._world.get_cell(self.get_position()).get_org())
                    self._world.set_is_player_turn(False)
                else:
                    self._world.add_message("You cannot move to the left")
            elif self.__last_key_pressed == 'd':
                # right
                if 0 <= self._x < self._world.get_width() - 1:
                    self.set_ability_active()
                    if self.__is_ability_on:
                        if self._x + 2 < self._world.get_height():
                            self._x += 2
                        else:
                            self._x += 1
                            self._world.add_message(
                                "You cannot move two squares (you will move one square) because there is a border there \n")
                    else:
                        self._x += 1
                    self.collision(self._world.get_cell(self.get_position()).get_org())
                    self._world.set_is_player_turn(False)
                else:
                    self._world.add_message("You cannot move to the right")

        s += f"{self._y}, {self._x})"
        self._world.add_message(s)
        self.__last_key_pressed = " "