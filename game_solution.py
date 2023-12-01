"""
This module contains the implementation of a Tower Defense Game.
Laurentiu Cristian Preda
initial commit: 09-11-2023
"""
import ast
import json
import time
from tkinter import Tk
from tkinter import (
    Menu as TkMenu,
    Frame as TkFrame,
    Canvas as TkCanvas,
    Button as TkButton,
    Label as TkLabel,
    Entry as TkEntry,
    messagebox,
    PhotoImage
)
from math import hypot, atan2, cos, sin
from PIL import Image, ImageTk
# ---All functions go here---


def read_coordinates(filename):
    """
    Read coordinates from a file and return a list of tuples.

    Args:
        filename (str): The path to the file containing the coordinates.

    Returns:
        list: A list of tuples representing the coordinates.
    """
    coordinates = []
    with open(filename, 'r', encoding="utf8") as file:
        for line in file:
            x, y = map(float, line.replace(
                '(', '').replace(')', '').split(','))
            coordinates.append((x, y))
    return coordinates


route = read_coordinates('route.txt')


class Leaderboard:
    """
    A class representing a leaderboard for a game.

    Attributes:
        filename (str): The filename of the leaderboard file.
        scores (list): A list of dictionaries representing the scores on the leaderboard.
    """

    def __init__(self, filename="leaderboard.json"):
        self.filename = filename
        self.scores = []

    def load_leaderboard(self):
        """
        Loads the leaderboard from the leaderboard file.
        If the file does not exist or is empty, initializes an empty leaderboard.
        """
        try:
            with open(self.filename, "r", encoding="utf8") as file:
                data = file.read()
                if data:
                    self.scores = json.loads(data)
                else:
                    self.scores = []
        except FileNotFoundError:
            self.scores = []

    def save_leaderboard(self):
        """
        Saves the leaderboard to the leaderboard file.
        """
        with open(self.filename, "w", encoding="utf8") as file:
            json.dump(self.scores, file)

    def add_score(self, initials, score):
        """
        Adds a score to the leaderboard.

        Args:
            initials (str): The initials of the player.
            score (int): The score achieved by the player.
        """
        self.scores.append({"initials": initials, "score": score})
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.save_leaderboard()

    def get_leaderboard(self):
        """
        Returns the leaderboard.

        Returns:
            list: A list of dictionaries representing the scores on the leaderboard.
        """
        return self.scores


class MainMenu:
    """
    Represents the main menu of the Tower Defense Game.

    Args:
        root (Tk): The root Tkinter window.
        game (Game): The instance of the Game class.

    Attributes:
        root (Tk): The root Tkinter window.
        game (Game): The instance of the Game class.
        main_menu_frame (TkFrame): The main menu frame.
    """

    def __init__(self, root, game):
        """
        Initializes the MainMenu class.

        Args:
            root (Tk): The root Tkinter window.
            game (Game): The instance of the Game class.
        """
        self.root = root
        self.game = game

        # Main menu frame
        self.main_menu_frame = TkFrame(root, bg="black")
        self.main_menu_frame.place(relwidth=1, relheight=1)

        # Title label
        title_label = TkLabel(
            self.main_menu_frame,
            text="Tower Defense Game",
            font=("Helvetica", 20),
            fg="white",
            bg="black"
        )
        title_label.pack(pady=50)

        # Buttons
        button_width = 15
        button_height = 2

        new_game_button = TkButton(
            self.main_menu_frame,
            text="New Game",
            font=("Helvetica", 16),
            command=self.start_new_game,
            width=button_width,
            height=button_height
        )
        new_game_button.pack(pady=20)

        load_game_button = TkButton(
            self.main_menu_frame,
            text="Load Game",
            font=("Helvetica", 16),
            command=self.load_game,
            width=button_width,
            height=button_height
        )
        load_game_button.pack(pady=20)

        settings_button = TkButton(
            self.main_menu_frame,
            text="Settings",
            font=("Helvetica", 16),
            command=self.open_settings,
            width=button_width,
            height=button_height
        )
        settings_button.pack(pady=20)

        exit_button = TkButton(
            self.main_menu_frame,
            text="Exit",
            font=("Helvetica", 16),
            command=self.root.destroy,
            width=button_width,
            height=button_height
        )
        exit_button.pack(pady=20)

    def open_settings(self):
        """
        Opens the settings menu.
        """
        # Open the settings menu
        settings_window = Tk()
        settings_window.title("Settings")
        settings_window.geometry("300x200")
        settings_window.resizable(False, False)

        # Create input fields for cheat/boss keys
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

        info_label = TkLabel(settings_window,
                             text="Click on a label to change the key.\nPress Escape to cancel.")
        info_label.pack(pady=20)

        # Exit button
        exit_button = TkButton(settings_window, text="Exit",
                               command=settings_window.destroy)
        exit_button.pack(pady=20)

        # Run the settings window
        settings_window.mainloop()

    def change_key(self, event, key_type):
        """
        Changes the cheat/boss key.

        Args:
            event (TkEvent): The event object.
            key_type (str): The type of key to change.
        """
        # Display "Enter key" and wait for user input
        original_text = event.widget.cget("text")

        def on_key_press(event):
            pressed_key = event.char.lower() if event.char else event.keysym
            if ord(pressed_key) == 27:  # Escape key
                label.config(text=original_text)
            elif pressed_key not in self.get_assigned_keys():
                self.update_key(event, label, key_type)
            else:
                label.config(
                    text=f"Cheat {key_type} key: {pressed_key.upper()} is already assigned!")
            label.unbind("<Key>")
            label.unbind("<FocusOut>")

        label = event.widget
        label.config(text=f"Cheat {key_type} key: Enter key")
        label.bind("<Key>", on_key_press)
        label.bind("<FocusOut>", lambda event: label.unbind("<Key>"))
        label.focus_set()

    def get_assigned_keys(self):
        """
        Returns a list of keys that have already been assigned.

        Returns:
            list: A list of assigned keys.
        """
        # Get a list of keys that have already been assigned
        assigned_keys = [
            self.game.cheat_money_key,
            self.game.cheat_health_key,
            self.game.boss_key
        ]

        return [key.lower() for key in assigned_keys if key]

    def update_key(self, event, label, key_type):
        """
        Updates the label with the pressed key and updates the game instance.

        Args:
            event (TkEvent): The event object.
            label (TkLabel): The label to update.
            key_type (str): The type of key to update.
        """
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
        """
        Starts a new game.
        """
        # Hide the main menu
        self.main_menu_frame.place_forget()

        # Start a new game logic (replace with your game initialization logic)
        # For demonstration, we'll print a message
        print("Starting a new game!")
        messagebox.showinfo("New Game", "New Game!")

    def load_game(self):
        """
        Loads a saved game.
        """
        try:
            # Load game logic here
            # For demonstration, we'll print a message
            print("Loading a saved game!")
            # load game logic here

            with open('save.json', 'r', encoding="utf8") as save_file:
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
                                  fire_rate=2000,
                                  dps=20,
                                  tower_type="sniper")
                elif tower_type == 'machine_gun':
                    tower = Tower(self.game.canvas, 3, self.game.cell_size,
                                  player=self.game.player,
                                  tower_range=150,
                                  fire_rate=200,
                                  dps=5,
                                  tower_type="machine_gun")
                else:
                    raise ValueError(f'Unknown tower type: {tower_type}')

                self.game.towers.append(tower)
                self.game.tower_coordinates[tower] = (tower_x, tower_y)
                tower.place_image_tower(tower_x, tower_y)

            self.game.update_player_info()

            # Hide the main menu
            self.main_menu_frame.place_forget()

            messagebox.showinfo("Load Game", "Game loaded!")

        except FileNotFoundError:
            messagebox.showerror("Load Game", "No save file found!")
            return


class Player:
    """A class representing a player in the game.

    Attributes:
        money (int): The amount of money the player has.
        health (int): The health of the player.
        score (int): The score of the player.

    Methods:
        __init__(
            self,
            starting_money=650,
            starting_health=100,
            score=0
        ): Initializes a new Player object.
        deduct_money(self, amount): Deducts the specified amount of money from the player.
        add_money(self, amount): Adds the specified amount of money to the player.
        add_health(self, amount): Adds the specified amount to the player's health.
        take_damage(self, amount): Reduces the player's health by the specified amount.
        increase_score(self, amount): Increases the player's score by the specified amount.
        is_game_over(self): Checks if the player's health is zero or below, indicating game over.
    """

    def __init__(self, starting_money=650, starting_health=100, score=0):
        """
        Initialize a new game instance.

        Args:
            starting_money (int): The starting amount of money for the game. Default is 650.
            starting_health (int): The starting health for the game. Default is 100.
            score (int): The initial score for the game. Default is 0.
        """
        self.money = starting_money
        self.health = starting_health
        self.score = score

    def deduct_money(self, amount):
        """
        Deducts the specified amount from the player's money.

        Args:
            amount (int): The amount to be deducted.

        Returns:
            None
        """
        self.money -= amount

    def add_money(self, amount):
        """
        Adds the specified amount of money to the player's balance.

        Parameters:
        - amount (int): The amount of money to add.

        Returns:
        None
        """
        self.money += amount

    def add_health(self, amount):
        """
        Adds the specified amount to the player's health.

        Args:
            amount (int): The amount of health to add.

        Returns:
            None
        """
        self.health += amount

    def take_damage(self, amount):
        """
        Reduces the player's health by the specified amount.

        Args:
            amount (int): The amount of damage to be taken.

        Returns:
            None
        """
        self.health -= amount
        print(f"Circle got away! Player health: {self.health}")

    def increase_score(self, amount):
        """
        Increases the score of the game by the specified amount.

        Args:
            amount (int): The amount by which to increase the score.
        """
        self.score += amount

    def is_game_over(self):
        """
        Check if the game is over.

        Returns:
            bool: True if the player's health is less than or equal to 0, False otherwise.
        """
        return self.health <= 0


class Tower:
    """
    Represents a tower in the game.

    Attributes:
    - canvas: The canvas on which the tower is placed.
    - size: The size of the tower.
    - cell_size: The size of each cell on the canvas.
    - player: The player who owns the tower.
    - fire_rate: The rate at which the tower can fire.
    - tower_range: The range of the tower.
    - tower_dps: The damage per second of the tower.
    - tower_type: The type of the tower.
    - tower_images: A dictionary of tower images.
    - barrel_line_tag: The tag used to identify the barrel line on the canvas.
    """

    def __init__(self, canvas, size, cell_size, player,
                 fire_rate=1000, tower_range='inf', dps=10,
                 tower_type="basic"):
        self.player = player
        self.canvas = canvas
        self.size = size
        self.cell_size = cell_size
        self.tower = None
        self.fire_rate = fire_rate
        self.last_shot_time = 0
        self.tower_range = tower_range
        self.tower_dps = dps
        self.tower_type = tower_type

        # Load tower images
        self.tower_images = {
            "basic": PhotoImage(file="basic.png"),
            "sniper": PhotoImage(file="sniper.png"),
            "machine_gun": PhotoImage(file="machine_gun.png"),
        }

        self.barrel_line_tag = f"barrel_line_{id(self)}"

    def rotate_tower_to_target(self, target):
        """
        Rotate the tower to face the target.

        Parameters:
        - target: The target to rotate the tower towards.
        """
        tower_x, tower_y = self.canvas.coords(self.tower)[:2]
        target_x, target_y = self.canvas.coords(target.circle)[:2]

        # Calculate the angle between the tower and the target
        angle_rad = atan2(target_y - tower_y, target_x - tower_x)

        # Set the length of the barrel line
        barrel_length = 30  # Adjust the length as needed

        # Calculate the end point of the line
        line_end_x = tower_x + barrel_length * cos(angle_rad)
        line_end_y = tower_y + barrel_length * sin(angle_rad)

        # Draw the barrel line
        self.canvas.delete(self.barrel_line_tag)  # Clear previous lines
        self.canvas.create_line(tower_x, tower_y,
                                line_end_x, line_end_y,
                                tags=self.barrel_line_tag, width=10,
                                fill="black")
        self.canvas.create_line(tower_x, tower_y,
                                line_end_x, line_end_y,
                                tags=self.barrel_line_tag, width=8,
                                fill="light gray")

    def place_image_tower(self, x, y):
        """
        Place the tower image on the canvas.

        Parameters:
        - x: The x-coordinate of the tower.
        - y: The y-coordinate of the tower.
        """
        tower_image = self.tower_images[self.tower_type]

        if tower_image:
            tower_x = x * self.cell_size + self.cell_size // 2
            tower_y = y * self.cell_size + self.cell_size // 2

            self.tower = self.canvas.create_image(tower_x, tower_y,
                                                  image=tower_image,
                                                  anchor="center")
        else:
            print("No tower image found!")

    def can_shoot(self):
        """
        Check if the tower can shoot.

        Returns:
        - True if the tower can shoot, False otherwise.
        """
        # Check if enough time has passed since the last shot
        current_time = time.time() * 1000  # Convert to milliseconds
        time_since_last_shot = current_time - self.last_shot_time

        # Check if the time since the last shot is greater than or equal to the fire rate
        return time_since_last_shot >= self.fire_rate

    def shoot(self, closest_circle):
        """
        Make the tower shoot at the closest circle.

        Parameters:
        - closest_circle: The closest circle to the tower.
        """
        # SHOOTING LOGIC HERE
        # DECREASE ITS HEALTH UNTIL IT REACHES ZERO,
        # THEN REMOVE IT FROM THE LIST OF CIRCLES AND CANVAS
        damage_per_shot = self.tower_dps

        # Rotate the tower to face the target
        self.rotate_tower_to_target(closest_circle)  # shoots

        self.last_shot_time = time.time() * 1000  # Update the last shot time

        closest_circle.decrease_health(damage_per_shot)

        if closest_circle.health <= 0:
            self.player.add_money(20)  # EDIT PLAYER MONEY REWARD HERE
            self.player.increase_score(100)  # EDIT PLAYER SCORE REWARD HERE
            print(
                f"Circle removed! Money: {self.player.money} Score: {self.player.score}")
            closest_circle.remove_circle()

    def find_closest_circle(self, circles):
        """
        Find the closest circle to the tower.

        Parameters:
        - circles: The list of circles to search from.

        Returns:
        - The closest circle to the tower.
        """
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
    """
    Represents a moving circle in the game.

    Attributes:
        canvas (object): The canvas object where the circle is drawn.
        player (object): The player object.
        game (object): The game object.
        radius (int): The radius of the circle (default is 10).
        health (int): The health of the circle (default is 100).
        x (int): The x-coordinate of the circle's initial position (default is -100).
        y (int): The y-coordinate of the circle's initial position (default is -100).
        circle (object): The circle object created on the canvas.
        current_coordinate_index (int): The index of the current coordinate in the route.
    """

    def __init__(self, canvas, player, game, radius=10, health=100, x=-100, y=-100):
        """
        Initializes a MovingCircle object.

        Args:
            canvas (object): The canvas object where the circle is drawn.
            player (object): The player object.
            game (object): The game object.
            radius (int, optional): The radius of the circle (default is 10).
            health (int, optional): The health of the circle (default is 100).
            x (int, optional): The x-coordinate of the circle's initial position (default is -100).
            y (int, optional): The y-coordinate of the circle's initial position (default is -100).
        """
        self.canvas = canvas
        self.radius = radius
        self.health = health
        self.player = player
        self.game = game
        self.circle = self.canvas.create_oval(
            x, y,
            x + radius * 2,
            y + radius * 2,
            fill='black'
        )
        self.current_coordinate_index = 0

    def move_circle(self, delay=20):
        """
        Moves the circle along the predefined route.

        Args:
            delay (int, optional): The delay between each move in milliseconds (default is 20).
        """
        if route:
            if self.current_coordinate_index < len(route):
                x, y = route[self.current_coordinate_index]
                self.canvas.coords(
                    self.circle,
                    x, y,
                    x+self.radius * 2,
                    y+self.radius * 2
                )
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
        """
        Returns the colour of the circle based on its health.

        Returns:
            str: The colour of the circle.
        """
        if self.health > 75:
            return "green"
        if self.health > 50:
            return "yellow"
        if self.health > 25:
            return "orange"
        return "red"

    def update_circle_colour(self):
        """
        Updates the circle colour based on current health.
        """
        self.canvas.itemconfig(self.circle, fill=self.get_circle_colour())

    def remove_circle(self):
        """
        Removes the circle from the canvas and updates the game state.
        """
        self.canvas.delete(self.circle)
        self.canvas.update()
        self.current_coordinate_index = 0

        if self in self.game.circles:
            self.game.circles.remove(self)

    def decrease_health(self, damage):
        """
        Decreases the health of the circle by the specified amount and updates the circle colour.

        Args:
            damage (int): The amount of damage to be applied.
        """
        self.health -= damage
        self.update_circle_colour()

        if self.health <= 0:
            self.remove_circle()


class MapGenerator:
    """
    A class that generates and draws a map based on given parameters.

    Attributes:
        master (Tk): The master widget.
        width (int): The width of the map.
        height (int): The height of the map.
        cell_size (int): The size of each cell in the map.
        canvas (Tk.Canvas): The canvas widget to draw the map on.
        map (list): A 2D list representing the map.
        path_coordinates (list): A list to store the coordinates of the selected path.
    """

    def __init__(self, master, width, height, cell_size):
        """
        Initializes a MapGenerator object.

        Args:
            master (Tk): The master widget.
            width (int): The width of the map.
            height (int): The height of the map.
            cell_size (int): The size of each cell in the map.
        """
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
        """
        Returns the coordinates of the selected path.

        Returns:
            list: The coordinates of the selected path.
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
        Draws the map based on the coordinates provided in a file.

        Args:
            filename (str): The path to the file containing the coordinates.
        """
        with open(filename, "r", encoding="utf8") as file:
            lines = file.readlines()
            coordinates = [ast.literal_eval(line.strip()) for line in lines]

        # Set the coordinates from the file as the new path
        for coordinate in coordinates:
            x, y = coordinate
            self.map[y][x] = 1
            self.path_coordinates.append((x, y))

        # Redraw the updated map
        self.draw_map()


class Game:
    """
    Represents the Tower Defense Game.

    The Game class is responsible for initializing and managing the Tower Defense game.
    It sets up the game window, initializes game variables, creates GUI elements,
    and binds event handlers.
    It also loads the boss image, creates the map, and starts the game loop.

    Attributes:
        root (Tk): The root window of the game.
        circles (list): A list to store the circles in the game.
        cell_size (int): The size of each cell in the game map.
        towers (list): A list to store the towers in the game.
        tower_coordinates (dict): A dictionary to store the coordinates of each tower.
        player (Player): The player object representing the player in the game.
        leaderboard (Leaderboard): The leaderboard object representing the leaderboard in the game.
        cheat_money_key (str): The key to activate the money cheat.
        cheat_health_key (str): The key to activate the health cheat.
        boss_key (str): The key to toggle the visibility of the boss frame.
        boss_image (ImageTk.PhotoImage): The image of the boss.
        game_in_progress (bool): A flag indicating whether the game is in progress.
        current_wave (int): The current wave number.
        num_circles_per_wave (list): A list of the number of circles per wave.
        time_between_waves (int): The time between waves in milliseconds.
        frame (TkFrame): The frame that holds the canvas.
        selection_frame (TkFrame): The frame that holds the buttons.
        score_label (TkLabel): The label to display the player's score.
        health_label (TkLabel): The label to display the player's health.
        money_label (TkLabel): The label to display the player's money.
        selected_tower_label (TkLabel): The label to display the selected tower.
        selected_tower_type (str): The type of the selected tower.
        basic_tower_price (int): The price of the basic tower.
        sniper_tower_price (int): The price of the sniper tower.
        machine_gun_tower_price (int): The price of the machine gun tower.
        canvas (TkCanvas): The canvas that holds the map and circles.
        main_menu (MainMenu): The main menu object representing the main menu screen.
        menu (TkMenu): The menu bar of the game window.
        boss_frame (TkFrame): The frame that holds the boss canvas.
        boss_canvas (TkCanvas): The canvas that displays the boss image.
        map_generator (MapGenerator):
        The map generator object responsible for creating and displaying the game map.
    """

    def __init__(self):
        """
        Initialize the Tower Defense Game.

        This function sets up the game window, initializes game variables, creates GUI elements,
        and binds event handlers.
        It also loads the boss image, creates the map, and starts the game loop.

        Parameters:
        None

        Returns:
        None
        """
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

        # Load the boss image
        boss_img = Image.open("important_document_cropped.jpg")
        boss_img = boss_img.resize((1280, 720), Image.LANCZOS)
        self.boss_image = ImageTk.PhotoImage(boss_img)

        self.root.bind("<Key>", self.cheat_handler)  # Cheat handler

        # variable to check if the game is in progress:
        self.game_in_progress = False

        # these are the waves
        self.current_wave = 0
        self.num_circles_per_wave = [
            5 + 4 * i if i < 5 else 5 + 5 *
            (i - 5) if i < 10 else 5 + 6 * (i - 10)
            for i in range(100)
        ]
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
        self.selected_tower_label = TkLabel(
            self.selection_frame, text="Selected Tower: None", bg="gray")
        self.selected_tower_label.pack(pady=5)

        # Tower selection buttons:
        button_width = 100
        button_height = 120

        # Variable to store the selected tower type:
        self.selected_tower_type = None

        self.basic_tower_price = 220
        basic_tower_image = PhotoImage(file="basic.png")
        basic_tower_button = TkButton(
            self.selection_frame,
            text=f"Normal Tower\nPrice: {self.basic_tower_price}",
            command=lambda: self.select_tower("basic"),
            image=basic_tower_image,
            compound="top",
            width=button_width,
            height=button_height
        )
        basic_tower_button.pack(pady=10)
        self.sniper_tower_price = 400
        sniper_tower_image = PhotoImage(file="sniper.png")
        sniper_tower_button = TkButton(
            self.selection_frame,
            text=f"Sniper Tower\nPrice: {self.sniper_tower_price}",
            command=lambda: self.select_tower("sniper"),
            image=sniper_tower_image,
            compound="top",
            width=button_width,
            height=button_height
        )
        sniper_tower_button.pack(pady=10)
        self.machine_gun_tower_price = 350
        machine_gun_tower_image = PhotoImage(file="machine_gun.png")
        machine_gun_tower_button = TkButton(
            self.selection_frame,
            text=f"Machine Gun\nPrice: {self.machine_gun_tower_price}",
            command=lambda: self.select_tower("machine_gun"),
            image=machine_gun_tower_image,
            compound="top",
            width=button_width,
            height=button_height
        )
        machine_gun_tower_button.pack(pady=10)

        # Start game button
        start_game_button = TkButton(
            self.selection_frame,
            text="Start Game",
            command=self.start_game,
            width=button_width,
            height=button_height
        )
        start_game_button.pack(pady=60, padx=50)

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

        self.menu.add_command(label="Exit program",
                              command=self.root.quit)  # exit button

        # Boss frame
        self.boss_frame = TkFrame(self.root,
                                  width=1280,
                                  height=720,
                                  bg="white")
        self.boss_frame.pack_propagate(0)  # Don't let it shrink
        # Boss canvas
        self.boss_canvas = TkCanvas(self.boss_frame,
                                    width=1280,
                                    height=720,
                                    bg="white")
        self.boss_canvas.create_image(0, 0,
                                      image=self.boss_image,
                                      anchor="nw")
        self.boss_canvas.pack()

        # Create and display the map
        self.map_generator = MapGenerator(
            self.canvas, 50, 36, cell_size=self.cell_size)

        self.map_generator.draw_map_from_file("coords.txt")

        self.start_circles()

        self.root.mainloop()

    def cheat_handler(self, event):
        """
        Handle cheat keys.

        This method is responsible for handling cheat keys.
        It checks the pressed key and performs the corresponding cheat action.
        If the cheat key is the money cheat key,
        it adds 100 units of money to the player's account and updates the player's information.

        Args:
            event (Event): The event object representing the key press event.

        Returns:
            None
        """
        pressed_key = event.char.lower() if event.char else event.keysym
        if pressed_key == self.cheat_money_key:
            self.player.add_money(100)
            print(f"Cheat activated! Money: {self.player.money}")
            self.update_player_info()
        elif pressed_key == self.cheat_health_key:
            self.player.add_health(100)
            print(f"Cheat activated! Health: {self.player.health}")
            self.update_player_info()
        elif pressed_key == self.boss_key:
            self.toggle_boss_frame()
        else:
            print(f"Unknown key: {pressed_key}")

    def toggle_boss_frame(self):
        """
        Toggles the visibility of the boss frame.

        If the boss frame is currently visible, it will be hidden.
        If the boss frame is currently hidden, it will be shown at position (0, 0).
        """
        if self.boss_frame.winfo_ismapped():
            self.boss_frame.place_forget()
        else:
            self.boss_frame.place(x=0, y=0)

    def show_game_over_screen(self):
        """
        Display the game over screen with a canvas/frame for entering initials.

        Args:
            self (object): The instance of the class.

        Returns:
            None
        """
        game_over_frame = TkFrame(self.root, width=400, height=200, bg="white")
        game_over_frame.pack_propagate(0)
        game_over_frame.place(x=400, y=260)

        label = TkLabel(game_over_frame,
                        text="Game Over!\nEnter Your Initials:")
        label.pack(pady=10)

        entry = TkEntry(game_over_frame)
        entry.pack(pady=10)

        submit_button = TkButton(
            game_over_frame,
            text="Submit",
            command=lambda: self.submit_score(entry.get())
        )
        submit_button.pack(pady=10)

    def submit_score(self, initials):
        """
        Submits the player's score to the leaderboard and displays the updated leaderboard.

        Args:
            initials (str): The player's initials.

        Returns:
            None
        """
        # Add the player's score to the leaderboard
        self.leaderboard.load_leaderboard()
        self.leaderboard.add_score(initials, self.player.score)

        # Display the leaderboard
        self.display_leaderboard()

    def display_leaderboard(self):
        """
        Display the leaderboard on the GUI.

        Retrieves the leaderboard data and displays it on a Tkinter frame.
        """
        leaderboard_frame = TkFrame(
            self.root, width=400, height=400, bg="white")
        leaderboard_frame.pack_propagate(0)
        leaderboard_frame.place(x=400, y=260)

        scores = self.leaderboard.get_leaderboard()

        label = TkLabel(leaderboard_frame, text="Leaderboard:")
        label.pack(pady=10)

        for score in scores:
            entry_label = TkLabel(
                leaderboard_frame,
                text=f"{score['initials']}: {score['score']}"
            )
            entry_label.pack(pady=5)

    def check_wave_completion(self):
        """
        Check if all circles have reached the end of the game area.
        If there are still circles remaining, the function will be called again after a short delay.
        If all circles have reached the end, it will start a new wave of circles.
        If the player's game is over, it will call the game_over function.
        """
        if self.circles:
            # Check again after a short delay
            self.root.after(100, self.check_wave_completion)
        else:
            # All circles have reached the end, start the new wave
            if self.player.is_game_over():
                self.game_over()
            self.root.after(self.time_between_waves, self.new_wave)

    def new_wave(self):
        """
        Increments the wave counter, displays a message box with the new wave number,
        creates circles for the current wave, and schedules the next wave if the player
        has not lost.
        """
        if self.player.is_game_over():
            return
        self.current_wave += 1
        messagebox.showinfo(
            "New Wave",
            f"Starting wave {self.current_wave}!"
        )
        num_circles = self.num_circles_per_wave[self.current_wave - 1]
        self.create_circles(num_circles)
        if not self.player.is_game_over():
            self.check_wave_completion()

    def game_over(self):
        """
        Ends the game and displays a message box with the game over information.
        """
        self.game_in_progress = False
        messagebox.showinfo(
            "Game Over",
            f"Game Over!\nWaves Survived: {self.current_wave}"
        )
        self.show_game_over_screen()

    def update_player_info(self):
        """
        Update the player's information labels.

        This method updates the score, health, and money labels with the current values
        from the player object.

        Args:
            None

        Returns:
            None
        """
        # Update player info labels
        self.score_label.config(text=f"Score: {self.player.score}")
        self.health_label.config(text=f"Health: {self.player.health}")
        self.money_label.config(text=f"Money: {self.player.money}")

    def create_circles(self, num_circles):
        """
        Create a specified number of circles and add them to the game.

        Args:
            num_circles (int): The number of circles to create.

        Returns:
            None
        """
        for _ in range(num_circles):
            circle = MovingCircle(self.canvas,
                                  player=self.player,
                                  game=self)
            self.circles.append(circle)

    def update_circles(self, circle_index=0):
        """
        Update the circles in the game.

        Parameters:
        - circle_index (int): The index of the circle to be updated. Default is 0.

        Returns:
        None
        """
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
                            self.update_circles,
                            circle_index + 1)

        else:
            # All circles have been moved, schedule the next update
            self.root.after(1000, self.update_circles)

    def start_circles(self):
        """
        Start the circles animation.

        This method starts the animation of circles by calling the necessary functions.
        It first starts the tower updates and then updates the circles.
        """
        self.start_tower_updates()
        self.update_circles()

    def select_tower(self, tower_type):
        """
        Selects a tower of the specified type.

        Args:
            tower_type (str): The type of tower to select.

        Returns:
            None
        """
        # Set the selected tower type
        self.selected_tower_type = tower_type
        # Update the label to show the selected tower
        self.selected_tower_label.config(
            text=f"Selected Tower: {tower_type.title()}"
        )

    def place_tower(self, event):
        """
        Places a tower on the game grid based on the mouse click position.

        Args:
            event (Event): The mouse click event.

        Returns:
            None
        """
        # Calculate the grid coordinates based on the mouse click position
        x = event.x // self.cell_size
        y = event.y // self.cell_size

        # Check if the square under the tower is brown or if there is already a tower placed
        if self.tower_placement_valid(x, y):
            if event.num == 1:  # Left click
                if self.selected_tower_type == "basic":
                    cost = self.basic_tower_price
                    if not self.can_afford_tower(cost):
                        return
                    basic_tower = Tower(self.canvas,
                                        3,
                                        self.cell_size,
                                        player=self.player,
                                        tower_range=200,
                                        fire_rate=800,
                                        dps=20,
                                        tower_type="basic")
                    self.towers.append(basic_tower)
                    self.tower_coordinates[basic_tower] = (x, y)
                    basic_tower.place_image_tower(x, y)
                    self.update_player_info()
                elif self.selected_tower_type == "sniper":
                    cost = self.sniper_tower_price
                    if not self.can_afford_tower(cost):
                        return
                    sniper_tower = Tower(self.canvas,
                                         3,
                                         self.cell_size,
                                         player=self.player,
                                         fire_rate=2000,
                                         dps=30,
                                         tower_type="sniper")
                    self.towers.append(sniper_tower)
                    self.tower_coordinates[sniper_tower] = (x, y)
                    sniper_tower.place_image_tower(x, y)
                    self.update_player_info()
                elif self.selected_tower_type == "machine_gun":
                    cost = self.machine_gun_tower_price
                    if not self.can_afford_tower(cost):
                        return
                    machine_gun_tower = Tower(self.canvas,
                                              3,
                                              self.cell_size,
                                              player=self.player,
                                              tower_range=150,
                                              fire_rate=200,
                                              dps=10,
                                              tower_type="machine_gun")
                    self.towers.append(machine_gun_tower)
                    self.tower_coordinates[machine_gun_tower] = (x, y)
                    machine_gun_tower.place_image_tower(x, y)
                    self.update_player_info()
                else:
                    print("No tower selected!")

    def tower_placement_valid(self, x, y):
        """
        Check if the tower placement is valid at the given coordinates.

        Args:
            x (int): The x-coordinate of the tower.
            y (int): The y-coordinate of the tower.

        Returns:
            bool: True if the tower placement is valid, False otherwise.
        """
        # Check if the square under the tower is brown or if there is already a tower placed
        # Convert tower coordinates to match the scale factor of path coordinates
        x *= self.cell_size
        y *= self.cell_size

        # Check if the square under the tower is brown or if there is already a tower placed
        path_x = x // self.cell_size
        path_y = y // self.cell_size
        if (
            self.map_generator.map[path_y][path_x] == 1
            or (path_x, path_y) in self.map_generator.get_path_coordinates()
        ):
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
        """
        Checks if the player can afford a tower with the given cost.

        Args:
            cost (int): The cost of the tower.

        Returns:
            bool: True if the player can afford the tower, False otherwise.
        """
        if self.player.money >= cost:
            self.player.deduct_money(cost)
            print(f"Placed tower. Money: {self.player.money}")
            self.update_player_info()
            return True
        print("You cannot afford this tower yet!")
        print(f"You need {cost - self.player.money} more money!")
        return False

    def update_towers(self):
        """
        Update the towers by finding the closest circle and shooting at it if possible.
        """
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
        """
        Updates the towers in the game.
        """
        self.update_towers()

    def start_game(self):
        """
        Starts the game if it is not already in progress.
        If the game is already in progress, it prints a message and continues the game.
        """
        if not self.game_in_progress:
            if self.current_wave == 0:
                messagebox.showinfo("Game Started", "Game started!")
            elif self.current_wave > 0:
                messagebox.showinfo(
                    "Game Started",
                    f"Game resumed! Resuming from wave {self.current_wave + 1}"
                )
            else:
                messagebox.showinfo("Game Started", "Game started!")
            self.game_in_progress = True
            self.new_wave()
        else:
            print("Game already started!")  # to not stop the game.

    def save_game(self):
        """Save the current game state to a JSON file."""
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

        with open('save.json', 'w', encoding="utf8") as save_file:
            json.dump(save_data, save_file)

        messagebox.showinfo("Save Game", "Game saved!")

# ---RUN PROGRAM--- #


def main():
    """
    The main function of the game_solution module.
    """
    Game()


if __name__ == "__main__":
    main()  # this will initialise the program
