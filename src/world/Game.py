# import tkinter as tk
# from tkinter import messagebox
# from World import World
#
#
# class Game(tk.Tk):
#     def __init__(self, dane):
#         super().__init__()
#         self.dane = dane
#         self.__world = None
#         self.create_world(dane[0], dane[1], dane[2], dane[3])
#
#     def create_world(self, width, height, read, is_hex):
#         self.__world = World(width, height, read, is_hex)
#
#     def get_world(self):
#         return self.__world
#
#     def start_turn(self):
#         #if self.__world.get_key() != ' ':
#         print(f"\n\n\n\nTurn: {self.__world.turn_count}")
#         self.__world.take_a_turn()
#         #self.__world.set_key(' ')
#         #self.__world.set_key_pressed(False)
#         #self.update()
#
#     def save_to_log(self):
#         self.__world.save_to_log()
#         # try:
#         #     self.__world.save_to_log()
#         #     messagebox.showinfo("Info", "Gra została zapisana do log.log")
#         # except Exception as e:
#         #     messagebox.showerror("Error", f"Error saving game: {e}")
#
#     def read_log_file(self):
#         try:
#             with open("log.log", "r") as f:
#                 line = f.readline()
#                 if line.startswith("World:"):
#                     parts = line.split(" ")
#                     height = int(parts[2].split(",")[0])
#                     width = int(parts[-1])
#                     self.create_world(width, height, True, self.dane[2] == 1)
#                 else:
#                     self.create_world(self.dane[0], self.dane[1], False, self.dane[2] == 1)
#                     # czy is_hex : self.dane[2] == 1
#         except (FileNotFoundError, IOError):
#             self.create_world(self.dane[0], self.dane[1], False, self.dane[2] == 1)
#
#     def end_game(self):
#         self.destroy()
