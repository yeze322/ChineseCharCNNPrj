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

def getGrayChannel(pic, scale=255, channel=0):
    pic *= scale/pic.max()
    pic = pic.astype(np.uint8)
    if len(pic.shape) == 2:
        return pic
    else:
        return pic[:,:,channel]

def autoLoadPic(fname):
    pic = loadPic(fname)
    return getGrayChannel(pic)