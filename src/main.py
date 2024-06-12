import tkinter as tk
from world.graphics.InputWindow import InputWindow
from world.graphics.MainApplication import MainApplication

def main():
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
