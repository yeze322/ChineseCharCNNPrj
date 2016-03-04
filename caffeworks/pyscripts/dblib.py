import numpy as np
import lmdb
import caffe
import os
import piclib
import flib

def convertStringToTupple(raw_string, dim=2, datum=None):
	if datum == None:
		datum = caffe.proto.caffe_pb2.Datum()
	datum.ParseFromString(raw_string)
	mat = np.fromstring(datum.data, dtype=np.uint8)
	if dim == 3:
		mat = mat.reshape(datum.channels, datum.height, datum.width)
	elif dim == 2:
		mat = mat.reshape(datum.height, datum.width)
	else:
		raise ValueError("Error, invalid dim")
		return (None, None)
	label = datum.label
	return (mat, label)

# DB operations
class DB:
	def __init__(self, dbname, write=False, mapsize=99999):
		self.env = lmdb.open(dbname, readonly=not write, map_size=mapsize)
		self.txn = self.env.begin(write=write)
		self.cur = self.txn.cursor()
		self.datum = caffe.proto.caffe_pb2.Datum()
		self.labelDiction = None
		if os.path.isfile(dbname+'/labelDiction.pkl'):
			self.labelDiction = flib.load_obj(dbname+'/labelDiction.pkl')

	def __del__(self):
		self.env.close()

	def close():
		self.env.close()
		return
	def saveModify(self):
		self.txn.commit()
		return
	def count(self):
		return self.env.stat()['entries']

	def getElementTupple(self, index):
		if index+1 > self.count():
			raise IndexError('index out of range')
			return None
		else:
			raw_str = self.txn.get('{:08}'.format(index))
			return convertStringToTupple(raw_str, dim=2, datum=self.datum)

	def addData(self, X, label, index, autocommit=False):
		self.datum.channels = 1
		self.datum.height = X.shape[0]
		self.datum.width = X.shape[1]
		
		self.datum.data = X.tobytes()
		self.datum.label = label

		str_id = '{:08}'.format(index)
		try:
			self.txn.put(str_id, self.datum.SerializeToString())
		except:
			return False
		if autocommit:
			self.saveModify()
		return True

	# tuppleList : (filename, label)
	def addTuppleList(self, tplist, startIndex=0, autocommit = True):
		failCount = 0
		datum = None
		for fname, label in tplist:
			mat = piclib.autoLoadPic(fname)
			# properties only set once
			if datum == None:
				datum = caffe.proto.caffe_pb2.Datum()
				datum.channels = 1
				datum.width = mat.shape[0]
				datum.height = mat.shape[1]
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

		return 'Input={}; Fail={}'.format(len(tplist), failCount)









