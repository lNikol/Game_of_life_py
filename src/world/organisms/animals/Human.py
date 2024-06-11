from .Animal import Animal

import random


class Human(Animal):
    def __init__(self, y, x, w):
        super().__init__("Human.png", "Human", 5, 4, y, x, w)
        self.__is_ability_on = False
        self.__is_ability_active = False
        self.__ability_key_pressed = False
        self.__last_key_pressed = ' '
        self.__counter_after_ability = 0
        self.__ability_counter = -1
        print(f"Human ({x},{y}) was created\n")

    def copy(self, position):
        return Human(position[0], position[1], self.__world)

    def action(self):
        print("\n\nYour turn\n\n")
        self.move_system()

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
                    print("The ability cannot be activated")

    def move_system(self):
        if not self.__world.is_hex:
            if self.__last_key_pressed == 'w':
                if self.__y >= 1 and self.__y < self.__world.height:
                    self.set_ability_active()
                    if self.__is_ability_on and self.__is_ability_active:
                        if self.__y - 2 >= 0:
                            self.__y -= 2
                        else:
                            self.__y -= 1
                            print(
                                "You cannot move two squares (you will move one square) because there is a border there \n")
                    else:
                        self.__y -= 1
                    self.__collision(self.__world.get_cell(self.get_position()).org)
                    self.__world.set_is_player_turn(False)
                else:
                    print("You cannot move to the top")
            elif self.__last_key_pressed == 's':
                if self.__y >= 0 and self.__y < self.__world.get_height() - 1:
                    self.set_ability_active()
                    if self.__is_ability_on and self.__is_ability_active:
                        if self.y + 2 < self.__world.get_height():
                            self.__y += 2
                        else:
                            self.__y += 1
                            print(
                                "You cannot move two squares (you will move one square) because there is a border there \n")
                    else:
                        self.__y += 1
                    self.__collision(self.__world.get_cell(self.get_position()).org)
                    self.__world.set_is_player_turn(False)
                else:
                    print("You cannot move to the bottom")
            elif self.__last_key_pressed == 'a':
                if self.__x >= 1 and self.__x < self.__world.get_width():
                    self.set_ability_active()
                    if self.__is_ability_on and self.__is_ability_active:
                        if self.__x - 2 >= 0:
                            self.__x -= 2
                        else:
                            self.__x -= 1
                            print(
                                "You cannot move two squares (you will move one square) because there is a border there \n")
                    else:
                        self.__x -= 1
                    self.__collision(self.__world.get_cell(self.get_position()).org)
                    self.__world.set_is_player_turn(False)
                else:
                    print("You cannot move to the left")
            elif self.__last_key_pressed == 'd':
                if self.__x >= 0 and self.__x < self.__world.get_width() - 1:
                    self.set_ability_active()
                    if self.__is_ability_on and self.__is_ability_active:
                        if self.__x + 2 < self.__world.get_width():
                            self.__x += 2
                        else:
                            self.__x += 1
                            print(
                                "You cannot move two squares (you will move one square) because there is a border there \n")
                    else:
                        self.__x += 1
                    self.__collision(self.__world.get_cell(self.get_position()).org)
                    self.__world.set_is_player_turn(False)
                else:
                    print("You cannot move to the right")
        else:
            # Implementacja ruchów dla szachownicy heksagonalnej
            pass
