# Laurentiu Cristian Preda
# GAME SOLUTION
# has to work in python 3.8
# initial commit: 09-11-2023
from tkinter import Tk

# ---All functions go here---

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
