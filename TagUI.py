# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tag3.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import cv2
import dlib
import RPi.GPIO as GPIO
import signal
import uuid  # Random
from CentralFn import Central_Fn , SendJSON
from pirc522 import RFID
import base64
import requests
import json
from urllib.request import urlopen ,URLError
from popup2 import Dialog_Fail
from popup1 import Dialog_Success



detector = dlib.get_frontal_face_detector()


color_green = (0, 255, 0)
line_width = 1
image_height = 100
image_width = 100

facedetecting = True

unique_filename = str(uuid.uuid4())
buzzer_pin = 5
g = SendJSON()
f = Central_Fn()


final_body = dict()

cam_preview = f.OpenCam()

class Ui_Tag(object):
    def checkConnection(self):
        try:
            urlopen('http://www.google.com', timeout=1)
            return True
        except URLError as err:
            
            return False
    def dialogError(self):
        print("Tag")
        Dialog = QtWidgets.QDialog()
        ui = Dialog_Fail()
        ui.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()
    def dialogSuccess(self):
        print("Numpad")
        Dialog = QtWidgets.QDialog()
        ui = Dialog_Success()
        ui.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()
    def checkRFID(self,rfidNum):
        self.textEdit_status.clear()
        try:
            urlopen('http://www.google.com', timeout=1)
            ruid = rfidNum
            base64img = 'TEST RETURN'
            print(g.apiAddress())
            url = g.apiAddress() + '/in/check/'
            data = {'rfid_num': ruid, }
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(data), headers=headers)
            text = str(r.status_code)
            resp = json.loads(r.text)
            body = resp['body']
            # body = header['body']
            # rfid = parameter['rfid']
            # print("Status : "+text)
            # print("Body : ",body)
            final_body['rfid'] = body.get("rfid_id")
            final_body['user_id'] = body.get("user_id")
            final_body['firstname'] = body.get("first_name")
            final_body['lastname'] = body.get("last_name")
            # print("Content :",body)
            print("final_body :", final_body)
            # if(final_body['rfid'] and final_body['user_id'] and final_body['firstname'] and final_body['lastname'] ):
    
            self.textEdit_status.insertPlainText(final_body['firstname'] + ' ' + final_body['lastname'])
            if (body):
                print("final_body['rfid']", final_body['rfid'])
                print("final_body['user_id']", final_body['user_id'])


        except:
            resp = json.loads(r.text)
            if (resp['status'] == 'fail'):
                print("Data Not found")
                self.textEdit_status.insertPlainText("ไม่พบข้อมูลผู้ใช้ \nหรือไม่ได้เชื่อมต่ออินเทอร์เน็ต")
                self.dialogError()
                return 0
        self.faceDetect(final_body['rfid'], final_body['user_id'])
        
        

    def takeImg(self, RFID,uid, crop):
        print('DEF takeIMG : RFID is : ' , RFID)
        retval, buffer = cv2.imencode('.jpg', crop)
        jpg_as_text = base64.b64encode(buffer)
        a = jpg_as_text.decode('utf-8')
        imgdata = base64.b64decode(jpg_as_text)
        filename = str(uuid.uuid4())
        with open(filename, 'wb') as f:
            f.write(imgdata)
        print("UID :" ,RFID)
        print(jpg_as_text)
        res = g.sendJSON(RFID,uid,a)
        if (res == 200):
            self.textEdit_rfid.clear()
            self.dialogSuccess()

    def faceDetect(self,rfid,uid):
        # cam_preview.set(3, 320)  # set width
        # cam_preview.set(4, 180)  # set height
        print("This is faceDetect")
        print('DEF faceDetect : RFID is : ' , rfid)
        print('DEF faceDetect : UID is : ' , uid)
        if (uid != ''):
            facedetecting = True
            while facedetecting:
                print("In While Loop : ")
                ret_val, img = cam_preview.read()
                gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                dets = detector(gray_image)
                for det in dets:
                    cv2.rectangle(img, (det.left(), det.top()), (det.right(), det.bottom()), color_green, line_width)
                    crop = img[det.top():det.bottom(), det.left():det.right()]
                    print(crop)
                    if (len(crop) != 0 and crop != []):
                        print("ถ่ายรูป")
                        self.takeImg(rfid,uid,crop)
                        facedetecting = False
                # cv2.imshow('Face Detection', img)

                if cv2.waitKey(1) == 27:
                    break  # esc to quit
        cv2.destroyAllWindows()
    def clickRFID(self):
        run = True
        rdr = RFID()
        rdr.wait_for_tag()
        # util = rdr.util()
        # util.debug = True
        print("Starting")
        while run:
            self.textEdit_rfid.clear()
            rdr.wait_for_tag()
            print("แท๊กบัตรเลย")
            (error, data) = rdr.request()
            if not error:
                print("\nDetected: " + format(data, "02x"))

            (error, uid) = rdr.anticoll()
            if not error:
                hex = "{0:x}".format(uid[0]) + "," + "{0:x}".format(uid[1]) + "," + "{0:x}".format(
                    uid[2]) + "," + "{0:x}".format(uid[3])
                zero_digit = "{0:x}".format(uid[0])
                if (len(zero_digit) == 1):
                    zero_digit = "0" + zero_digit
                first_digit = "{0:x}".format(uid[1])
                if (len(first_digit) == 1):
                    first_digit = "0" + first_digit
                second_digit = "{0:x}".format(uid[2])
                if (len(second_digit) == 1):
                    second_digit = "0" + second_digit
                thrid_digit = "{0:x}".format(uid[3])
                if (len(thrid_digit) == 1):
                    thrid_digit = "0" + thrid_digit
                hex = zero_digit+first_digit+second_digit+thrid_digit
                fullUID = hex.upper()
                print ("FullUID :: " + fullUID)
                self.textEdit_rfid.insertPlainText(fullUID)
                run = False
        rdr.cleanup()
    def sendTextRFID(self):
        num = self.textEdit_rfid.toPlainText()
        print("Number ::  "+num)
        if (num != ''):
            isConnect = self.checkConnection()
            if (isConnect == True):
                self.checkRFID(num)
            elif (isConnect == False):
                self.textEdit_status.clear()
                self.textEdit_status.insertPlainText("ไม่มีการเชื่อมต่ออินเทอร์เน็ต")
                return False
            # self.faceDetect(num)
    def cancle(self,Form):
        Form.hide()
    def __init__(self):
        # cam.set(5, 30)  #set FPS
        cam_preview.set(3, 300)  # set width
        cam_preview.set(4, 300)  # set height
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start()
    def nextFrameSlot(self):
        rval, frame = cam_preview.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dets = detector(gray_image)
        for det in dets:
            cv2.rectangle(frame, (det.left(), det.top()), (det.right(), det.bottom()), color_green, line_width)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.textEdit_camera.setPixmap(pixmap)
        
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 409)
        self.labeltop = QtWidgets.QLabel(Form)
        self.labeltop.setGeometry(QtCore.QRect(530, 10, 291, 31))
        self.labeltop.setStyleSheet("font: 20pt \".SF NS Text\";")
        self.labeltop.setObjectName("labeltop")
        self.labelbuttom = QtWidgets.QLabel(Form)
        self.labelbuttom.setGeometry(QtCore.QRect(600, 270, 291, 31))
        self.labelbuttom.setStyleSheet("font: 20pt \".SF NS Text\";")
        self.labelbuttom.setObjectName("labelbuttom")
        self.textEdit_status = QtWidgets.QTextBrowser(Form)
        self.textEdit_status.setGeometry(QtCore.QRect(480, 310, 301, 91))
        self.textEdit_status.setStyleSheet("font: 18pt \".SF NS Text\";")
        self.textEdit_status.setObjectName("textEdit_status")
        self.textEdit_camera = QtWidgets.QLabel(Form)
        self.textEdit_camera.setGeometry(QtCore.QRect(480, 50, 301, 221))
        self.textEdit_camera.setObjectName("textEdit_camera")
        self.label_ = QtWidgets.QLabel(Form)
        self.label_.setGeometry(QtCore.QRect(110, 10, 291, 31))
        self.label_.setStyleSheet("font: 24pt \".SF NS Text\";")
        self.label_.setObjectName("label_")
        self.RFID = QtWidgets.QPushButton(Form)
        self.RFID.clicked.connect(self.clickRFID)
        self.RFID.setGeometry(QtCore.QRect(310, 50, 161, 51))
        self.RFID.setStyleSheet("background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:1 rgba(38, 164, 221, 255));\n"
"color: rgb(255, 255, 255);\n"
"font: 19pt \".SF NS Text\";")
        self.RFID.setObjectName("RFID")
        self.textEdit_rfid = QtWidgets.QTextEdit(Form)
        self.textEdit_rfid.setGeometry(QtCore.QRect(10, 50, 301, 51))
        self.textEdit_rfid.setStyleSheet("font: 26pt \".SF NS Text\";\n"
"")
        self.textEdit_rfid.setObjectName("textEdit_rfid")
        self.Button_Cancel = QtWidgets.QPushButton(Form)
        self.Button_Cancel.setGeometry(QtCore.QRect(20, 340, 171, 51))
        self.Button_Cancel.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(238, 83, 79, 255));\n"
"color: rgb(255, 255, 255);\n"
"font: 18pt \".SF NS Text\";")
        self.Button_Cancel.setObjectName("Button_Cancel")
        self.Button_Cancel.clicked.connect(self.cancle)
        self.Button_Done = QtWidgets.QPushButton(Form)
        self.Button_Done.setGeometry(QtCore.QRect(280, 340, 181, 51))
        self.Button_Cancel.clicked.connect(lambda :self.cancle(Form))
        self.Button_Done.setStyleSheet("background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:1 rgba(50, 142, 50, 255));\n"
"font: 20pt \".SF NS Text\";\n"
"color: rgb(255, 255, 255);\n"
"")
        self.Button_Done.setObjectName("Button_Done")
        self.Button_Done.clicked.connect(self.sendTextRFID)
        self.label_pic = QtWidgets.QLabel(Form)
        self.label_pic.setGeometry(QtCore.QRect(100, 80, 271, 271))
        self.label_pic.setText("")
        self.label_pic.setPixmap(QtGui.QPixmap("RFID.png"))
        self.label_pic.setScaledContents(True)
        self.label_pic.setObjectName("label_pic")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "ระบบประทับเวลาด้วยใบหน้า"))
        self.labeltop.setText(_translate("Form", "กรุณาปรับใบหน้าให้ตรง"))
        self.labelbuttom.setText(_translate("Form", "สถานะ"))
        self.label_.setText(_translate("Form", "ลงเวลาด้วยการแท็กบัตร"))
        self.RFID.setText(_translate("Form", "กดแล้วแท็กบัตร"))
        self.textEdit_rfid.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:36pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:13pt;\"><br /></p></body></html>"))
        self.Button_Cancel.setText(_translate("Form", "Cancel"))
        self.Button_Done.setText(_translate("Form", "Done"))

class MyApp(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_Tag()
        self.ui.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())