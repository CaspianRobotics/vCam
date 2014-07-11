import numpy as np
import cv2
import urllib2

class DataProcessing:
	""" process the input stream ip and grab the packages and unpack them to images """

	def __init__ (self, ip_stream):
		self._trim_ip_stream = self.extract_ip_stream(ip_stream)
		# print self._trim_ip_stream
		request = urllib2.Request(self._trim_ip_stream)
		self._response = urllib2.urlopen(request)

	def extract_ip_stream(self, ip_stream):
		begin_index = ip_stream.index('[')
		end_index = ip_stream.index(']')
		return ip_stream[begin_index + 2: end_index -1]

	def unpack_package (self):
		self._response.read(1)
		self._response.read(1)
		self._response.read(2)
		self._response.read(4)
		self._response.read(4)
		jpeg_size = int(self._response.read(3).encode('hex'), 16)
		padding_size = int(self._response.read(1).encode('hex'), 16)
		self._response.read(4)
		self._response.read(1)
		self._response.read(115)
		img_str = self._response.read(jpeg_size)
		self._response.read(padding_size)
		return img_str

	def grab_image(self):
		img_str = self.unpack_package()
		nparr = np.fromstring(img_str, np.uint8)
		img = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
		return img 
