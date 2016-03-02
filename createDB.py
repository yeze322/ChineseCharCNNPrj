# command line arg parser
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="flistname", default='mnist_list')
parser.add_option('-d', '--dest', dest='dbname', default='mtest')
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

# start main function
tuppleList, labelDiction = flib.generateFnameLableTuppleList(opt.flistname, labelre=flib.mnist_re, labelfunc=int)

MAP_SIZE = 1*30*30*len(tuppleList)*20

db = dblib.DB(opt.dbname, write=True, mapsize=MAP_SIZE)

if opt.mode == 'batch':
	db.addTuppleList(tuppleList)
else:	
	for index, (picname, label) in enumerate(tuppleList):
		data = autoLoadPic(picname)
		db.addData(data, label, index)
	db.saveModify()

flib.save_obj(opt.dbname+'/labelDiction', labelDiction)