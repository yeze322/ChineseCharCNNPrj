import matplotlib.pyplot as plt
import caffe
import numpy as np
def pl(img):
    plt.imshow(img,cmap='gray')
    plt.show()

def sitdown(blobdata):
	bshape = blobdata[0].shape
	data = blobdata[0].transpose(1,0,2).reshape(bshape[1],bshape[0]*bshape[2])
	return data

def imgshaper(imgname):
	# 36*36*3
	img = caffe.io.load_image(imgname)
	img = img.transpose(2,0,1)
	return img[None,:]

net = caffe.Net('./cut.prototxt', './dst.caffemodel',1)
