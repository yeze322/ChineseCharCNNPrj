import numpy as np
import lmdb
import caffe
import os
import piclib
import flib


# DB operations
class DB:
	def __init__(self, dbname, write=False, mapsize=99999):
		self.env = lmdb.open(dbname, readonly=not write, map_size=mapsize)
		self.txn = self.env.begin(write=write)
		self.cur = self.txn.cursor()
		
		self.datum = caffe.proto.caffe_pb2.Datum()
		try:
			self.labelDiction = flib.load_obj(dbname+'/obj/labelDiction.pkl')
			print "labelDiction loaded"
			self.datashape = flib.load_obj(dbname+'/obj/picsize.pkl')
			print "datashape loaded"
			self._setDatum()
			print "Read Mode"
		except:
			print "Create Mode..."

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
			raw_str = self.txn.get('{:08}'.format(index))
			return self._convertString(raw_str)

	# tuppleList : (filename, label), return shape of the data
	def addTuppleList(self, tplist, startIndex=0, autocommit = True, reverse=True):
		failCount = 0
		datum = None
		for fname, label in tplist:
			mat = piclib.autoLoadPic(fname)
			if reverse:
				mat = 255 - mat
			# properties only set once
			if datum == None:
				datum = caffe.proto.caffe_pb2.Datum()
				datum.channels,datum.width,datum.height = mat.shape
			# edit db data
			datum.data = mat.tobytes()
			datum.label = label
			# insert
			key = '{:08}'.format(startIndex)
			try:
				self.txn.put(key, datum.SerializeToString())
				startIndex += 1
			except:
				failCount += 1
		# judgement of if commit
		if autocommit:
			self.saveModify()

		return mat.shape, startIndex

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

