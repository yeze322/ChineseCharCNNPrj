import dblib
import piclib
import flib
import re
import unittest

opsuf = 'testpic/'
class RETest(unittest.TestCase):
	def test_re_mnist(self):
		string = '/home/yeze/Desktop/ChineseCharPrj/caffeworks/data/pngs/0_7.png'
		ret = re.match(flib.RE_MNIST, string).groups()
		self.assertEqual(int(ret[0]), 7)

class PicTest(unittest.TestCase):
	def test_load10filelist(self):
		ret, dic = flib.generateFnameLableTuppleList(\
			'../data/mnist_list', labelre=flib.RE_MNIST, limit=10)
		self.assertEqual(len(ret), 10)

	def test_readDigitPic(self):
		pic = piclib.loadPic('digit.png')
		self.assertEqual(pic.shape, (28,28))
		self.assertEqual(pic.max(), 1.)

		pic_gray = piclib.getScaleChannel(pic)
		self.assertEqual(pic_gray.max(), 255)
		self.assertEqual(pic_gray.shape, (28,28))

		piclib.savePic(opsuf+'dig_norm.png', pic_gray)
		piclib.savePic(opsuf+'dig_gray.png', pic_gray, mode='gray')

	def test_readCharPic(self):
		pic = piclib.loadPic('char.jpg')
		self.assertEqual(pic.shape, (36,36,3))
		
		pic_gray = piclib.getScaleChannel(pic,channels=1)
		self.assertEqual(pic_gray.shape, (36,36))
		self.assertEqual(pic_gray.max(), 255)

		piclib.savePic(opsuf+'char_norm.png', pic_gray)
		piclib.savePic(opsuf+'char_gray.png', pic_gray, mode='gray')


class DBTest(unittest.TestCase):
	def test_o(self):
		self.assertEqual(1,1)

def runtest(classname):
    suite = unittest.TestLoader().loadTestsFromTestCase(classname)
    unittest.TextTestRunner(verbosity=2).run(suite)
	
if __name__ == '__main__':
	runtest(RETest)
	runtest(PicTest)


