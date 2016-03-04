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

def getScaleChannel(pic, scale=255, channels=[0,1,2]):
    pic *= scale/pic.max()
    pic = pic.astype(np.uint8)
    if len(pic.shape) == 2:
        return pic
    else:
        return pic[:,:,channels]

def autoLoadPic(fname,channels=[0,1,2]):
    pic = loadPic(fname)
    scaled = getScaleChannel(pic)
    return np.rollaxis(scaled, 2, 0) #(x,y,3) -> (3,x,y)
