import numpy as np
import cv2
import urllib2


class DataProcessing:

    """ process the input stream ip and grab the packages and unpack them to images """

    def __init__(self, ip_stream):
        self._trim_ip_stream = self.extract_ip_stream(ip_stream)
        # print self._trim_ip_stream
        request = urllib2.Request(self._trim_ip_stream)
        self._response = urllib2.urlopen(request)
        self._pedestrian_cascade = cv2.CascadeClassifier(
            "./hogcascade/lbpcascade_frontalface.xml.xml")

    def extract_ip_stream(self, ip_stream):
        begin_index = ip_stream.index('[')
        end_index = ip_stream.index(']')
        return ip_stream[begin_index + 2: end_index - 1]

    def unpack_package(self):
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
        cv2.cvtColor(img, cv2.cv.CV_BGR2RGB, img)
        return img

    def detect_pedestrian(self):
        img_color = self.grab_image()
        # fgbg = cv2.createBackgroundSubtractorMOG()
        # blur = cv2.GaussianBlur(img_color,(5,5),0)
        # fgmask = fgbg.apply(blur)
        # th2 = cv2.adaptiveThreshold(fgmask,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            # cv2.THRESH_BINARY,9,1)

        img_gray = cv2.cvtColor(img_color, cv2.cv.CV_RGB2GRAY)
        img_gray = cv2.equalizeHist(img_gray)
        # cv2.imshow('frame', img_gray)

        rects = self._pedestrian_cascade.detectMultiScale(1.3, 4, 0, (20, 20))
        for (x, y, w, h) in rects:
            cv2.rectangle(img_color, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.cvtColor(img_color, cv2.cv.CV_BGR2RGB, img_color)
        return img_color
