import numpy as np
import lmdb
import caffe
import os
import piclib
import flib
import matplotlib.pyplot as plt

# DB operations
class DB:
	def __init__(self, dbname, lead0, write=False, mapsize=99999):
		self.env = lmdb.open(dbname, readonly=not write, map_size=mapsize)
		self.txn = self.env.begin(write=write)
		self.cur = self.txn.cursor()
		self.leadformat = '{:0'+str(lead0)+'}'

		self.datum = caffe.proto.caffe_pb2.Datum()
		self.labelList = None
		self.datashape = None
		try:
			self.labelList = flib.load_obj(dbname+'/obj/labelDiction.pkl')
			print "labelDiction loaded"
			self.datashape = flib.load_obj(dbname+'/obj/picsize.pkl')
			print "datashape loaded"
			self._setDatum()
			print "Read Mode"
		except:
			print "DB's diction and data shape missing, Create Mode..."

	def __del__(self):
		self.env.close()

	def _setDatum(self):
		print self.datashape
		if len(self.datashape) == 2:
			self.datum.channels = 1
			self.datum.height, self.datum.width = self.datashape
		elif len(self.datashape) == 3:
			self.datum.channels,self.datum.height,self.datum.width = self.datashape
		else:
			raise Exception('data size error:{}'.format(self.datashape))
		return
	def _close():
		self.env.close()
		return
	def saveModify(self):
		self.txn.commit()
		return
	def count(self):
		return self.env.stat()['entries']

	def _convertString(self, raw_string):
		self.datum.ParseFromString(raw_string)
		mat = np.fromstring(self.datum.data, dtype=np.uint8)
		mat = mat.reshape(self.datum.channels, self.datum.height, self.datum.width)
		return (mat, self.datum.label)

	def getElementTupple(self, index):
		if index+1 > self.count():
			raise IndexError('index out of range')
			return None
		else:
			raw_str = self.txn.get(self.leadformat.format(index))
			return self._convertString(raw_str)

	# tuppleList : (filename, label), return shape of the data
	def addTuppleList(self, tplist, startIndex=0, autocommit = True, f=piclib.basicHandler):
		failCount = 0
		datum = None
		for fname, label in tplist:
			mat = piclib.loadPic(fname)
			mat = f(mat)
			# properties only set once
			if datum == None:
				datum = caffe.proto.caffe_pb2.Datum()
				datum.channels,datum.width,datum.height = mat.shape
			# edit db data
			datum.data = mat.tobytes()
			datum.label = label
			# insert
			key = self.leadformat.format(startIndex)
			try:
				self.txn.put(key, datum.SerializeToString())
				startIndex += 1
			except:
				failCount += 1
		# judgement of if commit
		if autocommit:
			self.saveModify()

		return mat.shape, startIndex
	def plotByIndex(self, index):
		data, label = self.getElementTupple(index)
		if data.shape[0] == 1:
			plt.imshow(data[0], cmap='gray')	
		else:
			plt.imshow(data.transpose(1,2,0))
		if self.labelList == None:
			title = str(label)
		else:
			title = str(self.labelList[label]) + '--' + str(label)
		plt.title(title)
		plt.show()
#	def addData(self, X, label, index, autocommit=False):
#		if self.datum == None:
#			self._setDatum(X)
#		
#		self.datum.data = X.tobytes()
#		self.datum.label = label
#
#		str_id = '{:08}'.format(index)
#		try:
#			self.txn.put(str_id, self.datum.SerializeToString())
#		except:
#			return False
#		if autocommit:
#			self.saveModify()
#		return True

