'''
Created on 2016-06-09
'''

from threading import Thread
from threading import Event
from Queue import Queue

import subprocess
import signal
import time

import zbar
import Image
import cv2

from lockObject import lockObject
from servo import servo

class qrdecode(object):
	def __init__(self):
		pass

	def decode(self,filename):
		print "decode, filename is : " + filename
		scanner = zbar.ImageScanner()
		# configure the reader
		scanner.parse_config('enable')
		# obtain image data
		pil = Image.open(filename).convert('L')
		width, height = pil.size
		raw = pil.tostring()
		# wrap image data
		image = zbar.Image(width, height, 'Y800', raw)
		# scan the image for barcodes
		scanner.scan(image)
		# extract results
		for symbol in image:
			# do something useful with results
			print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
			del(image)
			return symbol.data
		# clean up
		del(image)
		return False

def alarm_handler(signum, frame):
	raise Exception

signal.signal(signal.SIGALRM, alarm_handler)

class camera_task(Thread):
	def __init__(self, queue, index=0, device = '1', filen="./qrcode.jpeg"):
		Thread.__init__(self)
		self.filename = filen
		self.qr = qrdecode()
		self.c = ['fswebcam', '-d' ,'/dev/video' + str(device),'--save',self.filename,'-S','2']
		self.queue = queue
		self._stop = Event()
	'''
	http://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread-in-python
	'''
	def stop(self):
 		self._stop.set()

	def stopped(self):
		return self._stop.isSet()

	def run(self):
		ptimeout = 0
		while True:
			if ptimeout > 2:
				return
			ptimeout += 1
			if self.stopped():
				return
			print "----camera----"
			try:
				process = subprocess.Popen(self.c)
				process.communicate()
				print "----camera done----"
			except Exception:
				continue
			print "----qrdecode----"
			try:
				res = self.qr.decode(self.filename)
				if res != False:
					self.queue.put(res)
					return
			except Exception:
				continue
			time.sleep(2.2)

def main():
	while  True:
		queue = Queue()
		camt0 = camera_task(queue, 0, 0, 'len.jpeg')
		camt0.daemon = True
		#camt = camera_task(queue, 0, 1)
		#camt.daemon = True
		camt0.start()
		#camt.start()
		s = queue.get()
		print s
		lk = lockObject()
		sv = servo()
		ret = lk.draw_qrcode(s)
		if ret != False:
			print 'ok!!! you have picked your stuff successfully!!!!!'
			lp = subprocess.call(['sudo', './light']) # require a light execute
			time.sleep(2)
			sv.open()
			lk.remove_item(ret)
		else:
			print 'no!!! Is that the right qrcode b**ch????'
		#camt.stop()
		camt0.stop()
		raw_input()

if __name__ == '__main__':
	main()
