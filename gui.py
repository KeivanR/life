import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from itertools import combinations
from utils import *

xmax = 100
ymax = 100
cell_size = 5
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

shape = np.array([
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,1,0,0,0],
    [0,0,0,1,1,1,1,0,0,1],
    [0,0,0,1,0,0,1,0,0,1],
    [0,0,0,1,1,1,1,1,1,1],
    [0,0,1,1,1,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
])

def gen_shape():
    return np.random.choice(2,(20,20))
shape1 = gen_shape()
shape2 = gen_shape()
shape3 = gen_shape()

# Add the shape at various positions
cells[xmax//2:xmax//2+shape1.shape[0],ymax//2:ymax//2+shape1.shape[1],0] = shape1
cells[xmax//3:xmax//3+shape2.shape[0],ymax//2:ymax//2+shape2.shape[1],1] = shape2
cells[xmax//3:xmax//3+shape3.shape[0],ymax//3:ymax//3+shape3.shape[1],2] = shape3
# cells[xmax//4-5:xmax//4+5,ymax//5-5:ymax//5+5] = shape
# cells[xmax//5-5:xmax//5+5,ymax//5-5:ymax//5+5] = shape

fen_princ = tk.Tk()

fen_princ.title("GAME OF LIFE")

monCanvas = tk.Canvas(fen_princ, width=xmax*cell_size, height=ymax*cell_size, bg='ivory')
monCanvas.pack()

def update_cells():
    global cells
    cells = rules(cells)

def update_canvas():
    global cells
    img =  ImageTk.PhotoImage(image=Image.fromarray((cells*255).astype(np.uint8)).resize((xmax*cell_size, ymax*cell_size), Image.NEAREST))
    monCanvas.delete("all")
    monCanvas.pack()
    monCanvas.create_image(0,0, anchor="nw", image=img)
    monCanvas.img = img  # Keep a reference to prevent garbage collection

def update():
    global cells
    update_cells()
    update_canvas()
    monCanvas.after(dt, update)

r = 6
def click_red(event):
    global cells
    y = event.x//cell_size
    x = event.y//cell_size
    cells[x-r:x+r, y-r:y+r, 0] = 1
def click_green(event):
    global cells
    y = event.x//cell_size
    x = event.y//cell_size
    cells[x-r:x+r, y-r:y+r, 1] = 1
def click_blue(event):
    global cells
    y = event.x//cell_size
    x = event.y//cell_size
    cells[x-r:x+r, y-r:y+r, 2] = 1

monCanvas.bind('<Button-1>', click_red)
monCanvas.bind('<Button-2>', click_green)
monCanvas.bind('<Button-3>', click_blue)

update()

fen_princ.mainloop()