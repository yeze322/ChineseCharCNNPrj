import re
import os

ftree = os.walk('./')
fontname = None
for subdir,_,fnamelist in ftree:
    if subdir == './':
        continue
    if fontname == None:
        try:
            fontname = re.match('..([a-z]+)[0-9].+', subdir).groups()[0]
        except:
            print subdir
    preffix = re.match('.+([0-9]+).+', subdir).groups()[0]
    for fname in fnamelist:
        oldName = subdir+'/'+fname
        newName = './'+fontname+'_'+preffix+'_'+fname
        os.system('cp ' + oldName + ' ' + newName)
