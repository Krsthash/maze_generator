import tkinter as tk
import threading
import random
from time import sleep

# Global variables
width = 800
height = 800
cell_size = 50
grid = []


def find_the_end(end_x, end_y):
    def is_valid(p, dir):
        print(f"Pointer y: {p.y}\nPointer x: {p.x}\nDirection: {dir}\n\n")
        if dir == 0:  # UP
            if p.y != 0:
                if grid[p.y // cell_size-1][p.x // cell_size].visited:
                    return 0
                else:
                    return 1  # Can visit the cell
            else:
                return 0
        elif dir == 1:  # RIGHT
            if p.x != width-cell_size:
                if grid[p.y // cell_size][p.x // cell_size+1].visited:
                    return 0
                else:
                    return 1  # Can visit the cell
            else:
                return 0
        elif dir == 2:  # DOWN
            if p.y != height-cell_size:
                if grid[p.y // cell_size+1][p.x // cell_size].visited:
                    return 0
                else:
                    return 1  # Can visit the cell
            else:
                return 0
        elif dir == 3:  # LEFT
            if p.x != 0:
                if grid[p.y // cell_size][p.x // cell_size-1].visited:
                    return 0
                else:
                    return 1  # Can visit the cell
            else:
                return 0

    def get_choices(p):
        choices = []
        if is_valid(p, 0):
            choices.append(0)
        if is_valid(p, 1):
            choices.append(1)
        if is_valid(p, 2):
            choices.append(2)
        if is_valid(p, 3):
            choices.append(3)
        return choices

    pointer_array = []
    pointer = grid[0][0]
    pointer.visited = True
    while not (pointer.y == end_y-cell_size and pointer.x == end_x-cell_size):
        print(pointer.y, pointer.x)
        sleep(0.01)
        # Choose a random direction
        directions = get_choices(pointer)
        print(directions)
        if len(directions):
            direction = directions[random.randint(0, len(directions)-1)]

            pointer.visited = True
            pointer_array.append(pointer)
            if direction == 0:
                pointer = grid[pointer.y // cell_size-1][pointer.x // cell_size]
            elif direction == 1:
                pointer = grid[pointer.y // cell_size][pointer.x // cell_size + 1]
            elif direction == 2:
                pointer = grid[pointer.y // cell_size + 1][pointer.x // cell_size]
            elif direction == 3:
                pointer = grid[pointer.y // cell_size][pointer.x // cell_size - 1]
            pointer.visited = True
            pointer_array[-1].highlight(2)
            pointer.highlight(1)
        else:
            pointer.highlight(0)
            pointer = pointer_array[-1]
            pointer_array[-1].highlight(0)
            pointer_array.pop(-1)
            print(f"BACKTRACKED TO POINTER (y:{pointer.y}, x:{pointer.x})")
    print("FOUND THE END!!")


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = [True, True, True, True]  # Up, Right, Bottom, Left
        self.visited = False

    def draw(self):
        if self.walls[0]:
            canvas.create_line(self.x, self.y, self.x + cell_size, self.y, fill="#1e2738", width=2)
        if self.walls[1]:
            canvas.create_line(self.x + cell_size, self.y, self.x + cell_size, self.y + cell_size,
                               fill="#1e2738", width=2)
        if self.walls[2]:
            canvas.create_line(self.x + cell_size, self.y + cell_size, self.x, self.y + cell_size,
                               fill="#1e2738", width=2)
        if self.walls[3]:
            canvas.create_line(self.x, self.y + cell_size, self.x, self.y, fill="#1e2738", width=2)

    def highlight(self, switch):
        if switch == 1:  # Red highlight
            canvas.create_rectangle(self.x+1, self.y+1, self.x + cell_size - 1, self.y + cell_size - 1, fill='red', width=0)
        elif switch == 2:  # Bright highlight
            canvas.create_rectangle(self.x+1, self.y+1, self.x + cell_size - 1, self.y + cell_size - 1, fill='#9e5560', width=0)
        else:  # Remove highlight
            canvas.create_rectangle(self.x, self.y, self.x + cell_size, self.y + cell_size, fill='#8b9fc4', width=0)
            self.draw()


# Window initialization

root = tk.Tk()
root.title('Maze Generator')
root.geometry(f"{width}x{height}")
root.resizable(False, False)

# Canvas initialization
canvas = tk.Canvas(root, width=width, height=height, bg='#8b9fc4', highlightthickness=0)
canvas.pack()

# Populating the grid
for y in range(height//cell_size):
    row = []
    for x in range(width//cell_size):
        cell = Cell(x * cell_size, y * cell_size)
        row.append(cell)
        # Draw cells to the canvas
        cell.draw()
    grid.append(row)

thread = threading.Thread(target=lambda: find_the_end(height, width))
thread.start()

root.mainloop()

