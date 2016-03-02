import caffe

srcnet = caffe.Net('test.prototxt', 'lenet_iter_5000.caffemodel', caffe.TEST)
dstnet = caffe.Net('emptytest.proto',1)

print 'net loaded: srcnet, dstnet'

keylist = srcnet.params.keys()
print keylist

def sync():
    for k in keylist:
        for i in range(0,2):
            dstnet.params[k][i] = srcnet.params[k][i]

def savePara(fname='dstpara'):
    dstnet.save(fname)
    print 'save at:' + fname

print 'func loaded: sync()'
print 'func loaded: savePara()'

#sync()
#savePara()
