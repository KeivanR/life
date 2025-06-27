import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from itertools import combinations
from utils import *

xmax = 300
ymax = 300
cell_size = 3
dt = 1  # milliseconds

combs = list(combinations(list(range(8)),2))

cells = np.zeros((xmax, ymax, 3))

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

#shape = np.stack([shape]*3, -1)

# Add the shape at various positions
cells[xmax//2-5:xmax//2+5,ymax//2-5:ymax//2+5,0] = shape
cells[xmax//3-5:xmax//3+5,ymax//2-5:ymax//2+5,1] = shape
cells[xmax//3-5:xmax//3+5,ymax//5-5:ymax//5+5,2] = shape
# cells[xmax//4-5:xmax//4+5,ymax//5-5:ymax//5+5] = shape
# cells[xmax//5-5:xmax//5+5,ymax//5-5:ymax//5+5] = shape

fen_princ = tk.Tk()

fen_princ.title("GAME OF LIFE")

monCanvas = tk.Canvas(fen_princ, width=xmax*cell_size, height=ymax*cell_size, bg='ivory')

def update_cells(cells):
    return rules(cells)

def update_canvas(cells):
    img =  ImageTk.PhotoImage(image=Image.fromarray((cells*255).astype(np.uint8)).resize((xmax*cell_size, ymax*cell_size), Image.NEAREST))
    monCanvas.delete("all")
    monCanvas.pack()
    monCanvas.create_image(0,0, anchor="nw", image=img)
    monCanvas.img = img  # Keep a reference to prevent garbage collection

def update(cells):
    cells = update_cells(cells)
    update_canvas(cells)
    monCanvas.after(dt, update, cells)

update(cells)

fen_princ.mainloop()