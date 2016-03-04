import caffe

def checkParaList(srcnet, dstnet):
    srcl = srcnet.params.keys()
    dstl = dstnet.params.keys()
    cmml = [ l for l in dstl if l in srcl]
    if cmml == dstl:
        return cmml
    else:
        return None

def paraSync(srcnet, dstnet, savename='dst.caffemodel'):
    commonLayer = checkParaList(srcnet, dstnet)
    if commonLayer == None:
        raise Exception('srcnet and dstnet, parameter mismatch')
    else:
        print 'check pass, common layers={}'.format(commonLayer)
    for k in commonLayer:
        for i in range(0,2):
            dstnet.params[k][i] = srcnet.params[k][i]
    dstnet.save(savename)
    print "save net parameter success! FILE=[{}]".format(savename)
