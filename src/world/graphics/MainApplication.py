import tkinter as tk
from cmath import sqrt
from tkinter import Menu

class MainApplication:
    def __init__(self, root):
        self.cell_size = 0
        read_log_file = False
        w = 0
        h = 0
        is_hex = True
        from ..Game import Game
        self.game = Game(read_log_file, is_hex)
        self.game_world = self.game.get_world()
        self.root = root
        self.root.geometry("1200x900")  # Szerokość x Wysokość
        self.root.title("Game of Life")
        self.setup_gui()


    def show_organism_menu(self, event):
        menu = Menu(self.root, tearoff=0)
        organisms = self.game_world.get_organisms_in_game()  # Zakładamy, że istnieje metoda zwracająca dostępne organizmy
        for organism in organisms:
            menu.add_command(label=organism.__name__, command=lambda org=organism: self.add_organism(event.x, event.y, org))
        menu.post(event.x_root, event.y_root)
    def add_organism(self, x, y, organism):
        if not self.game_world.get_is_hex():
            cell_x = int(x // self.cell_size)
            cell_y = int(y // self.cell_size)
            print(self.game_world)

            org = organism([cell_y, cell_x], self.game_world)
            if self.organism_map.get_cell([cell_y, cell_x]).get_org() is None:
                self.organism_map.set_organism([cell_y, cell_x], org)
                self.game_world.append_org(org)
            self.draw_grid()
        else:
            cell_q, cell_r = self.pixel_to_hex(x, y)

            # Sprawdzenie, czy obliczone współrzędne mieszczą się w granicach planszy
            if 0 <= cell_q < self.game_world.get_width() and 0 <= cell_r < self.game_world.get_height():
                # Tworzenie organizmu na odpowiednich współrzędnych
                org = organism([cell_r, cell_q], self.game_world)

                # Sprawdzenie, czy na wybranej komórce nie ma już organizmu
                if self.organism_map.get_cell([cell_r, cell_q]).get_org() is None:
                    self.organism_map.set_organism([cell_r, cell_q], org)
                    self.game_world.append_org(org)
                    self.draw_grid()  # Odświeżenie siatki po dodaniu organizmu
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
        self.canvas.bind("<Button-3>", self.show_organism_menu)  # Bind right-click to show_organism_menu

        # Ustawienie callbacka po zakończeniu uaktualnienia
        self.root.after_idle(self.setup_world)
        self.root.after_idle(self.draw_grid)

    def setup_world(self):
        self.organism_map = self.game_world.get_map()

    def draw_grid(self):
        self.canvas.delete("all")
        self.canvas.update()

        # Uzyskanie wymiarów Canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if not self.game_world.get_is_hex():
            self.cell_size = min(canvas_width // self.game_world.get_width(), canvas_height // self.game_world.get_height()) * 0.75
            for y in range(self.game_world.get_height()):
                for x in range(self.game_world.get_width()):
                    color = "white"
                    organism = self.organism_map.get_cell([y, x]).get_org()
                    if organism:
                        from ..organisms.plants.Plant import Plant
                        from ..organisms.animals.Animal import Animal
                        if isinstance(organism, Animal):
                            color = "red"
                        elif isinstance(organism, Plant):
                            color = "lightgreen"
                    x0 = x * self.cell_size
                    y0 = y * self.cell_size
                    x1 = x0 + self.cell_size
                    y1 = y0 + self.cell_size
                    self.canvas.create_rectangle(x0, y0, x1, y1, outline="gray", fill=color)

                    # Rysowanie literki organizmu, jeśli istnieje
                    if organism:
                        sym = organism.get_name()[0]
                        self.canvas.create_text(x0 + self.cell_size // 2, y0 + self.cell_size // 2, text=sym,
                                                font=("Helvetica", 12))
        else:
            self.cell_size = min(canvas_width // self.game_world.get_width(), canvas_height // self.game_world.get_height()) * 0.6
            for y in range(self.game_world.get_height()):
                for x in range(self.game_world.get_width()):
                    color = "white"
                    organism = self.organism_map.get_cell([y, x]).get_org()
                    if organism:
                        from ..organisms.plants.Plant import Plant
                        from ..organisms.animals.Animal import Animal
                        if isinstance(organism, Animal):
                            color = "red"
                        elif isinstance(organism, Plant):
                            color = "lightgreen"
                    self.draw_hexagon(x, y, color)

                    # Rysowanie literki organizmu, jeśli istnieje
                    if organism:
                        sym = organism.get_name()[0]
                        x0, y0 = self.hex_to_pixel(x, y)
                        self.canvas.create_text(x0, y0, text=sym, font=("Helvetica", 12))

    def draw_hexagon(self, x, y, color):
        size = self.cell_size
        x0, y0 = self.hex_to_pixel(x, y)
        points = [
            x0 + size * 0.5, y0,
            x0 + size * 0.25, y0 + size * 0.433,
            x0 - size * 0.25, y0 + size * 0.433,
            x0 - size * 0.5, y0,
            x0 - size * 0.25, y0 - size * 0.433,
            x0 + size * 0.25, y0 - size * 0.433
        ]
        points = [abs(p) for p in points]  # Make sure all points are real numbers
        self.canvas.create_polygon(points, outline="gray", fill=color)

    def hex_to_pixel(self, q, r):
        size = self.cell_size
        x = size * (3/2 * q)
        y = size * (sqrt(3)/2 * q + sqrt(3) * r)
        return abs(x + self.cell_size)//1.8, abs(y + self.cell_size)//1.8  # Adjust for canvas offset and ensure values are real

    def pixel_to_hex(self, x, y):
        size = self.cell_size
        q = (2/3 * x) / size
        r = (-1/3 * x + sqrt(3)/3 * y) / size
        return int(q), int(r)

    def take_turn(self):
        # Wykonanie tury gry
        # Tutaj dodaj logikę wykonania tury dla każdego organizmu
        if self.game_world.get_human().get_key() == " ":
            self.update_organisms()
            self.draw_grid()  # Rysowanie zaktualizowanej siatki
            return
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
        elif key == 'q':
            self.game_world.set_key('q')
        elif key == 'o':
            self.game_world.set_key('o')

    def close_ui(self):
        # Metoda do zamykania UI
        self.root.destroy()
