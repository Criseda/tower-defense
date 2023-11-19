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
from os import path
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


class Tower:

    def __init__(self, canvas, size, cell_size):
        self.canvas = canvas
        self.size = size
        self.cell_size = cell_size
        self.tower = None

    def place_tower(self, x, y):

        self.tower = self.canvas.create_rectangle(x * self.cell_size,
                                                  y * self.cell_size,
                                                  (x + self.size) *
                                                  self.cell_size,
                                                  (y + self.size) *
                                                  self.cell_size,
                                                  fill="red")


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

    def move_circle(self, delay=20):
        global route
        if route:
            if self.current_coordinate_index < len(route):
                x, y = route[self.current_coordinate_index]
                self.canvas.coords(self.circle, x-self.radius,
                                   y-self.radius, x+self.radius, y+self.radius)
                self.canvas.update()
                self.current_coordinate_index += 1
                # Schedule next move
                # 2nd delay might be redundant, removing it
                self.canvas.after(delay, self.move_circle)


class MapGenerator:

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

    def get_path_coordinates(self):

        return self.path_coordinates

    def draw_map(self):

        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                # dark brown for road, green for grass
                color = "#8B4513" if cell == 1 else "green"
                self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                             (x + 1) * self.cell_size, (y +
                                                                        1) * self.cell_size,
                                             fill=color)

    def draw_map_from_file(self, filename):

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

    def __init__(self):
        self.root = Tk()
        self.root.title("Tower Defense Game")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        self.root.config(bg="black")
        self.circles = []
        self.cell_size = 20
        self.towers = []
        self.tower_coordinates = {}

        # this is the frame that holds the canvas
        self.frame = TkFrame(self.root, width=1000, height=720, bg="blue")
        self.frame.pack(side='left')

        # this is the canvas that holds the map / circle
        self.canvas = TkCanvas(self.frame, width=1000, height=720, bg="white")
        self.canvas.pack()

        self.canvas.bind("<Button-3>", self.place_tower)

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
        self.map_generator = MapGenerator(
            self.canvas, 50, 36, cell_size=self.cell_size)

        self.map_generator.draw_map_from_file("coords.txt")

        self.start_circles()

        self.root.mainloop()

    def create_circles_newnew(self, num_circles):
        for _ in range(num_circles):
            circle = MovingCircle(self.canvas, self.cell_size//2)
            self.circles.append(circle)

    def update_circles(self, circle_index=0):
        if circle_index < len(self.circles):
            # Move the circle
            self.circles[circle_index].move_circle()

            # Schedule the next update with a delay
            delay_between_circles = 400  # Adjust this value as needed
            self.root.after(delay_between_circles,
                            self.update_circles, circle_index + 1)
        else:
            # All circles have been moved, schedule the next update
            self.root.after(1000, self.update_circles)

    def start_circles(self):
        # delay from circle to another
        self.create_circles_newnew(num_circles=5)
        self.update_circles()

    def tower_placement_valid(self, x, y):
        # Check if the square under the tower is brown or if there is already a tower placed
        # Convert tower coordinates to match the scale factor of path coordinates
        x *= self.cell_size
        y *= self.cell_size

        # Check if the square under the tower is brown or if there is already a tower placed
        path_x = x // self.cell_size
        path_y = y // self.cell_size
        if self.map_generator.map[path_y][path_x] == 1 or (path_x, path_y) in self.map_generator.get_path_coordinates():
            print("You cannot place a tower over the path!")
            return False

        # Check if there is already a tower placed at the given coordinates
        for tower in self.towers:
            tower_x, tower_y = self.tower_coordinates[tower]
            if tower_x == path_x and tower_y == path_y:
                print("You cannot place a tower onto another tower!")
                return False

        return True

    def place_tower(self, event):
        # Calculate the grid coordinates based on the mouse click position
        x = event.x // self.cell_size
        y = event.y // self.cell_size

        # Check if the square under the tower is brown or if there is already a tower placed
        if self.tower_placement_valid(x, y):
            tower = Tower(self.canvas, 3, self.cell_size)
            self.towers.append(tower)
            self.tower_coordinates[tower] = (x, y)
            tower.place_tower(x, y)

    def new_game(self):
        messagebox.showinfo("New Game", "Starting a new game!")

    def save_game(self):
        messagebox.showinfo("Save Game", "Game saved!")

    def load_game(self):
        messagebox.showinfo("Load Game", "Game loaded!")

    def about(self):
        messagebox.showinfo("About", "Tower Defense Game by Your Name")

# ---RUN PROGRAM--- #


def main():
    """
    The main function of the game_solution module.
    """
    Game()
    # create_smooth_path('middle.txt', 'middle_smooth.txt', steps=25)


if __name__ == "__main__":
    main()  # this will initialise the program
