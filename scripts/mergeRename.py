# run this script under fontname_(1).jpg.dir
# you can get a pakaged datalist
# named in a standard style for trainning char classfier
# python this [dstdir]

import re
import os
import sys
import progressbar as pb

OVERWRITE_MODE = True
# check ouput dir
dstdir = sys.argv[1] #input the target dir for saving pics
if not os.path.exists(dstdir):
    os.mkdir(dstdir)

# walk tree
ftree = os.walk('./')


RE_FONT = '..([a-z]+)[0-9].+'
RE_INDEX = '.+([0-9]+).+'

CONTAINL = ['ipynb', 'invalid']
ISL = ['./']

def checkdir(dname):
    if dname in ISL:
        return False
    judge = [ 1 for i in CONTAINL if i not in dname]
    return len(judge)==len(CONTAINL)

tuppleList = [\
        (subd, \
        re.match(RE_FONT, subd).groups()[0], \
        re.match(RE_INDEX, subd).groups()[0], \
        flist) \
        for subd,_,flist in ftree \
        if checkdir(subd)
        ]

bar = pb.ProgressBar(sum([len(i[3]) for i in tuppleList])).start()
BAR_COUNT = 0

# start iter
for subd, font, index, flist in tuppleList:
    for fname in flist:
        # progress bar:
        oldName = subd+'/'+fname
        newName = dstdir+'/'+font+'_'+index+'_'+fname
        if not os.path.exists(newName):
            os.system('cp ' + oldName + ' ' + newName)
        BAR_COUNT += 1
        bar.update(BAR_COUNT)


print "Finished, total=[{}]".format(BAR_COUNT)
