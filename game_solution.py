"""
This module contains the implementation of a Tower Defense Game.
It uses tkinter for the GUI and provides classes for generating maps,
moving circles and the game itself.
"""

# Laurentiu Cristian Preda
# GAME SOLUTION - TOWER DEFENSE GAME!
# has to work in python 3.8
# tested on python 3.8.10
# initial commit: 09-11-2023
from tkinter import Tk
from tkinter import (Menu as TkMenu,
                     Frame as TkFrame,
                     Canvas as TkCanvas,
                     messagebox as messagebox)
# ---All functions go here---


def read_coordinates_new(filename):
    coordinates = []
    with open(filename, 'r', encoding="utf8") as file:
        for line in file:
            x, y = map(float, line.replace(
                '(', '').replace(')', '').split(','))
            coordinates.append((x, y))
    return coordinates


route = read_coordinates_new('route.txt')


class MovingCircle:
    """
    A class that represents a moving circle on a canvas.

    Attributes:
    canvas (tkinter.Canvas): The canvas on which the circle is drawn.
    radius (int): The radius of the circle.
    circle (int): The ID of the circle on the canvas.
    coordinates (list): A list of (x, y) coordinates that the circle will move to.
    """

    def __init__(self, canvas, radius=10):
        self.canvas = canvas
        self.radius = radius
        self.circle = self.canvas.create_oval(
            0, 0, radius*2, radius*2, fill='black')
        self.current_coordinate_index = 0


    def move_circle(self, delay=15):
        global route
        if route:
            if self.current_coordinate_index < len(route):
                x, y = route[self.current_coordinate_index]
                self.canvas.coords(self.circle, x-self.radius,
                                   y-self.radius, x+self.radius, y+self.radius)
                self.canvas.update()
                self.current_coordinate_index += 1
                # Schedule next move
                self.canvas.after(delay, self.move_circle, delay) # 2nd delay might be redundant


class MapGenerator:
    """
    A class used to generate and draw a map for a game.

    Attributes
    ----------
    master : tkinter.Canvas
        The canvas where the map will be drawn.
    width : int
        The width of the map in cells.
    height : int
        The height of the map in cells.
    cell_size : int
        The size of each cell in pixels.
    canvas : tkinter.Canvas
        The canvas where the map will be drawn.
    map : list
        A 2D list representing the map. Each element is either 0 (grass) or 1 (road).
    path_coordinates : list
        A list of tuples representing the coordinates of the selected path.

    Methods
    -------
    on_canvas_click(event)
        Toggles the path status of the clicked cell and updates the map accordingly.
    get_path_coordinates()
        Returns the coordinates of the selected path.
    draw_map()
        Draws the map on the canvas.
    draw_map_from_file(filename)
        Reads the coordinates of the selected path from a file and updates the map accordingly.
    """

    def __init__(self, master, width, height, cell_size):
        self.master = master
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.canvas = master
        self.canvas.pack()

        self.map = [[0 for _ in range(width)]
                    for _ in range(height)]  # Initialize the map
        self.path_coordinates = []  # To store the coordinates of the selected path

        # Binding the left mouse click event to the canvas
        # self.canvas.bind("<Button-1>", self.on_canvas_click)

    def on_canvas_click(self, event):
        """
        Toggles the path status of the clicked cell and updates the map accordingly.

        Parameters
        ----------
        event : tkinter.Event
            The mouse click event.
        """
        # Calculate the grid coordinates based on the mouse click position
        x = event.x // self.cell_size
        y = event.y // self.cell_size

        # Toggle the path status of the clicked cell
        if self.map[y][x] == 0:
            self.map[y][x] = 1
            self.path_coordinates.append((x, y))
            self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                         (x + 1) * self.cell_size, (y + 1) *
                                         self.cell_size,
                                         fill="black")
        else:
            self.map[y][x] = 0
            self.path_coordinates.remove((x, y))
            self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                         (x + 1) * self.cell_size, (y + 1) *
                                         self.cell_size,
                                         fill="white")

    def get_path_coordinates(self):
        """
        Returns the coordinates of the selected path.

        Returns
        -------
        list
            A list of tuples representing the coordinates of the selected path.
        """
        return self.path_coordinates

    def draw_map(self):
        """
        Draws the map on the canvas.
        """
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                # dark brown for road, green for grass
                color = "#8B4513" if cell == 1 else "green"
                self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                             (x + 1) * self.cell_size, (y +
                                                                        1) * self.cell_size,
                                             fill=color)

    def draw_map_from_file(self, filename):
        """
        Reads the coordinates of the selected path from a file and updates the map accordingly.

        Parameters
        ----------
        filename : str
            The name of the file containing the coordinates of the selected path.
        """
        with open(filename, "r", encoding="utf8") as file:
            lines = file.readlines()
            coordinates = [eval(line.strip()) for line in lines]

        # Set the coordinates from the file as the new path
        for coordinate in coordinates:
            x, y = coordinate
            self.map[y][x] = 1
            self.path_coordinates.append((x, y))

        # Redraw the updated map
        self.draw_map()


class Game:
    """
    A class representing the Tower Defense Game.

    Attributes:
    - root: The main window of the game.
    - circles: A list of MovingCircle objects representing the circles in the game.
    - cell_size: The size of each cell in the game.
    - frame: The frame that holds the canvas.
    - canvas: The canvas that holds the map and circles.
    - menu: The menu bar of the game.
    - file_menu: The file menu of the game.
    - help_menu: The help menu of the game.
    """

    def __init__(self):
        self.root = Tk()
        self.root.title("Tower Defense Game")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        self.root.config(bg="black")
        # new stuff I do not exactly get rn
        self.circles = []
        self.cell_size = 20

        # this is the frame that holds the canvas
        self.frame = TkFrame(self.root, width=1000, height=720, bg="blue")
        self.frame.pack(side='left')

        # this is the canvas that holds the map / circle
        self.canvas = TkCanvas(self.frame, width=1000, height=720, bg="white")
        self.canvas.pack()

        self.menu = TkMenu(self.root)  # menu bar
        self.root.config(menu=self.menu)

        self.file_menu = TkMenu(self.menu, tearoff=0)  # file menu
        self.file_menu.add_command(label="New Game", command=self.new_game)
        self.file_menu.add_command(label="Save Game", command=self.save_game)
        self.file_menu.add_command(label="Load Game", command=self.load_game)
        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.help_menu = TkMenu(self.menu, tearoff=0)
        self.help_menu.add_command(label="About", command=self.about)
        self.menu.add_cascade(label="Help", menu=self.help_menu)

        self.menu.add_command(label="Exit program",
                              command=self.root.quit)  # exit button

        # Create and display the map
        map_generator = MapGenerator(
            self.canvas, 50, 36, cell_size=self.cell_size)
        map_generator.draw_map_from_file("coords.txt")

        self.start_circles()

        self.root.mainloop()

    def create_circles(self, num_circles, delay): #I AM UNSURE WHICH ONE IS BETTER
        for i in range(num_circles):
            circle = MovingCircle(self.canvas, self.cell_size//2)
            self.circles.append(circle)
            self.canvas.after(i * delay, circle.move_circle)

    def create_circles_new(self, num_circles, delay, i=0): # I AM UNSURE WHICH ONE IS BETTER
        if i < num_circles:
            circle = MovingCircle(self.canvas, self.cell_size//2)
            self.circles.append(circle)
            self.canvas.after(i * delay, circle.move_circle)
            self.canvas.after(delay, self.create_circles_new,
                              num_circles, delay, i+1)

    def start_circles(self):
        # delay from circle to another
        self.create_circles(num_circles=10, delay=1500)

    def new_game(self):
        messagebox.showinfo("New Game", "Starting a new game!")

    def save_game(self):
        messagebox.showinfo("Save Game", "Game saved!")

    def load_game(self):
        messagebox.showinfo("Load Game", "Game loaded!")

    def about(self):
        messagebox.showinfo("About", "Tower Defense Game by Your Name")


def create_smooth_path(input_file, output_file, steps=10):
    """
    Interpolates a smooth path between a series of coordinates and writes the result to a file.

    Args:
        input_file (str): The path to the input file containing the coordinates.
        output_file (str): The path to the output file to write the interpolated coordinates to.
        steps (int, optional): The number of steps to use for interpolation. Defaults to 10.
    """

    with open(input_file, 'r', encoding="utf8") as f:
        coordinates = [eval(line.strip()) for line in f]

    with open(output_file, 'w', encoding="utf8") as f:
        for i in range(len(coordinates) - 1):
            start_x, start_y = coordinates[i]
            end_x, end_y = coordinates[i + 1]

            # Generate and write interpolated coordinates
            for step in range(steps):
                t = step / steps
                x = start_x * (1 - t) + end_x * t
                y = start_y * (1 - t) + end_y * t
                f.write(f"({x}, {y})\n")

            # Write end coordinate
            f.write(f"({end_x}, {end_y})\n")

# ---RUN PROGRAM--- #


def main():
    """
    The main function of the game_solution module.
    """
    Game()
    # create_smooth_path('middle.txt', 'middle_smooth.txt', steps=25)


if __name__ == "__main__":
    main()  # this will initialise the program
