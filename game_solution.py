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
# TODO: configure the leaderboard a little bit more
# TODO: boss key
# TODO: add tower prices, images, etc. on the tower buttons, make it easier to see what you can afford
# TODO: show the currently selected tower type on the screen somewhere, once placed, set tower_type held in hand to None
# TODO: create pixel art for the individual towers, initiate them with PIL
# TODO: With PIL, create functionality to rotate the tower image to face the closest circle

import json
import time
from tkinter import Tk
from tkinter import (Menu as TkMenu,
                     Frame as TkFrame,
                     Canvas as TkCanvas,
                     messagebox as messagebox,
                     Button as TkButton,
                     Label as TkLabel,
                     Entry as TkEntry)
from math import hypot
# ---All functions go here---


def read_coordinates(filename):
    coordinates = []
    with open(filename, 'r', encoding="utf8") as file:
        for line in file:
            x, y = map(float, line.replace(
                '(', '').replace(')', '').split(','))
            coordinates.append((x, y))
    return coordinates


route = read_coordinates('route.txt')


class Leaderboard:
    def __init__(self, filename="leaderboard.json"):
        self.filename = filename
        self.scores = []

    def load_leaderboard(self):
        try:
            with open(self.filename, "r") as file:
                self.scores = json.load(file)
        except FileNotFoundError:
            self.scores = []

    def save_leaderboard(self):
        with open(self.filename, "w") as file:
            json.dump(self.scores, file)

    def add_score(self, initials, score):
        self.scores.append({"initials": initials, "score": score})
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.save_leaderboard()

    def get_leaderboard(self):
        return self.scores


class MainMenu:
    def __init__(self, root, game):
        self.root = root
        self.game = game

        # Main menu frame
        self.main_menu_frame = TkFrame(root, bg="black")
        self.main_menu_frame.place(relwidth=1, relheight=1)

        # Title label
        title_label = TkLabel(self.main_menu_frame, text="Tower Defense Game", font=(
            "Helvetica", 20), fg="white", bg="black")
        title_label.pack(pady=50)

        # Buttons
        new_game_button = TkButton(
            self.main_menu_frame, text="New Game", command=self.start_new_game)
        new_game_button.pack(pady=20)

        load_game_button = TkButton(
            self.main_menu_frame, text="Load Game", command=self.load_game)
        load_game_button.pack(pady=20)

        exit_button = TkButton(self.main_menu_frame,
                               text="Exit", command=self.root.destroy)
        exit_button.pack(pady=20)
        settings_buton = TkButton(self.main_menu_frame,
                                  text="Settings", command=self.open_settings)
        settings_buton.pack(pady=20)

    def open_settings(self):
        # Open the settings menu
        settings_window = Tk()
        settings_window.title("Settings")
        settings_window.geometry("300x150")
        settings_window.resizable(False, False)
        
        #Create input fields for cheat/boss keys
        cheat_money_label = TkLabel(settings_window,
                                    text=f"Cheat Money Key: {self.game.cheat_money_key.upper()}")
        cheat_money_label.pack()
        cheat_money_label.bind("<Button-1>",
                               lambda event: self.change_key(event, "money"))
        cheat_money_label.focus_set()
        
        cheat_health_label = TkLabel(settings_window,
                                     text=f"Cheat Health Key: {self.game.cheat_health_key.upper()}")
        cheat_health_label.pack()
        cheat_health_label.bind("<Button-1>",
                                lambda event: self.change_key(event, "health"))
        cheat_health_label.focus_set()
        
        boss_label = TkLabel(settings_window,
                             text=f"Boss Key: {self.game.boss_key.upper()}")
        boss_label.pack()
        boss_label.bind("<Button-1>",
                        lambda event: self.change_key(event, "boss"))
        boss_label.focus_set()
        
        # Exit button
        exit_button = TkButton(settings_window, text="Exit",
                               command=settings_window.destroy)
        exit_button.pack(pady=20)
        
        # Run the settings window
        settings_window.mainloop()
 
    def change_key(self, event, key_type):
        # Display "Enter key" and wait for user input
        original_text = event.widget.cget("text")
        
        def on_key_press(event):
            pressed_key = event.char.lower() if event.char else event.keysym
            if ord(pressed_key) == 27: # Escape key
                label.config(text=original_text)
            elif pressed_key not in self.get_assigned_keys():
                self.update_key(event, label, key_type)
            else:
                label.config(text=f"Cheat {key_type} key: {pressed_key.upper()} is already assigned!")
            label.unbind("<Key>")
            label.unbind("<FocusOut>")
        
        label = event.widget
        label.config(text=f"Cheat {key_type} key: Enter key")
        label.bind("<Key>", on_key_press)
        label.bind("<FocusOut>", lambda event: label.unbind("<Key>"))
        label.focus_set()
    
    def get_assigned_keys(self):
        # Get a list of keys that have already been assigned
        assigned_keys = [
            self.game.cheat_money_key,
            self.game.cheat_health_key,
            self.game.boss_key
        ]
        
        return [key.lower() for key in assigned_keys if key]
        
    def update_key(self, event, label, key_type):
        # Update the label with the pressed key
        pressed_key = event.char.lower()
        if pressed_key and len(pressed_key) == 1:
            label.config(text=f"Cheat {key_type} key: {pressed_key.upper()}")
            if key_type == "money":
                self.game.cheat_money_key = pressed_key
            elif key_type == "health":
                self.game.cheat_health_key = pressed_key
            elif key_type == "boss":
                self.game.boss_key = pressed_key
        
    def start_new_game(self):
        # Hide the main menu
        self.main_menu_frame.place_forget()

        # Start a new game logic (replace with your game initialization logic)
        # For demonstration, we'll print a message
        print("Starting a new game!")
        messagebox.showinfo("New Game", "New Game!")

    def load_game(self):
        try:
            # Load game logic here
            # For demonstration, we'll print a message
            print("Loading a saved game!")
            # load game logic here

            with open('save.json', 'r') as save_file:
                save_data = json.load(save_file)
            self.game.player.money = save_data['player']['money']
            self.game.player.health = save_data['player']['health']
            self.game.player.score = save_data['player']['score']
            self.game.current_wave = save_data['current_wave'] - 1

            for tower_info in save_data['towers']:
                tower_type = tower_info['type']
                tower_x, tower_y = tower_info['coordinates']

                if tower_type == 'basic':
                    tower = Tower(self.game.canvas, 3, self.game.cell_size,
                                  player=self.game.player,
                                  tower_range=200,
                                  fire_rate=1000,
                                  tower_type="basic")
                elif tower_type == 'sniper':
                    tower = Tower(self.game.canvas, 3, self.game.cell_size,
                                  player=self.game.player,
                                  colour="blue",
                                  shooting_colour="cyan",
                                  fire_rate=2000,
                                  dps=30,
                                  tower_type="sniper")
                elif tower_type == 'machine_gun':
                    tower = Tower(self.game.canvas, 3, self.game.cell_size,
                                  player=self.game.player,
                                  colour="yellow",
                                  shooting_colour="lime",
                                  tower_range=100,
                                  fire_rate=200,
                                  dps=5,
                                  tower_type="machine_gun")
                else:
                    raise ValueError(f'Unknown tower type: {tower_type}')

                self.game.towers.append(tower)
                self.game.tower_coordinates[tower] = (tower_x, tower_y)
                tower.place_tower(tower_x, tower_y)

            self.game.update_player_info()

            # Hide the main menu
            self.main_menu_frame.place_forget()

            messagebox.showinfo("Load Game", "Game loaded!")

        except FileNotFoundError:
            messagebox.showerror("Load Game", "No save file found!")
            return


class Player:
    def __init__(self, starting_money=650, starting_health=100, score=0):
        self.money = starting_money
        self.health = starting_health
        self.score = score

    def deduct_money(self, amount):
        self.money -= amount

    def add_money(self, amount):
        self.money += amount
        
    def add_health(self, amount):
        self.health += amount

    def take_damage(self, amount):
        self.health -= amount
        print(f"Circle got away! Player health: {self.health}")

    def increase_score(self, amount):
        self.score += amount

    def is_game_over(self):
        return self.health <= 0


class Tower:

    def __init__(self, canvas, size, cell_size, player,
                 fire_rate=1000, tower_range='inf',
                 colour="red", shooting_colour="orange", dps=10,
                 tower_type="basic"):
        self.player = player
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
        self.tower_type = tower_type

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
            self.player.add_money(20)  # EDIT PLAYER MONEY REWARD HERE
            self.player.increase_score(100)  # EDIT PLAYER SCORE REWARD HERE
            print(
                f"Circle removed! Money: {self.player.money} Score: {self.player.score}")
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

    def __init__(self, canvas, player, game, radius=10, health=100, x=-100, y=-100):
        # x, y = -100 to be out of sight
        self.canvas = canvas
        self.radius = radius
        self.health = health
        self.player = player
        self.game = game
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
                    if self.circle in self.canvas.find_all():
                        self.player.take_damage(20)
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

        if self in self.game.circles:
            self.game.circles.remove(self)

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
        # this is the leaderboard
        self.leaderboard = Leaderboard()
        
        self.cheat_money_key = 'c'  # Default cheat money key
        self.cheat_health_key = 'v'  # Default cheat health key
        self.boss_key = 'b'  # Default boss key
        self.root.bind("<Key>", self.cheat_handler) # Cheat handler

        # variable to check if the game is in progress:
        self.game_in_progress = False

        # these are the waves
        self.current_wave = 0
        self.num_circles_per_wave = [5, 8, 12, 16, 20]
        self.time_between_waves = 1000  # 1 second between waves

        # this is the frame that holds the canvas
        self.frame = TkFrame(self.root, width=1000, height=720, bg="blue")
        self.frame.pack(side='left')

        # this is the frame that holds the buttons
        self.selection_frame = TkFrame(self.root, width=280, height=720,
                                       bg="gray")
        self.selection_frame.pack(side='right')
        self.selection_frame.pack_propagate(0)

        # Player info labels
        self.score_label = TkLabel(
            self.selection_frame, text="Score: 0", bg="gray")
        self.score_label.pack(pady=5)
        self.health_label = TkLabel(
            self.selection_frame, text="Health: 100", bg="gray")
        self.health_label.pack(pady=5)
        self.money_label = TkLabel(
            self.selection_frame, text="Money: 650", bg="gray")
        self.money_label.pack(pady=5)

        # Tower selection buttons:
        button_width = 20
        button_height = 10

        # Variable to store the selected tower type:
        self.selected_tower_type = None

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

        # Start game button
        start_game_button = TkButton(self.selection_frame, text="Start Game",
                                     command=lambda: self.start_game(),
                                     width=button_width, height=button_height)
        start_game_button.pack(pady=10)

        # this is the canvas that holds the map / circle
        self.canvas = TkCanvas(self.frame, width=1000, height=720, bg="white")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.place_tower)

        # Main menu screen
        self.main_menu = MainMenu(self.root, self)

        self.menu = TkMenu(self.root)  # menu bar
        self.root.config(menu=self.menu)

        self.menu.add_command(label="Save Game", command=self.save_game)

        self.menu.add_command(label="Start Game",
                              command=self.start_game)  # start button

        self.menu.add_command(label="About", command=self.about)

        self.menu.add_command(label="Exit program",
                              command=self.root.quit)  # exit button

        # Create and display the map
        self.map_generator = MapGenerator(
            self.canvas, 50, 36, cell_size=self.cell_size)

        self.map_generator.draw_map_from_file("coords.txt")

        self.start_circles()

        self.root.mainloop()
    
    def cheat_handler(self, event):
        # Handle cheat keys
        pressed_key = event.char.lower() if event.char else event.keysym
        if pressed_key == self.cheat_money_key:
            self.player.add_money(100)
            print(f"Cheat activated! Money: {self.player.money}")
            self.update_player_info()
        elif pressed_key == self.cheat_health_key:
            self.player.add_health(100)
            print(f"Cheat activated! Health: {self.player.health}")
            self.update_player_info()
        else:
            print(f"Unknown key: {pressed_key}")

    def show_game_over_screen(self):
        # Display a new canvas/frame for entering initials
        game_over_frame = TkFrame(self.root, width=400, height=200, bg="white")
        game_over_frame.pack_propagate(0)
        game_over_frame.place(x=400, y=260)

        label = TkLabel(game_over_frame,
                        text="Game Over!\nEnter Your Initials:")
        label.pack(pady=10)

        entry = TkEntry(game_over_frame)
        entry.pack(pady=10)

        submit_button = TkButton(
            game_over_frame, text="Submit", command=lambda: self.submit_score(entry.get()))
        submit_button.pack(pady=10)

    def submit_score(self, initials):
        # Add the player's score to the leaderboard
        self.leaderboard.load_leaderboard()
        self.leaderboard.add_score(initials, self.player.score)

        # Display the leaderboard
        self.display_leaderboard()

    def display_leaderboard(self):
        # Retrieve and display the leaderboard
        leaderboard_frame = TkFrame(
            self.root, width=400, height=400, bg="white")
        leaderboard_frame.pack_propagate(0)
        leaderboard_frame.place(x=400, y=260)

        scores = self.leaderboard.get_leaderboard()

        label = TkLabel(leaderboard_frame, text="Leaderboard:")
        label.pack(pady=10)

        for score in scores:
            entry_label = TkLabel(
                leaderboard_frame, text=f"{score['initials']}: {score['score']}")
            entry_label.pack(pady=5)

    def check_wave_completion(self):
        if self.circles:
            # Check again after a short delay
            self.root.after(100, self.check_wave_completion)
        else:
            # All circles have reached the end, start the new wave
            if self.player.is_game_over():
                self.game_over()
            self.root.after(self.time_between_waves, self.new_wave)

    def new_wave(self):
        # Increment the wave counter
        if self.player.is_game_over():
            return
        self.current_wave += 1
        messagebox.showinfo(
            "New Wave", f"Starting wave {self.current_wave}!")
        # Create the circles for the current wave
        num_circles = self.num_circles_per_wave[self.current_wave - 1]
        self.create_circles(num_circles)

        # Schedule the next wave if the player has not lost
        if not self.player.is_game_over():
            self.check_wave_completion()


    def game_over(self):
        self.game_in_progress = False
        messagebox.showinfo(
            "Game Over", "Game Over!\nWaves Survived: {}".format(self.current_wave))
        # Then do what you need to do for game over
        # TODO: Change this to retry or quit for later?
        # self.root.destroy()
        self.show_game_over_screen()

    def update_player_info(self):
        # Update player info labels
        self.score_label.config(text=f"Score: {self.player.score}")
        self.health_label.config(text=f"Health: {self.player.health}")
        self.money_label.config(text=f"Money: {self.player.money}")

    def create_circles(self, num_circles):
        for _ in range(num_circles):
            circle = MovingCircle(self.canvas, player=self.player, game=self)
            self.circles.append(circle)

    def update_circles(self, circle_index=0):
        if circle_index < len(self.circles):
            # Move the circle
            self.circles[circle_index].move_circle()

            # Check for game over
            if self.player.is_game_over():
                self.game_over()
                return

            # Update player info
            self.update_player_info()

            # Schedule the next update with a delay
            delay_between_circles = 400  # Adjust this value as needed
            self.root.after(delay_between_circles,
                            self.update_circles, circle_index + 1)

        else:
            # All circles have been moved, schedule the next update
            self.root.after(1000, self.update_circles)

    def start_circles(self):
        # delay from circle to another
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
                if self.selected_tower_type == "basic":
                    cost = 170
                    if not self.can_afford_tower(cost):
                        return
                    basic_tower = Tower(self.canvas, 3, self.cell_size,
                                        player=self.player,
                                        tower_range=200,
                                        fire_rate=1000,
                                        tower_type="basic")
                    self.towers.append(basic_tower)
                    self.tower_coordinates[basic_tower] = (x, y)
                    basic_tower.place_tower(x, y)
                    self.update_player_info()
                elif self.selected_tower_type == "sniper":
                    cost = 200
                    if not self.can_afford_tower(cost):
                        return
                    sniper_tower = Tower(self.canvas, 3, self.cell_size,
                                         player=self.player,
                                         colour="blue",
                                         shooting_colour="cyan",
                                         fire_rate=2000,
                                         dps=30,
                                         tower_type="sniper")
                    self.towers.append(sniper_tower)
                    self.tower_coordinates[sniper_tower] = (x, y)
                    sniper_tower.place_tower(x, y)
                    self.update_player_info()
                elif self.selected_tower_type == "machine_gun":
                    cost = 250
                    if not self.can_afford_tower(cost):
                        return
                    machine_gun_tower = Tower(self.canvas, 3, self.cell_size,
                                              player=self.player,
                                              colour="yellow",
                                              shooting_colour="lime",
                                              tower_range=100,
                                              fire_rate=200,
                                              dps=5,
                                              tower_type="machine_gun")
                    self.towers.append(machine_gun_tower)
                    self.tower_coordinates[machine_gun_tower] = (x, y)
                    machine_gun_tower.place_tower(x, y)
                    self.update_player_info()
                else:
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
            print(f"Placed tower. Money: {self.player.money}")
            self.update_player_info()
            return True
        else:
            print("You cannot afford this tower yet!")
            print(f"You need {cost - self.player.money} more money!")
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

    def start_game(self):
        print(self.game_in_progress)  # DEBUGGING
        if not self.game_in_progress:
            if self.current_wave == 0:
                messagebox.showinfo("Game Started", "Game started!")
            elif self.current_wave > 0:
                messagebox.showinfo("Game Started",
                                    f"Game resumed! Resuming from wave {self.current_wave + 1}")
            else:
                messagebox.showinfo("Game Started", "Game started! (debug)")
            self.game_in_progress = True
            self.new_wave()
        else:
            # messagebox.showinfo("Game Started", "Game already started!") DEBUG
            print("Game already started!")  # to not stop the game.

    def save_game(self):
        # save game logic here
        save_data = {
            'towers': [{'coordinates': tower_coordinates,
                        'type': tower.tower_type} for tower,
                       tower_coordinates in self.tower_coordinates.items()],
            'player': {
                'money': self.player.money,
                'health': self.player.health,
                'score': self.player.score,
            },
            'current_wave': self.current_wave,
        }

        with open('save.json', 'w') as save_file:
            json.dump(save_data, save_file)

        messagebox.showinfo("Save Game", "Game saved!")

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
