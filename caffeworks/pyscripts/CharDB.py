# command line arg parser
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="flistname")#, default='mnist_list')
parser.add_option('-d', '--dbname', dest='dbname')#, default='mtest')
parser.add_option('-m', '--mode', dest='mode', default='batch')

(opt, args) = parser.parse_args()

print "flistname={}".format(opt.flistname)
print "dbname={}".format(opt.dbname)

# import libs
import sys
sys.path.append('/home/yeze/Desktop/ChineseCharPrj/caffeworks/pyscripts')
import piclib
import dblib
import flib
import numpy as np
import logging


RE = flib.RE_CH
# start main function
tuppleList, labelDiction = flib.generateFnameLableTuppleList(opt.flistname, labelre=RE)

MAP_SIZE = 1*36*36*len(tuppleList)*20

db = dblib.DB(opt.dbname, write=True, mapsize=MAP_SIZE)

if opt.mode == 'batch':
	db.addTuppleList(tuppleList)
else:	
	for index, (picname, label) in enumerate(tuppleList):
		data = piclib.autoLoadPic(picname)
		db.addData(data, label, index)
	db.saveModify()

flib.save_obj(opt.dbname+'/labelDiction', labelDiction)
