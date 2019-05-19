# encoding:utf-8
import base64
import urllib
import urllib2
import cv2
import numpy as np
from glob import glob
import json
from multiprocessing import Pool
import time

files = glob('/data2/zhousiyu/workspace/FaceAging/prepare_face_dataset/CACD2000_img/*.jpg')

for file in files:
    img = cv2.imread(file)
    img = cv2.resize(img, (448, 224))
    img = cv2.imwrite(file, img)
    print file + ": Resize Success!"