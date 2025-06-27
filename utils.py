import numpy as np
from scipy import signal

def rules(cells):
    # 1+6, 3+4 -> square
    # 2+5, 0+7 -> hexagone
    ur = 1e-2
    # sumcells = np.zeros((cells.shape[0]-2,cells.shape[1]-2, 3))
    # sumcells += cells[2:,2:] #0
    # sumcells += cells[2:,1:-1] #1
    # sumcells += cells[2:,:-2] #2
    # sumcells += cells[1:-1,2:] #3
    # sumcells += cells[1:-1,:-2] #4
    # sumcells += cells[:-2,2:] #5
    # sumcells += cells[:-2,1:-1] #6
    # sumcells += cells[:-2,:-2] #7

    filt = np.array([
        [0,0,1,1,0,0],
        [0,1,1,1,1,0],
        [1,1,0,0,1,1],
        [1,1,0,0,1,1],
        [0,1,1,1,1,0],
        [0,0,1,1,0,0],
    ])
    sumcells = np.stack([
        signal.convolve2d(cells[:,:,0], filt, boundary='symm', mode='same'),
        signal.convolve2d(cells[:,:,1], filt, boundary='symm', mode='same'),
        signal.convolve2d(cells[:,:,2], filt, boundary='symm', mode='same'),
        ],-1)



    cells[:,:,0] += ur*diff_func(sumcells[:,:,1])#-ur*gaussian(sumcells[:,:,2], mu=3,std=5,amp=5,h=.8)
    cells[:,:,1] += ur*gaussian(sumcells[:,:,2], mu=3.1,std=5,amp=5,h=.8)#-ur*gaussian(sumcells[:,:,0], mu=3.1,std=5,amp=5,h=.8)
    cells[:,:,2] += ur*gaussian(sumcells[:,:,0], mu=3.2,std=5,amp=5,h=.8)#-ur*gaussian(sumcells[:,:,1], mu=3.2,std=5,amp=5,h=.8)
    cells = cells.clip(0,1)

    return cells

def gaussian(x, mu=3,std=5,amp=5,h=.8):
    return amp * (np.exp(-(x-mu)**2/std)+h-1)


def diff_func(x):
    mu = 3
    std = 5
    amp = 5
    h = .8
    return gaussian(x, mu,std,amp,h)