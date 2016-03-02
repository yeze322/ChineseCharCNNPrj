import numpy as np
from linecache import getlines
import re
import pickle

def save_obj(fname, obj):
    with open(fname + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(fname):
    with open(fname, 'rb') as f:
        return pickle.load(f)
'''
input: listFileName - file contains 9 fonts' child list
return: a shuffled/sorted file list collection
'''
mnist_re = r'.+_([0-9]).png'
char_re = r'.+/([a-z]+)_.+jpg'

def generateFnameLableTuppleList(inputListName, labelre, labelfunc=None, limit=-1, ifshuffle=True):
    labelDiction = {}
    flist = getlines(inputListName)
    if len(flist) == 0:
        raise Exception('flist is empty')
    if limit != -1:
        flist = flist[0:limit]

    collection = []
    labelIndex = 0

    for subfname in flist:
        label = re.match(labelre, subfname).groups()[0]

        if label not in labelDiction:
            if labelfunc == None:
                labelDiction[label] = labelIndex
                labelIndex += 1
            else:
                labelDiction[label] = labelfunc(label)

        collection.append((subfname.strip(), labelDiction[label]))

    if ifshuffle:
        np.random.shuffle(collection)
    return collection, labelDiction
