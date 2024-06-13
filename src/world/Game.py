import tkinter as tk
from tkinter import messagebox
import os

from .World import World


class Game(tk.Tk):
    def __init__(self, read_from_file=False, is_hex=False):
        super().__init__()
        self.dane = [0, 0, read_from_file, is_hex]
        self.__world = None
        if read_from_file:
            self.read_log_file()
            self.create_world(self.dane[0], self.dane[1], self.dane[2], self.dane[3])
        else:
            while self.dane[0] <= 4 or self.dane[0] >= 100 or self.dane[1] <= 4 or self.dane[1] >= 100:
                self.dane[0] = int(input("Write width (from 5 to 100): "))
                self.dane[1] = int(input("Write width (from 5 to 100): "))
            self.create_world(self.dane[0], self.dane[1], False, is_hex)


    def create_world(self, width, height, read, is_hex):
        self.__world = World(width, height, read, is_hex)

    def get_world(self):
        return self.__world

    def write_to_log(self):
        with open("log.log", 'w') as fw:
            info = self.__world.save_to_log()
            fw.write(info)
            fw.close()
            print(f"Gra została zapisana do log.log")

    def read_log_file(self, is_hex=False):
        try:
            with open("log.log", "r") as f:
                line = f.readline()
                if line.startswith("World:"):
                    parts = line.split(" ")
                    self.dane[0] = int(parts[2].split(",")[0])
                    self.dane[1] = int(parts[-1])
                else:
                    while self.dane[0] <= 4 or self.dane[0] >= 100 or self.dane[1] <= 4 or self.dane[1] >= 100:
                        self.dane[0] = input("Write width (from 5 to 100)")
                        self.dane[1] = input("Write width (from 5 to 100)")
                    # czy is_hex : self.dane[2] == 1
        except (FileNotFoundError, IOError):
            while self.dane[0] <= 4 or self.dane[0] >= 100 or self.dane[1] <= 4 or self.dane[1] >= 100:
                self.dane[0] = input("Write width (from 5 to 100)")
                self.dane[1] = input("Write width (from 5 to 100)")


    def end_game(self):
        self.destroy()
