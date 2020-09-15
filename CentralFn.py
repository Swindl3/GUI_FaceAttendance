from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import dlib
import time
import RPi.GPIO as GPIO
import signal
import uuid  # Random
import base64
import requests
import json
from pirc522 import RFID
import os
import cv2
from popup1 import Dialog_Success
# url_api = 'http://192.168.0.36:8888/in/add/'

# rdr = RFID()
# util = rdr.util()
# util.debug = True

# detector = dlib.get_frontal_face_detector()

color_green = (0, 255, 0)
line_width = 2
image_height = 100
image_width = 100

run = True
facedetecting = True

unique_filename = str(uuid.uuid4())
buzzer_pin = 5
#
def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance
class SendJSON(object):
    def apiAddress(self):
            url = "http://192.168.43.103:8888"
            return url
    def beep(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(buzzer_pin, GPIO.IN)
        GPIO.setup(buzzer_pin, GPIO.OUT)
        GPIO.output(buzzer_pin, True)
        time.sleep(0.3)
        GPIO.output(buzzer_pin, False)
        GPIO.cleanup()
    def sendJSON(self,rfid,uid, base64img):
        url = self.apiAddress()+'/in/add/'
        data = {'rfid_id':rfid,'user_id': uid, 'imgpath': base64img}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        text = str(r.status_code)
        print("Status : " + text)
        if(r.status_code == 200):
            self.beep()
            # self.dialogSuccess()
        return r.status_code
    

@singleton
class Central_Fn(object):
    cam = cv2.VideoCapture(0)
    def OpenCam(self):
        return self.cam


