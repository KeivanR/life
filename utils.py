import numpy as np

def rules(cells):
    # 1+6, 3+4 -> square
    # 2+5, 0+7 -> hexagone
    ur = 1e-2
    sumcells = np.zeros((cells.shape[0]-2,cells.shape[1]-2, 3))
    sumcells += cells[2:,2:] #0
    sumcells += cells[2:,1:-1] #1
    sumcells += cells[2:,:-2] #2
    sumcells += cells[1:-1,2:] #3
    sumcells += cells[1:-1,:-2] #4
    sumcells += cells[:-2,2:] #5
    sumcells += cells[:-2,1:-1] #6
    sumcells += cells[:-2,:-2] #7



    # cells[1:-1,1:-1][sumcells<2] = 0
    # cells[1:-1,1:-1][sumcells>3] = 0
    # cells[1:-1,1:-1][sumcells==3] = 1
    cells[1:-1,1:-1,0] += ur*diff_func(sumcells[:,:,1])
    cells[1:-1,1:-1,1] += ur*gaussian(sumcells[:,:,2], 3.1,5,5,.8)
    cells[1:-1,1:-1,2] += ur*gaussian(sumcells[:,:,0], 3.2,5,5,.8)-ur*gaussian(sumcells[:,:,1], 3.2,5,5,.8)
    cells = cells.clip(0,1)

    return cells

def gaussian(x, mu,std,amp,h):
    return amp * (np.exp(-(x-mu)**2/std)+h-1)


def diff_func(x):
    mu = 3
    std = 5
    amp = 5
    h = .8
    return gaussian(x, mu,std,amp,h)