# Laurentiu Cristian Preda
# GAME SOLUTION - TOWER DEFENSE GAME!
# has to work in python 3.8
# tested on python 3.8.10
# initial commit: 09-11-2023
from tkinter import Tk
from tkinter import Button as TkButton, Label as TkLabel, Menu as TkMenu, Frame as TkFrame, Canvas as TkCanvas

# ---All functions go here---


class Game:
    def __init__(self):
        """
        Initializes the game
        """
        # creates window
        self.window = Window("Game Solution").get_window()
        # creates a button
        self.play_button = Button(self.window,
                                  text="Play",
                                  command=None,
                                  x=0, y=0,
                                  width=100,
                                  height=50)
        # creates a label
        self.my_label = Label(self.window,
                              text="Hello World!",
                              x=200, y=200,
                              font=("Arial", 32),
                              bg="white",
                              fg="black",
                              width=250,
                              height=50)
        # starts the game
        self.window.mainloop()


class Window:
    def __init__(self, title, size="1280x720"):
        """
        Initializes the window
        :param title: title
        :param size: size (defaults to 1280x720 if not specified)
        """
        self.window = Tk()
        self.window.title(title)
        self.configure_window(size)

    def configure_window(self, window_size):
        # splits window_size into width and height
        width_height = window_size.split('x')
        window_width = int(width_height[0])
        window_height = int(width_height[1])
        # gets screen width and height
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        # sets position of window to centre of screen
        position_right = int((screen_width / 2) - (window_width / 2))
        position_down = int((screen_height / 2) - (window_height / 2))
        self.window.geometry(f"{window_size}+{position_right}+{position_down}")
        # prevents window from being resized
        self.window.resizable(False, False)

    def get_window(self):
        return self.window


class Enemy:
    def __init__(self, health, speed, damage, reward):
        """
        Initializes the health, speed, damage and reward of the enemy
        :param health: health
        :param speed: speed
        :param damage: damage
        :param reward: reward
        """
        self.health = health
        self.speed = speed
        self.damage = damage
        self.reward = reward

    def getHealth(self):
        """
        Returns the health of the enemy
        :return: health
        """
        return self.health

    def setHealth(self, health):
        """
        Sets the health of the enemy
        :param health: health
        :return: None
        """
        self.health = health

    def getSpeed(self):
        """
        Returns the speed of the enemy
        :return: speed
        """
        return self.speed

    def setSpeed(self, speed):
        """
        Sets the speed of the enemy
        :param speed: speed
        :return: None
        """
        self.speed = speed

    def getDamage(self):
        """
        Returns the damage of the enemy
        :return: damage
        """
        return self.damage

    def setDamage(self, damage):
        """
        Sets the damage of the enemy
        :param damage: damage
        :return: None
        """
        self.damage = damage

    def getReward(self):
        """
        Returns the reward of the enemy
        :return: reward
        """
        return self.reward

    def setReward(self, reward):
        """
        Sets the reward of the enemy
        :param reward: reward
        :return: None
        """
        self.reward = reward


class Tower:
    def __init__(self, cost, size):
        """
        Initializes the cost and size of the tower
        :param cost: cost
        :param size: size
        """
        self.cost = cost
        self.size = size

    def getCost(self):
        """
        Returns the cost of the tower
        :return: cost
        """
        return self.cost

    def setCost(self, cost):
        """
        Sets the cost of the tower
        :param cost: cost
        :return: None
        """
        self.cost = cost

    def getSize(self):
        """
        Returns the size of the tower
        :return: size
        """
        return self.size

    def setSize(self, size):
        """
        Sets the size of the tower
        :param size: size
        :return: None
        """
        self.size = size


class Projectile:
    def __init__(self, damage, speed, range):
        """
        Initializes the damage, speed and range of the projectile
        :param damage: damage
        :param speed: speed
        :param range: range
        """
        self.damage = damage
        self.speed = speed
        self.range = range

    def getDamage(self):
        """
        Returns the damage of the projectile
        :return: damage
        """
        return self.damage

    def setDamage(self, damage):
        """
        Sets the damage of the projectile
        :param damage: damage
        :return: None
        """
        self.damage = damage

    def getSpeed(self):
        """
        Returns the speed of the projectile
        :return: speed
        """
        return self.speed

    def setSpeed(self, speed):
        """
        Sets the speed of the projectile
        :param speed: speed
        :return: None
        """
        self.speed = speed

    def getRange(self):
        """
        Returns the range of the projectile
        :return: range
        """
        return self.range

    def setRange(self, range):
        """
        Sets the range of the projectile
        :param range: range
        :return: None
        """
        self.range = range


class Button:
    def __init__(self, window, text, command, x, y, width, height):
        """
        Initializes the text, command, x and y coordinates, width and height of the button
        :param window: Tk window
        :param text: text
        :param command: command
        :param x: x coordinate
        :param y: y coordinate
        :param width: width
        :param height: height
        """
        self.text = text
        self.command = command
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.button = TkButton(text=self.text, command=self.command)
        self.button.place(x=self.x, y=self.y,
                          width=self.width, height=self.height)


class Label:
    def __init__(self, window, text, x, y, font, bg, fg, width, height):
        """
        Initializes the text, x and y coordinates, font, background, foreground, width and height of the label
        :param window: Tk window
        :param text: text
        :param x: x coordinate
        :param y: y coordinate
        :param font: font
        :param bg: background
        :param fg: foreground
        :param width: width
        :param height: height
        """
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.bg = bg
        self.fg = fg
        self.width = width
        self.height = height
        self.label = TkLabel(text=self.text, font=self.font,
                             bg=self.bg, fg=self.fg)
        self.label.place(x=self.x, y=self.y,
                         width=self.width, height=self.height)


class Menu:
    pass


class Map:
    pass


class Path:
    pass


class Wave:
    def __init__(self, num_enemies, enemy_type, spawn_rate, spawn_delay):
        """
        Initializes the number of enemies, enemy type, spawn rate and spawn delay
        :param num_enemies: number of enemies
        :param enemy_type: enemy type
        :param spawn_rate: spawn rate
        :param spawn_delay: spawn delay
        """
        self.num_enemies = num_enemies
        self.enemy_type = enemy_type
        self.spawn_rate = spawn_rate
        self.spawn_delay = spawn_delay


class Player:
    def __init__(self):
        """
        Initializes the player's money, lives and score
        """
        self.money = 0
        self.lives = 10
        self.score = 0

    def getMoney(self):
        """
        Returns the amount of money the player has
        :return: money
        """
        return self.money

    def setMoney(self, money):
        """
        Sets the amount of money the player has
        :param money: money
        :return: None
        """
        self.money = money

    def getLives(self):
        """
        Returns the amount of lives the player has
        :return: lives
        """
        return self.lives

    def setLives(self, lives):
        """
        Sets the amount of lives the player has
        :param lives: lives
        :return: None
        """
        self.lives = lives

    def getScore(self):
        """
        Returns the score of the player
        :return: score
        """
        return self.score

    def setScore(self, score):
        """
        Sets the score of the player
        :param score: score
        :return: None
        """
        self.score = score


class GameOver:
    pass


class GameWon:
    pass


class GamePaused:
    pass


class GameSettings:
    pass


class GameHelp:
    pass


class GameCredits:
    pass


class GameQuit:
    pass


class GameSave:
    pass


class GameLoad:
    pass


class GameNew:
    pass


class GameExit:
    pass


class GameStart:
    pass


class GameRestart:
    pass


class GameResume:
    pass


# ---RUN PROGRAM--- #
def main():
    game = Game()


if __name__ == "__main__":
    main()  # this will initialise the program
