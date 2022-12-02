import tkinter as tk

# Window initialization
WIDTH = 500
HEIGHT = 500

root = tk.Tk()
root.title('Maze Generator')
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)

# Canvas initialization
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='#8b9fc4', highlightthickness=0)
canvas.pack()

root.mainloop()

