# You need to have caffe installed with python support, and the BVLC reference models
# downloadad.  Please refer to the caffe website/codebase for instructions.
import caffe
import numpy as np
from matplotlib import pyplot as plt
plt.rcParams['figure.figsize'] = (10,10)

caffe_root = '/home/yeze/Documents/caffe/'  # point this to wherever you placed caffe
caffe.set_mode_gpu()
# NOTE: you must change deploy.prototxt to include "force_backward: true"
net = caffe.Net(caffe_root + 'models/bvlc_reference_caffenet/deploy.prototxt',
                caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel',
                caffe.TEST)
net.blobs['data'].reshape(1,3,227,227)
means = np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1)
#=====================================
current = np.random.rand(3,227,227)*255 - means[:,None,None]