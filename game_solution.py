#has to work in python 3.8
#initial commit
from tkinter import Tk

window = Tk()
window_size = "1280x720"
window.title("Game Solution") #sets title of game
width_height = window_size.split('x') #splits geometry into width and height
window_width = int(width_height[0]) #1280
window_height = int(width_height[1]) #720
screen_width = window.winfo_screenwidth() #gets screen width
screen_height = window.winfo_screenheight() #gets screen height
position_right = int( (screen_width / 2) - (window_width / 2) ) #sets position of window to centre of screen
position_down = int( (screen_height / 2) - (window_height / 2) ) #sets position of window to centre of screen
window.geometry(f"{window_size}+{position_right}+{position_down}") #sets window size and position
window.resizable(False, False)

window.mainloop()