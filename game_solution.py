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
import time
from tkinter import Tk
from tkinter import (Menu as TkMenu,
                     Frame as TkFrame,
                     Canvas as TkCanvas,
                     messagebox as messagebox,
                     Button as TkButton)
from math import hypot
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


class Player:
    def __init__(self, starting_money=650, starting_health=100):
        self.money = starting_money
        self.health = starting_health

    def deduct_money(self, amount):
        self.money -= amount

    def add_money(self, amount):
        self.money += amount

    def take_damage(self, amount):
        self.health -= amount

    def is_game_over(self):
        return self.health <= 0


class Tower:

    def __init__(self, canvas, size, cell_size,
                 fire_rate=1000, tower_range='inf',
                 colour="red", shooting_colour="orange", dps=10):
        self.canvas = canvas
        self.size = size
        self.cell_size = cell_size
        self.tower = None
        self.init_colour = colour
        self.shooting_colour = shooting_colour
        self.fire_rate = fire_rate
        self.last_shot_time = 0
        self.tower_range = tower_range
        self.tower_dps = dps

    def can_shoot(self):
        # Check if enough time has passed since the last shot
        current_time = time.time() * 1000  # Convert to milliseconds
        time_since_last_shot = current_time - self.last_shot_time

        # Check if the time since the last shot is greater than or qual to the fire rate
        return time_since_last_shot >= self.fire_rate

    def shoot(self, closest_circle):
        # SHOOTING LOGIC HERE
        # DECREASE ITS HEALTH UNTIL IT REACHES ZERO,
        # THEN REMOVE IT FROM THE LIST OF CIRCLES AND CANVAS
        damage_per_shot = self.tower_dps

        self.flash_shooting_colour()  # shoots

        self.last_shot_time = time.time() * 1000  # Update the last shot time

        closest_circle.decrease_health(damage_per_shot)

        if closest_circle.health <= 0:
            self.circles.remove(closest_circle)
            closest_circle.remove_circle()

    def flash_shooting_colour(self):
        # Flash the shooting colour for a short time
        self.canvas.itemconfig(self.tower, fill=self.shooting_colour)
        self.canvas.after(100, self.restore_tower_colour)

    def restore_tower_colour(self):
        # Restore the tower colour to its original colour
        self.canvas.itemconfig(self.tower, fill=self.init_colour)

    def place_tower(self, x, y):

        self.tower = self.canvas.create_rectangle(x * self.cell_size,
                                                  y * self.cell_size,
                                                  (x + self.size) *
                                                  self.cell_size,
                                                  (y + self.size) *
                                                  self.cell_size,
                                                  fill=self.init_colour)

    def find_closest_circle(self, circles):
        tower_x, tower_y = self.canvas.coords(self.tower)[:2]

        closest_circle = None
        min_distance = float(self.tower_range)

        for circle in circles:
            try:
                circle_x, circle_y = self.canvas.coords(
                    circle.circle)[:2]  # Only unpack the first two values
            except ValueError:
                # The circle has been removed from the canvas, skip to next
                continue
            distance = hypot(circle_x - tower_x, circle_y - tower_y)

            if distance < min_distance:
                min_distance = distance
                closest_circle = circle

        return closest_circle


class MovingCircle:

    def __init__(self, canvas, radius=10, health=100, x=-100, y=-100):
        # x, y = -100 to be out of sight
        self.canvas = canvas
        self.radius = radius
        self.health = health
        self.circle = self.canvas.create_oval(x,
                                              y,
                                              x + radius * 2,
                                              y + radius * 2,
                                              fill='black')
        self.current_coordinate_index = 0

    def move_circle(self, delay=20):
        global route
        if route:
            if self.current_coordinate_index < len(route):
                x, y = route[self.current_coordinate_index]
                self.canvas.coords(self.circle,
                                   x,
                                   y,
                                   x+self.radius * 2,
                                   y+self.radius * 2)
                self.canvas.update()
                self.current_coordinate_index += 1

                if self.current_coordinate_index == len(route):
                    # The circle has reached the end of the path, remove it
                    self.remove_circle()
                else:
                    # Schedule next move
                    self.canvas.after(delay, self.move_circle)

    def get_circle_colour(self):
        # Return the colour of the circle based on its health
        if self.health > 75:
            return "green"
        elif self.health > 50:
            return "yellow"
        elif self.health > 25:
            return "orange"
        else:
            return "red"

    def update_circle_colour(self):
        # Update the circle colour based on current health
        self.canvas.itemconfig(self.circle, fill=self.get_circle_colour())

    def remove_circle(self):
        self.canvas.delete(self.circle)
        self.canvas.update()
        self.current_coordinate_index = 0

    def decrease_health(self, damage):
        self.health -= damage
        self.update_circle_colour()

        if self.health <= 0:
            self.remove_circle()


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

        # this is the player
        self.player = Player()

        # this is the frame that holds the canvas
        self.frame = TkFrame(self.root, width=1000, height=720, bg="blue")
        self.frame.pack(side='left')

        # this is the frame that holds the buttons
        self.selection_frame = TkFrame(self.root, width=280, height=720,
                                       bg="gray")
        self.selection_frame.pack(side='right')
        self.selection_frame.pack_propagate(0)

        # Tower selection buttons:
        button_width = 20
        button_height = 10

        basic_tower_button = TkButton(self.selection_frame, text="Normal Tower",
                                      command=lambda: self.select_tower(
                                          "basic"),
                                      width=button_width, height=button_height)
        basic_tower_button.pack(pady=10)
        sniper_tower_button = TkButton(self.selection_frame, text="Sniper Tower",
                                       command=lambda: self.select_tower(
                                           "sniper"),
                                       width=button_width, height=button_height)
        sniper_tower_button.pack(pady=10)
        machine_gun_tower_button = TkButton(self.selection_frame, text="Machine Gun Tower",
                                            command=lambda: self.select_tower(
                                                "machine_gun"),
                                            width=button_width, height=button_height)
        machine_gun_tower_button.pack(pady=10)

        # Variable to store the selected tower type:
        self.selected_tower_type = None

        # this is the canvas that holds the map / circle
        self.canvas = TkCanvas(self.frame, width=1000, height=720, bg="white")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.place_tower)

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

    def create_circles(self, num_circles):
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
        self.create_circles(num_circles=5)
        self.start_tower_updates()
        self.update_circles()

    def select_tower(self, tower_type):
        # Set the selected tower type
        self.selected_tower_type = tower_type

    def place_tower(self, event):
        # Calculate the grid coordinates based on the mouse click position
        x = event.x // self.cell_size
        y = event.y // self.cell_size

        # Check if the square under the tower is brown or if there is already a tower placed
        if self.tower_placement_valid(x, y):
            if event.num == 1:  # Left click
                match self.selected_tower_type:
                    case "basic":
                        cost = 170
                        if not self.can_afford_tower(cost):
                            return
                        basic_tower = Tower(self.canvas, 3, self.cell_size,
                                            tower_range=200,
                                            fire_rate=1000)
                        self.towers.append(basic_tower)
                        self.tower_coordinates[basic_tower] = (x, y)
                        basic_tower.place_tower(x, y)
                    case "sniper":
                        cost = 200
                        if not self.can_afford_tower(cost):
                            return
                        sniper_tower = Tower(self.canvas, 3, self.cell_size,
                                             colour="blue",
                                             shooting_colour="cyan",
                                             fire_rate=2000,
                                             dps=30)
                        self.towers.append(sniper_tower)
                        self.tower_coordinates[sniper_tower] = (x, y)
                        sniper_tower.place_tower(x, y)
                    case "machine_gun":
                        cost = 250
                        if not self.can_afford_tower(cost):
                            return
                        machine_gun_tower = Tower(self.canvas, 3, self.cell_size,
                                                  colour="yellow",
                                                  shooting_colour="lime",
                                                  tower_range=100,
                                                  fire_rate=200,
                                                  dps=5)
                        self.towers.append(machine_gun_tower)
                        self.tower_coordinates[machine_gun_tower] = (x, y)
                        machine_gun_tower.place_tower(x, y)
                    case _:
                        print("No tower selected!")

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

    def can_afford_tower(self, cost):
        if self.player.money >= cost:
            self.player.deduct_money(cost)
            return True
        else:
            print("You cannot afford this tower yet!")
            return False

    def update_towers(self):
        delay_between_shots = 100  # Frequent updates required to handle different fire rates

        for tower in self.towers:
            closest_circle = tower.find_closest_circle(self.circles)

            if closest_circle and tower.can_shoot():
                try:
                    tower.shoot(closest_circle)
                except AttributeError:
                    continue  # The circle has been removed from the canvas, skip to next

        self.root.after(delay_between_shots, self.update_towers)

    def start_tower_updates(self):
        self.update_towers()

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


if __name__ == "__main__":
    main()  # this will initialise the program
