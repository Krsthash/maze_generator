import tkinter as tk
import threading
import random
from time import sleep

# Global variables
width = 800
height = 800
cell_size = 50
grid = []


def is_valid(p, dir_):
    # print(f"Pointer y: {p.y}\nPointer x: {p.x}\nDirection: {dir}\n\n")
    if dir_ == 0:  # UP
        if p.y != 0:
            if grid[p.y // cell_size - 1][p.x // cell_size].visited:
                return 0
            else:
                return 1  # Can visit the cell
        else:
            return 0
    elif dir_ == 1:  # RIGHT
        if p.x != width - cell_size:
            if grid[p.y // cell_size][p.x // cell_size + 1].visited:
                return 0
            else:
                return 1  # Can visit the cell
        else:
            return 0
    elif dir_ == 2:  # DOWN
        if p.y != height - cell_size:
            if grid[p.y // cell_size + 1][p.x // cell_size].visited:
                return 0
            else:
                return 1  # Can visit the cell
        else:
            return 0
    elif dir_ == 3:  # LEFT
        if p.x != 0:
            if grid[p.y // cell_size][p.x // cell_size - 1].visited:
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


def find_the_end(end_x, end_y):
    def backtracked_walls(p, last_p):
        p_y = p.y // cell_size
        p_x = p.x // cell_size
        last_p_y = last_p.y // cell_size
        last_p_x = last_p.x // cell_size
        if p_y == last_p_y+1 and p_x == last_p_x:  # Direction 1: (Backtracked from top, set back top border)
            return [True, p.walls[1], p.walls[2], p.walls[3]]
        elif p_y == last_p_y and p_x == last_p_x-1:  # Direction 2: (Backtracked from right, set back right border)
            return [p.walls[0], True, p.walls[2], p.walls[3]]
        elif p_y == last_p_y-1 and p_x == last_p_x:  # Direction 3: (Backtracked from bottom, set back bottom border)
            return [p.walls[0], p.walls[1], True, p.walls[3]]
        elif p_y == last_p_y and p_x == last_p_x+1:  # Direction 4: (Backtracked from left, set back left border)
            return [p.walls[0], p.walls[1], p.walls[2], True]

    pointer_array = []
    pointer = grid[0][0]
    pointer.visited = True
    while not (pointer.y == end_y-cell_size and pointer.x == end_x-cell_size):
        # print(pointer.y, pointer.x)
        sleep(0.01)
        # Choose a random direction
        directions = get_choices(pointer)
        if len(directions):
            direction = directions[random.randint(0, len(directions)-1)]

            pointer.visited = True
            pointer_array.append(pointer)
            if direction == 0:
                pointer = grid[pointer.y // cell_size-1][pointer.x // cell_size]
                pointer.walls = [pointer.walls[0], pointer.walls[1], False, pointer.walls[3]]
                pointer.draw()
                pointer_array[-1].walls = [False, pointer_array[-1].walls[1], pointer_array[-1].walls[2], pointer_array[-1].walls[3]]
                pointer_array[-1].draw()
            elif direction == 1:
                pointer = grid[pointer.y // cell_size][pointer.x // cell_size + 1]
                pointer.walls = [pointer.walls[0], pointer.walls[1], pointer.walls[2], False]
                pointer.draw()
                pointer_array[-1].walls = [pointer_array[-1].walls[0], False, pointer_array[-1].walls[2], pointer_array[-1].walls[3]]
                pointer_array[-1].draw()
            elif direction == 2:
                pointer = grid[pointer.y // cell_size + 1][pointer.x // cell_size]
                pointer.walls = [False, pointer.walls[1], pointer.walls[2], pointer.walls[3]]
                pointer.draw()
                pointer_array[-1].walls = [pointer_array[-1].walls[0], pointer_array[-1].walls[1], False, pointer_array[-1].walls[3]]
                pointer_array[-1].draw()
            elif direction == 3:
                pointer = grid[pointer.y // cell_size][pointer.x // cell_size - 1]
                pointer.walls = [pointer.walls[0], False, pointer.walls[2], pointer.walls[3]]
                pointer.draw()
                pointer_array[-1].walls = [pointer_array[-1].walls[0], pointer_array[-1].walls[1], pointer_array[-1].walls[2], False]
                pointer_array[-1].draw()
            pointer.visited = True
            # pointer_array[-1].highlight(2)
            # pointer.highlight(1)
        else:
            pointer.highlight(0)
            pointer.walls = [True, True, True, True]
            pointer.draw()
            l_pointer = pointer
            pointer = pointer_array[-1]
            pointer.walls = backtracked_walls(pointer, l_pointer)
            pointer.draw()
            # The problem is that the cell that it backtracks to will have its wall to the impossible cell already
            # set to invisible. Need a way to detect which direction the invisible square is from the cell and draw
            # back the wall.
            pointer_array[-1].highlight(0)
            pointer_array.pop(-1)
    print("FOUND THE END!!")
    return pointer_array


def create_distractions(p_array):
    n_cells_to_populate = (width//cell_size) * (height//cell_size)
    for y in range(height//cell_size):
        for x in range(width//cell_size):
            grid[y][x].visited = False
            if grid[y][x] in p_array:
                n_cells_to_populate -= 1
                grid[y][x].visited = True
    print(n_cells_to_populate)
    for path_cell in p_array:
        d_array = []
        pointer = path_cell
        while True:
            choices = get_choices(pointer)
            print(choices, pointer.y//cell_size, pointer.x//cell_size)
            if len(choices):
                direction = choices[random.randint(0, len(choices)-1)]

                pointer.visited = True
                d_array.append(pointer)
                n_cells_to_populate -= 1

                if direction == 0:
                    pointer = grid[pointer.y // cell_size - 1][pointer.x // cell_size]
                    pointer.walls = [pointer.walls[0], pointer.walls[1], False, pointer.walls[3]]
                    pointer.draw()
                    d_array[-1].walls = [False, d_array[-1].walls[1], d_array[-1].walls[2], d_array[-1].walls[3]]
                    d_array[-1].draw()
                elif direction == 1:
                    pointer = grid[pointer.y // cell_size][pointer.x // cell_size + 1]
                    pointer.walls = [pointer.walls[0], pointer.walls[1], pointer.walls[2], False]
                    pointer.draw()
                    d_array[-1].walls = [d_array[-1].walls[0], False, d_array[-1].walls[2], d_array[-1].walls[3]]
                    d_array[-1].draw()
                elif direction == 2:
                    pointer = grid[pointer.y // cell_size + 1][pointer.x // cell_size]
                    pointer.walls = [False, pointer.walls[1], pointer.walls[2], pointer.walls[3]]
                    pointer.draw()
                    d_array[-1].walls = [d_array[-1].walls[0], d_array[-1].walls[1], False, d_array[-1].walls[3]]
                    d_array[-1].draw()
                elif direction == 3:
                    pointer = grid[pointer.y // cell_size][pointer.x // cell_size - 1]
                    pointer.walls = [pointer.walls[0], False, pointer.walls[2], pointer.walls[3]]
                    pointer.draw()
                    d_array[-1].walls = [d_array[-1].walls[0], d_array[-1].walls[1], d_array[-1].walls[2], False]
                    d_array[-1].draw()
                pointer.visited = True
            else:
                if pointer == path_cell:
                    break
                else:
                    pointer = d_array[-1]
                    d_array.pop(-1)
    print(n_cells_to_populate)


def generate_maze():
    print("Generating the maze...")
    arr = find_the_end(height, width)
    create_distractions(arr)


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = [True, True, True, True]  # Up, Right, Bottom, Left
        self.visited = False

    def draw(self):
        if self.walls[0]:
            canvas.create_line(self.x, self.y, self.x + cell_size, self.y, fill="#1e2738", width=2)
        else:
            canvas.create_line(self.x, self.y, self.x + cell_size, self.y, fill="#8b9fc4", width=2)
        if self.walls[1]:
            canvas.create_line(self.x + cell_size, self.y, self.x + cell_size, self.y + cell_size,
                               fill="#1e2738", width=2)
        else:
            canvas.create_line(self.x + cell_size, self.y, self.x + cell_size, self.y + cell_size,
                               fill="#8b9fc4", width=2)
        if self.walls[2]:
            canvas.create_line(self.x + cell_size, self.y + cell_size, self.x, self.y + cell_size,
                               fill="#1e2738", width=2)
        else:
            canvas.create_line(self.x + cell_size, self.y + cell_size, self.x, self.y + cell_size,
                               fill="#8b9fc4", width=2)
        if self.walls[3]:
            canvas.create_line(self.x, self.y + cell_size, self.x, self.y, fill="#1e2738", width=2)
        else:
            canvas.create_line(self.x, self.y + cell_size, self.x, self.y, fill="#8b9fc4", width=2)

    def highlight(self, switch):
        if switch == 1:  # Red highlight
            canvas.create_rectangle(self.x+1, self.y+1, self.x + cell_size - 1, self.y + cell_size - 1,
                                    fill='red', width=0)
        elif switch == 2:  # Bright highlight
            canvas.create_rectangle(self.x+1, self.y+1, self.x + cell_size - 1, self.y + cell_size - 1,
                                    fill='#9e5560', width=0)
        else:  # Remove highlight
            canvas.create_rectangle(self.x+1, self.y+1, self.x + cell_size - 1, self.y + cell_size - 1,
                                    fill='#8b9fc4', width=0)
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
for i in range(height//cell_size):
    row = []
    for j in range(width//cell_size):
        cell = Cell(j * cell_size, i * cell_size)
        row.append(cell)
        # Draw cells to the canvas
        cell.draw()
    grid.append(row)

thread = threading.Thread(target=generate_maze)
thread.start()

root.mainloop()

