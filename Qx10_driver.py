#!/usr/bin/python
import sys
import json
import urllib2
import urllib
from pprint import pprint
import collections
import requests
import struct
import numpy as np
import cv2

params = collections.OrderedDict([
          ("method", "getAvailableApiList"),
          ("params", []),
          ("id", 1),
          ("version", "1.0")])

def int_or_str(v):
    if v.lower() == "false":
        return False
    if v.lower() == "true":
        return True
    try:
        return int(v)
    except ValueError:
        return v

if len(sys.argv) > 1:
    params["method"] = sys.argv[1]
    if len(sys.argv) > 2:
        params["params"] = [int_or_str(v) for v in sys.argv[2:]]
        print params

dic = urllib2.urlopen("http://10.0.0.1:10000/sony/camera",
    json.dumps(params)).read()

low_bound = dic.find('[')
high_bound = dic.find(']')

url = dic[low_bound+2:high_bound-1]
print url

request = urllib2.Request(url)
response = urllib2.urlopen(request)
# cv2.namedWindow('Video', 1)
terminate = False
# video  = cv2.VideoWriter('video.avi', -1, 20, (640, 480));
# if video.isOpened() == True:
  # print "ok"
while True:
  for i in xrange(5):
    # start_byte = int(response.read(1).encode('hex'), 16)
    response.read(1)
    # print "start_byte:", start_byte      
    # payload_type = int(response.read(1).encode('hex'), 16)
    response.read(1)
    # print "payload_type:", payload_type
    # sequence_num =  int(response.read(2).encode('hex'), 16)
    response.read(2)
    # print "sequence_num:", sequence_num
    # time_stamp = int(response.read(4).encode('hex'), 16)
    response.read(4)
    # print "time_stamp", time_stamp
    # start_code = int(response.read(4).encode('hex'), 16)
    response.read(4)
    # print "start_code", start_code
    jpeg_size = int(response.read(3).encode('hex'), 16)
    # print "jpeg_size", jpeg_size
    padding_size = int(response.read(1).encode('hex'), 16)
    # print "padding_size", padding_size
    # reserve = int(response.read(4).encode('hex'), 16)
    response.read(4)
    # print "reserve", reserve
    # flag = int(response.read(1).encode('hex'), 16)
    response.read(1)
    # print "flag", flag
    # reserve = int(response.read(115).encode('hex'), 16)
    response.read(115)
    # print ":reserve", reserve
    if i == 0:
      img_str = response.read(jpeg_size)
      response.read(padding_size)

      nparr = np.fromstring(img_str, np.uint8)
      img_np = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
      cv2.imshow('Video', img_np)
      # cv2.imwrite("temp.jpg", img_np)
      # x = img_np.reshape(480, 640, 3)
      # video.write(x)

      # for row in xrange(jpeg_size):
      if (cv2.waitKey(30) == 27):
        # video.release()
        terminate = True

    else:
      response.read(jpeg_size)
      response.read(padding_size)

  if terminate == True:
    break

cv2.destroyAllWindows()
