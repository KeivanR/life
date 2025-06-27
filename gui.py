import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from itertools import combinations
from utils import *

xmax = 300
ymax = 300
cell_size = 3
dt = 15  # milliseconds

combs = list(combinations(list(range(8)),2))

cells = np.zeros((xmax, ymax))

shape = np.array([
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0],
    [0,0,1,0,0,0,1,0,0,0],
    [0,0,1,1,1,1,1,0,0,0],
    [0,0,1,1,1,1,1,0,0,0],
    [0,0,1,0,0,1,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
])

# Add the shape at various positions
cells[xmax//2-5:xmax//2+5,ymax//2-5:ymax//2+5] = shape
# cells[xmax//3-5:xmax//3+5,ymax//2-5:ymax//2+5] = shape
# cells[xmax//3-5:xmax//3+5,ymax//5-5:ymax//5+5] = shape
# cells[xmax//4-5:xmax//4+5,ymax//5-5:ymax//5+5] = shape
# cells[xmax//5-5:xmax//5+5,ymax//5-5:ymax//5+5] = shape

fen_princ = tk.Tk()

fen_princ.title("GAME OF LIFE")

monCanvas = tk.Canvas(fen_princ, width=xmax*cell_size, height=ymax*cell_size, bg='ivory')

def update_cells():
    rules(cells)

def update_canvas():
    img =  ImageTk.PhotoImage(image=Image.fromarray(cells*255).resize((xmax*cell_size, ymax*cell_size), Image.NEAREST))
    monCanvas.delete("all")
    monCanvas.pack()
    monCanvas.create_image(0,0, anchor="nw", image=img)
    monCanvas.img = img  # Keep a reference to prevent garbage collection

def update():
    update_cells()
    update_canvas()
    monCanvas.after(dt, update)

update()

fen_princ.mainloop()