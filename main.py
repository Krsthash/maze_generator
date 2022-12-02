import tkinter as tk

# Global variables
width = 800
height = 800
cell_size = 50
grid = []


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        canvas.create_line(self.x, self.y, self.x + cell_size, self.y, fill="#1e2738", width=2)


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
    for x in range(width//cell_size):
        print(x, y)
        cell = Cell(x * cell_size, y * cell_size)
        grid.append(cell)
        # Draw cells to the canvas
        cell.draw()

root.mainloop()

