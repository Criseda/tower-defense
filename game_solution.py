# Laurentiu Cristian Preda
# GAME SOLUTION - TOWER DEFENSE GAME!
# has to work in python 3.8
# tested on python 3.8.10
# initial commit: 09-11-2023
from tkinter import Tk
from tkinter import Button as TkButton, Label as TkLabel, Menu as TkMenu, Frame as TkFrame, Canvas as TkCanvas, messagebox as messagebox
import time
import threading
# ---All functions go here---


class MovingCircle:
    def __init__(self, canvas, radius=10):
        self.canvas = canvas
        self.radius = radius
        self.circle = self.canvas.create_oval(
            0, 0, radius*2, radius*2, fill='black')
        self.coordinates = []

    def read_coordinates(self, filename, cell_size):
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                # Remove parentheses and split by comma
                x, y = map(int, line.replace(
                    '(', '').replace(')', '').split(','))
                # Convert grid indices to pixel coordinates
                x *= cell_size
                y *= cell_size
                self.coordinates.append((x, y))

    def move_circle_smooth(self, steps=25):  # Reduce the number of steps
        for i in range(len(self.coordinates) - 1):
            start_x, start_y = self.coordinates[i]
            end_x, end_y = self.coordinates[i + 1]

            # Interpolate between the start and end coordinates
            for step in range(steps):
                t = step / steps
                x = start_x * (1 - t) + end_x * t
                y = start_y * (1 - t) + end_y * t

                # Move the circle to the interpolated coordinate
                self.canvas.coords(self.circle, x-self.radius,
                                   y-self.radius, x+self.radius, y+self.radius)
                self.canvas.update()
                time.sleep(0.0025)  # Reduce the delay

                # Print the current coordinates of the circle
                # print(f"Current coordinates: ({x}, {y})")
    
    def move_circle_new(self, delay=25):
        if self.coordinates:
            x, y = self.coordinates.pop(0)
            self.canvas.coords(self.circle, x-self.radius,
                               y-self.radius, x+self.radius, y+self.radius)
            self.canvas.update()
            
            #Schedule next move
            self.canvas.after(delay, self.move_circle_new, delay)
                

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
        return self.path_coordinates

    def draw_map(self):
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                color = "#8B4513" if cell == 1 else "green" # dark brown for road, green for grass
                self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                             (x + 1) * self.cell_size, (y +
                                                                        1) * self.cell_size,
                                             fill=color)

    def draw_map_from_file(self, filename):
        with open("coords.txt", "r") as file:
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
        #new stuff i dont exactly get rn
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
        map_generator = MapGenerator(self.canvas, 50, 36, cell_size=self.cell_size)
        map_generator.draw_map_from_file("coords.txt")

        self.start_circles()

        self.root.mainloop()
    
    def create_circles(self, num_circles, delay):
        for i in range(num_circles):
            circle = MovingCircle(self.canvas, self.cell_size//2)
            circle.read_coordinates('middle.txt', self.cell_size)
            self.circles.append(circle)
            self.canvas.after(i * delay, circle.move_circle_new)
    
    def start_circles(self):
        self.create_circles(num_circles=5, delay=250) # delay from circle to another

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
    game = Game()


if __name__ == "__main__":
    main()  # this will initialise the program
