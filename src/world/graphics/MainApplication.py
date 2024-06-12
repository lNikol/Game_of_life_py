import tkinter as tk
from ..organisms.plants.Plant import Plant
from ..organisms.animals.Animal import Animal
from ..Game import Game

class MainApplication:
    def __init__(self, root):
        read_log_file = False
        w = 0
        h = 0
        is_hex = False
        self.game = Game(read_log_file, is_hex)
        self.game_world = self.game.get_world()
        self.root = root
        self.root.title("Game of Life")
        self.setup_gui()

    def setup_gui(self):
        self.frame_main = tk.Frame(self.root)
        self.frame_main.pack(expand=True, fill=tk.BOTH)

        self.canvas = tk.Canvas(self.frame_main, bg="white", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.info_frame = tk.Frame(self.frame_main, bg="lightgray")
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.info_textbox = tk.Text(self.info_frame, height=10, width=30)
        self.info_textbox.pack(padx=10, pady=10)

        self.turn_button = tk.Button(self.info_frame, text="Take Turn", command=self.take_turn)
        self.turn_button.pack(padx=10, pady=10)

        self.load_button = tk.Button(self.info_frame, text="Save Game", command=self.save_game)
        self.load_button.pack(padx=10, pady=10)

        self.root.bind("<Key>", self.key_listener)

        # Ustawienie callbacka po zakończeniu uaktualnienia
        self.root.after_idle(self.setup_world)
        self.root.after_idle(self.draw_grid)

    def setup_world(self):
        self.organism_map = self.game_world.get_map()

    def draw_grid(self):
        self.canvas.delete("all")
        self.canvas.update()

        # Uzyskanie wymiarów Canvas
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()

        # Obliczenie rozmiaru komórki
        cell_size = min(canvas_width // self.game_world.get_width(), canvas_height // self.game_world.get_height()) * 3.25
        for y in range(self.game_world.get_height()):
            for x in range(self.game_world.get_width()):
                color = "white"
                organism = self.organism_map.get_cell([y, x]).get_org()
                if organism:
                    if isinstance(organism, Animal):
                        color = "red"
                    elif isinstance(organism, Plant):
                        color = "lightgreen"
                x0 = x * cell_size
                y0 = y * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="gray", fill=color)

                # Rysowanie literki organizmu, jeśli istnieje
                if organism:
                    sym = ""
                    if organism.get_name() == "Grass":
                        sym = "g"
                    elif organism.get_name() == "Hogweed":
                        sym = "h"
                    elif organism.get_name() == "Wolfberries":
                        sym = "w"
                    elif organism.get_name() == "CyberSheep":
                        sym = "C"
                    else:
                        sym = organism.get_name()[0]
                    self.canvas.create_text(x0 + cell_size // 2, y0 + cell_size // 2, text=sym,
                                            font=("Helvetica", 12))

    def take_turn(self):
        # Wykonanie tury gry
        # Tutaj dodaj logikę wykonania tury dla każdego organizmu

        # Przykładowe aktualizowanie organizmów na mapie
        self.game_world.take_a_turn()
        if self.game_world.get_human_is_alive:
            self.update_organisms()
            self.draw_grid()  # Rysowanie zaktualizowanej siatki
        else:
            self.close_ui()
            return False

    def update_organisms(self):
        self.organism_map = self.game_world.get_map()
    def save_game(self):
        self.game.write_to_log()
        # Implementacja logiki ładowania gry
        pass

    def add_text_to_box(self, text):
        # Funkcja dodająca tekst do Text widgetu
        self.info_textbox.config(state=tk.NORMAL)  # Ustawienie stanu na NORMAL aby modyfikować tekst
        self.info_textbox.insert(tk.END, text + "\n")
        self.info_textbox.config(state=tk.DISABLED)  # Ponowne ustawienie stanu na DISABLED
    def key_listener(self, event):
        key = event.keysym.lower()
        if key == 'w':  # Góra
            self.game_world.set_key('w')
        elif key == 'a':  # Lewo
            self.game_world.set_key('a')
        elif key == 's':  # Dół
            self.game_world.set_key('s')
        elif key == 'd':  # Prawo
            self.game_world.set_key('d')
        elif key == 'o':
            self.game_world.set_key('o')

    def close_ui(self):
        # Metoda do zamykania UI
        self.root.destroy()
