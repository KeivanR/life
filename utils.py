import numpy as np
from scipy import signal
from PIL import Image, ImageTk

def gaussian_filter(dimx, dimy, mu, std):
        pos = np.stack([
            np.repeat(
                np.expand_dims(np.arange(dimx),1),
                dimy,
                1
            ),
            np.repeat(
                np.expand_dims(np.arange(dimy),0),
                dimx,
                0
            ),
        ], -1)
        values = np.exp(-np.sum((pos-mu)**2,-1)/std)
        return values
    
def doughnut_filter(dimx, dimy, std):
    mu = (dimx/2, dimy/2)
    surround = gaussian_filter(dimx, dimy, mu, std)
    heart = gaussian_filter(dimx, dimy, mu, std/5)
    doughnut = surround - heart
    return doughnut/np.sum(doughnut)

filt = doughnut_filter(20,20,10)

def rules(cells):
    # 1+6, 3+4 -> square
    # 2+5, 0+7 -> hexagone
    ur = 1e-1
    # sumcells = np.zeros((cells.shape[0]-2,cells.shape[1]-2, 3))
    # sumcells += cells[2:,2:] #0
    # sumcells += cells[2:,1:-1] #1
    # sumcells += cells[2:,:-2] #2
    # sumcells += cells[1:-1,2:] #3
    # sumcells += cells[1:-1,:-2] #4
    # sumcells += cells[:-2,2:] #5
    # sumcells += cells[:-2,1:-1] #6
    # sumcells += cells[:-2,:-2] #7


    
    # img = Image.fromarray((filt/2*255).astype(np.uint8))
    # img.show()
    # input()

    sumcells = np.stack([
        signal.convolve2d(cells[:,:,0], filt, boundary='symm', mode='same'),
        signal.convolve2d(cells[:,:,1], filt, boundary='symm', mode='same'),
        signal.convolve2d(cells[:,:,2], filt, boundary='symm', mode='same'),
        ],-1)

    alpha = 10
    cells[:,:,0] += ur*gaussian(sumcells[:,:,0], mu=0.75,std=.1,amp=5,h=.7)+ur*alpha*np.maximum(0,sumcells[:,:,0]*sumcells[:,:,1]-.1)-ur*alpha*np.maximum(0,sumcells[:,:,2]-.3)
    cells[:,:,1] += ur*gaussian(sumcells[:,:,1], mu=0.75,std=.1,amp=5,h=.7)+ur*alpha*np.maximum(0,sumcells[:,:,1]*sumcells[:,:,2]-.1)-ur*alpha*np.maximum(0,sumcells[:,:,0]-.3)
    cells[:,:,2] += ur*gaussian(sumcells[:,:,2], mu=0.75,std=.1,amp=5,h=.7)+ur*alpha*np.maximum(0,sumcells[:,:,2]*sumcells[:,:,0]-.1)-ur*alpha*np.maximum(0,sumcells[:,:,1]-.3)
    cells = cells.clip(0,1)

    return cells

def gaussian(x, mu=3,std=5,amp=5,h=.8):
    return amp * (np.exp(-(x-mu)**2/std)+h-1)
