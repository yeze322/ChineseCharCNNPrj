import numpy as np
import lmdb
import caffe

N = 10

# Let's pretend this is interesting data
X = np.zeros((3, 32, 32), dtype=np.uint8)

# We need to prepare the database for the size. We'll set it 10 times
# greater than what we theoretically need. There is little drawback to
# setting this too big. If you still run into problem after raising
# this, you might want to try saving fewer entries in a single
# transaction.
map_size = X.nbytes * 100

def adddd(index):
    datum = caffe.proto.caffe_pb2.Datum()
    datum.channels = X.shape[0]
    datum.height = X.shape[1]
    datum.width = X.shape[2]
    datum.data = X.tobytes()  # or .tostring() if numpy < 1.9
    datum.label = 1
    str_id = '{:08}'.format(index)
    txn.put(str_id, datum.SerializeToString())
    print env.stat()['entries']

env = lmdb.open('mylmdb', map_size=map_size)
#txn =    env.begin(write=True)
'''
with env.begin(write=True) as txn:
    # txn is a Transaction object
    for i in range(N):
        adddd(i)
        '''