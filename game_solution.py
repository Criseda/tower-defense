# Laurentiu Cristian Preda
# GAME SOLUTION - TOWER DEFENSE GAME!
# has to work in python 3.8
# tested on python 3.8.10
# initial commit: 09-11-2023
from tkinter import Tk
from tkinter import Button as TkButton, Label as TkLabel, Menu as TkMenu, Frame as TkFrame, Canvas as TkCanvas, messagebox as messagebox

# ---All functions go here---


class MapGenerator:
    def __init__(self, master, width, height, cell_size=30):
        self.master = master
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.canvas = TkCanvas(master, width=width * cell_size, height=height * cell_size, bg="white")
        self.canvas.pack()

        self.map = [[0 for _ in range(width)] for _ in range(height)]  # Initialize the map
        self.path_coordinates = []  # To store the coordinates of the selected path

        # Binding the left mouse click event to the canvas
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def on_canvas_click(self, event):
        # Calculate the grid coordinates based on the mouse click position
        x = event.x // self.cell_size
        y = event.y // self.cell_size

        # Toggle the path status of the clicked cell
        if self.map[y][x] == 0:
            self.map[y][x] = 1
            self.path_coordinates.append((x, y))
            self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                         (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                                         fill="black")
        else:
            self.map[y][x] = 0
            self.path_coordinates.remove((x, y))
            self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                         (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                                         fill="white")

    def get_path_coordinates(self):
        return self.path_coordinates

    def draw_map(self):
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                color = "black" if cell == 1 else "white"
                self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                             (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                                             fill=color)
    

class Game:
    def __init__(self):
        self.root = Tk()
        self.root.title("Tower Defense Game")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.config(bg="black")

        self.frame = TkFrame(self.root, bg="black") # this is the frame that holds the canvas
        self.frame.pack()

        self.canvas = TkCanvas(self.frame, width=800, height=600, bg="black") # this is the canvas that holds the game objects
        self.canvas.pack()

        self.menu = TkMenu(self.root) # menu bar
        self.root.config(menu=self.menu)

        self.file_menu = TkMenu(self.menu, tearoff=0) # file menu
        self.file_menu.add_command(label="New Game", command=self.new_game)
        self.file_menu.add_command(label="Save Game", command=self.save_game)
        self.file_menu.add_command(label="Load Game", command=self.load_game)
        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.help_menu = TkMenu(self.menu, tearoff=0)
        self.help_menu.add_command(label="About", command=self.about)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        
        for i in range(51):
            self.menu.add_command(label="", state="disabled") #empty space
        
        self.menu.add_command(label="Exit", command=self.root.quit) # exit button
        
        # Create and display the map
        map_generator = MapGenerator(self.canvas, 32, 24, cell_size=25)
        self.map_generator = map_generator


        self.root.mainloop()

    def new_game(self):
        # Print the path coordinates to the console
        path_coordinates = self.map_generator.get_path_coordinates()
        print("Predefined Path Coordinates:")
        for coordinate in path_coordinates:
            print(coordinate)
        messagebox.showinfo("New Game", "Starting a new game!")

    def save_game(self):
        messagebox.showinfo("Save Game", "Game saved!")

    def load_game(self):
        messagebox.showinfo("Load Game", "Game loaded!")

    def about(self):
        messagebox.showinfo("About", "Tower Defense Game by Your Name")


# ---RUN PROGRAM--- #
def main():
    game = Game()


if __name__ == "__main__":
    main()  # this will initialise the program
