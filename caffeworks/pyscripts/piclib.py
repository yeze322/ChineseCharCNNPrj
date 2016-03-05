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

#================
def _scaleIMG(data, MAX=255):
    if data.max() < 1:
        data *= MAX/data.max()
    return data

def _toUint8IMG(data):
    return data.astype(np.uint8)

def _reshapeIMG(data):
    if data.shape[2] < data.shape[0]:
        data = data.transpose(2,0,1)
    return data


def basicHandler(pic):
    pic = _scaleIMG(pic)
    pic = _toUint8IMG(pic)
    pic = _reshapeIMG(pic)
    return pic
    
def _selectChannel(data, channels=[0,1,2]):
    return data[channels,:,:]

def _invColor(pic):
    return 255-pic

def specific_H(pic):
    pic = basicHandler(pic) #important
    pic = _selectChannel(pic, [0])
    pic = _invColor(pic)
    return pic