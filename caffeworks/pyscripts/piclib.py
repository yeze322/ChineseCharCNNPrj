import matplotlib.pyplot as plt
import matplotlib.image as pimg
import matplotlib as mlib
import numpy as np
import Image

loadPic = pimg.imread

def savePic2(fname, matrix, mode='normal'):
    if mode == 'normal':
        pimg.imsave(fname, matrix)
    elif mode == 'gray':
        pimg.imsave(fname, matrix, cmap=mlib.cm.gray)
    else:
        pass

def savePic(fname, matrix, mode=None):
    img = Image.fromarray(matrix)
    img.save(fname)
    return

def getScaleChannel(data, scale=255, channels=[0,1,2]):
    data *= scale/data.max()
    data = data.astype(np.uint8)
    if len(data.shape) == 2:
        return data
    else:
        return data[:,:,channels]

def channelToEnd(mat):
    #(3,x,y) -> (x,y,3)
    return np.rollaxis(mat, 0, 3)

def channelToHead(mat):
    #(x,y,3) -> (3,x,y)
    return np.rollaxis(mat, 2, 0)

def autoLoadPic(fname,channels=[0,1,2]):
    pic = loadPic(fname)
    scaled = getScaleChannel(pic)
    return channelToHead(scaled)
