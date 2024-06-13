import tkinter as tk
from cmath import sqrt
from tkinter import Menu
class MainApplication:
    def __init__(self, root):
        self.cell_size = 0
        read_log_file = input("Please write read_log_file (True or False): ")
        if read_log_file.lower() == "true":
            read_log_file = True
        else:
            print("Incorrect input in read_log_file or False")
            read_log_file = False
        is_hex = input("Please write is_hex (True or False): ")
        if is_hex.lower() == "true":
            is_hex = True
        else:
            print("Incorrect input in is_hex or False")
            is_hex = False
        from ..Game import Game
        self.game = Game(read_log_file, is_hex)
        self.game_world = self.game.get_world()
        self.root = root
        self.root.geometry("1200x900")  # Szerokość x Wysokość
        self.root.title("Game of Life")
        self.setup_gui()

    def show_organism_menu(self, event, y, x):
        menu = tk.Menu(self.root, tearoff=0)
        organisms = self.game_world.get_organisms_in_game()
        for organism in organisms:
            menu.add_command(label=organism.__name__,
                             command=lambda org=organism: self.add_organism(y, x, org))
        menu.post(event.x_root, event.y_root)

    def add_organism(self, y, x, organism):
            org = organism([y, x], self.game_world)
            if self.organism_map.get_cell([y, x]).get_org() is None:
                self.organism_map.set_organism([y, x], org)
                self.game_world.append_org(org)
            self.draw_grid()

    def setup_gui(self):
        self.frame_main = tk.Frame(self.root)
        self.frame_main.pack(expand=True, fill=tk.BOTH)

        self.canvas = tk.Canvas(self.frame_main, bg="white", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.info_frame = tk.Frame(self.frame_main, bg="lightgray")
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.info_textbox = tk.Text(self.info_frame, height=40, width=60)
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
                    self.canvas.tag_bind(self.canvas.create_rectangle(x0, y0, x1, y1, fill=color), "<Button-3>", lambda event, yy=y, xx=x: self.show_organism_menu(event, yy, xx))

                    if organism:
                        sym = organism.get_name()[0]
                        self.canvas.create_text(x0 + self.cell_size // 2, y0 + self.cell_size // 2, text=sym, font=("Helvetica", 12))
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
                    hexagon = self.draw_hexagon(x, y, color)
                    self.canvas.tag_bind(hexagon, "<Button-3>", lambda event, yy=y, xx=x: self.show_organism_menu(event, yy, xx))

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
        hexagon = self.canvas.create_polygon(points, outline="gray", fill=color)
        return hexagon

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
        self.add_text_to_box(f"\ntura {self.game_world.get_turn_count()}: Rozpoczięto turę \n")
        if self.game_world.get_human().get_key() == " ":
            self.update_organisms()
            self.draw_grid()
            self.add_text_to_box(self.game_world.get_messages())
            return
        self.game_world.take_a_turn()
        if self.game_world.get_human_is_alive:
            self.update_organisms()
            self.draw_grid()
            self.add_text_to_box(self.game_world.get_messages())
        else:
            self.close_ui()
            return False

    def update_organisms(self):
        self.organism_map = self.game_world.get_map()

    def save_game(self):
        self.add_text_to_box(f"tura {self.game_world.get_turn_count()}: Pobrano grę \n")
        self.game.write_to_log()
        # Implementacja logiki ładowania gry
        pass

    def add_text_to_box(self, messages):
        # Funkcja dodająca tekst do Text widgetu
        self.info_textbox.config(state=tk.NORMAL)  # Ustawienie stanu na NORMAL aby modyfikować tekst
        for message in messages:
            self.info_textbox.insert(tk.END, message)
        self.info_textbox.config(state=tk.DISABLED)
        self.game_world.set_messages()
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
