import tkinter as tk
from tkinter import messagebox

class InputWindow:
    def __init__(self, master, width, height):
        self.master = master
        self.w = width
        self.h = height
        master.title("Input Dimensions")

        self.label = tk.Label(master, text="Enter width and height (5-99):")
        self.label.pack()

        self.width_label = tk.Label(master, text="Width:")
        self.width_label.pack()
        self.width_entry = tk.Entry(master)
        self.width_entry.pack()

        self.height_label = tk.Label(master, text="Height:")
        self.height_label.pack()
        self.height_entry = tk.Entry(master)
        self.height_entry.pack()

        self.submit_button = tk.Button(master, text="Submit", command=self.submit)
        self.submit_button.pack()

    def submit(self):
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            if 5 <= width <= 99 and 5 <= height <= 99:
                self.master.destroy()
                self.w, self.h = width, height
                return width, height
            else:
                messagebox.showerror("Error", "Width and Height must be between 5 and 99")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers")

