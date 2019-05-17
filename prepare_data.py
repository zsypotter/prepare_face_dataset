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

files = glob('/data2/zhousiyu/dataset/CACD2000_base/*.jpg')

def run(file):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    f = open(file, 'rb')
    img = base64.b64encode(f.read())
    f.close()

    params = "{\"image\":\""+img+"\",\"image_type\":\"BASE64\",\"face_field\":\"landmark150\"}"
    
    '''use'''
    access_token = "24.6db73e2036e25a717e0ceede845bf606.2592000.1560650101.282335-16273260"
    request_url = request_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request, timeout=1)
    content = response.read()
    
    '''save txt'''
    txt_name = 'CACD2000_txt/' + file.split('.')[0].split('/')[-1] + '.txt'
    f = open(txt_name, 'w')
    f.write(content)
    f.close()
    
    '''draw'''
    content = json.loads(content.strip())
    img = cv2.imread(file)
    landmark = np.zeros(img.shape, np.uint8)
    
    '''location'''
    l_left = int(content['result']['face_list'][0]['location']['left'])
    l_top = int(content['result']['face_list'][0]['location']['top'])
    l_width = int(content['result']['face_list'][0]['location']['width'])
    l_height = int(content['result']['face_list'][0]['location']['height'])
    
    '''landmark150'''
    point_size = 1
    thickness = 0
    for item in content['result']['face_list'][0]['landmark150']:
        x = content['result']['face_list'][0]['landmark150'][item]['x']
        y = content['result']['face_list'][0]['landmark150'][item]['y']
        if (item.find('cheek') != -1) or (item.find('chin') != -1):
            point_color = (255, 0, 0)
        elif item.find('eye') != -1:
            point_color = (0, 255, 0)
        elif item.find('mouth') != -1:
            point_color = (0, 0, 255)
        elif item.find('nose') != -1:
            point_color = (255, 255, 255)

        cv2.circle(landmark, (int(x), int(y)), point_size, point_color, thickness)
        
    img_crop = img[l_top:l_top+l_height, l_left:l_left+l_width]
    landmark_crop = landmark[l_top:l_top+l_height, l_left:l_left+l_width]
    concat = cv2.hconcat((img_crop, landmark_crop))
    
    '''save img'''
    img_name = 'CACD2000_img/' + file.split('.')[0].split('/')[-1] + '.jpg'
    cv2.imwrite(img_name, concat)

total = len(files)
count = 1
for file in files:
    try:
        run(file)
    except BaseException:
        print "Error"
    else:
        print file + ': Success', str(count) + '/' + str(total)
    time.sleep(0.5)
    count += 1