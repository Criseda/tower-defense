# Laurentiu Cristian Preda
# GAME SOLUTION - TOWER DEFENSE GAME!
# has to work in python 3.8
# tested on python 3.8.10
# initial commit: 09-11-2023
from tkinter import Tk
from tkinter import Button as TkButton, Label as TkLabel, Menu as TkMenu, Frame as TkFrame, Canvas as TkCanvas

# ---All functions go here---


class Game:
    pass


class Enemy:
    def __init__(self, health, speed, damage, reward):
        self.health = health
        self.speed = speed
        self.damage = damage
        self.reward = reward

    def getHealth(self):
        return self.health

    def setHealth(self, health):
        self.health = health

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = speed

    def getDamage(self):
        return self.damage

    def setDamage(self, damage):
        self.damage = damage

    def getReward(self):
        return self.reward

    def setReward(self, reward):
        self.reward = reward


class Tower:
    def __init__(self, cost, size):
        self.cost = cost
        self.size = size

    def getCost(self):
        return self.cost

    def setCost(self, cost):
        self.cost = cost

    def getSize(self):
        return self.size

    def setSize(self, size):
        self.size = size


class Projectile:
    def __init__(self, damage, speed, range):
        self.damage = damage
        self.speed = speed
        self.range = range

    def getDamage(self):
        return self.damage

    def setDamage(self, damage):
        self.damage = damage

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = speed

    def getRange(self):
        return self.range

    def setRange(self, range):
        self.range = range


class Button:
    def __init__(self, text, command, x, y, width, height):
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
    def __init__(self, text, x, y, font, bg, fg, width, height):
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
        self.num_enemies = num_enemies
        self.enemy_type = enemy_type
        self.spawn_rate = spawn_rate
        self.spawn_delay = spawn_delay


class Player:
    def __init__(self):
        self.money = 0
        self.lives = 10
        self.score = 0

    def getMoney(self):
        return self.money

    def setMoney(self, money):
        self.money = money

    def getLives(self):
        return self.lives

    def setLives(self, lives):
        self.lives = lives

    def getScore(self):
        return self.score

    def setScore(self, score):
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


# ---------------------------------

window = Tk()
window.title("Game Solution")  # sets title of game


def configure_window():
    """
    Configures window size and position to centre of screen
    :return: None
    """
    window_size = "1280x720"
    # splits window_size into width and height
    width_height = window_size.split('x')
    window_width = int(width_height[0])  # 1280
    window_height = int(width_height[1])  # 720
    screen_width = window.winfo_screenwidth()  # gets screen width
    screen_height = window.winfo_screenheight()  # gets screen height
    # sets position of window to centre of screen
    position_right = int((screen_width / 2) - (window_width / 2))
    # sets position of window to centre of screen
    position_down = int((screen_height / 2) - (window_height / 2))
    # sets window size and position to centre of screen
    window.geometry(f"{window_size}+{position_right}+{position_down}")
    # prevents window from being resized
    window.resizable(False, False)


# Any code not within a function goes here
configure_window()
# ----------------------------------------
window.mainloop()
