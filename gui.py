import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

xmax = 500
ymax = 500
cell_size = 1
dt = 30  # milliseconds

cells = np.zeros((xmax, ymax))
cells[xmax//2,ymax//2] = 1

fen_princ = tk.Tk()

fen_princ.title("GAME OF LIFE")

fen_princ.geometry("600x600")

monCanvas = tk.Canvas(fen_princ, width=xmax*cell_size, height=ymax*cell_size, bg='ivory')

monCanvas.create_line(5,6,70,60, fill="orange")
monCanvas.pack()

def rules(i,j):
    if i==0 or i==xmax-1 or j==0 or j==ymax-1:
        return 0
    surround = np.zeros(8)
    surround[0:3] = cells[j-1,i-1:i+2]
    surround[3] = cells[j, i-1]
    surround[4] = cells[j, i+1]
    surround[5:8] = cells[j+1,i-1:i+2]
    s = sum(surround)
    if s<1 or s>7:
        return 0
    return 1

def fast_rules():
    sumcells = cells[2:,2:]
    sumcells += cells[2:,1:-1]
    sumcells += cells[2:,:-2]
    sumcells += cells[1:-1,2:]
    #sumcells += cells[1:-1,:-2]
    #sumcells += cells[:-2,2:]
    sumcells += cells[:-2,1:-1]
    sumcells += cells[:-2,:-2]
    cells[1:-1,1:-1][sumcells<2] = 0
    cells[1:-1,1:-1][sumcells>5] = 0
    # Set cells to 0 where the sum is between 2 and 5 (inclusive)
    mask = (sumcells >= 1) & (sumcells <= 5)
    cells[1:-1,1:-1][mask] = 1


def update_cells():
    for i in range(0, xmax):
        for j in range(0, ymax):
            cells[i,j] = rules(i,j)

def update_cells_fast():
    fast_rules()

def update_canvas():
    for i in range(0, xmax):
        for j in range(0, ymax):
            x1 = i*cell_size
            y1 = j*cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            monCanvas.create_rectangle(x1, y1, x2, y2, fill="white" if cells[i,j]==0 else "black")

def update_canvas_fast():
    img =  ImageTk.PhotoImage(image=Image.fromarray(cells*255).resize((xmax*cell_size, ymax*cell_size)))
    monCanvas.delete("all")
    monCanvas.pack()
    monCanvas.create_image(0,0, anchor="nw", image=img)
    monCanvas.img = img  # Keep a reference to prevent garbage collection

def update():
    update_cells_fast()
    update_canvas_fast()
    monCanvas.after(dt, update)

update()

fen_princ.mainloop()