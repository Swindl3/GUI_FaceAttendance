# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'numpad.ui'
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
import time
import RPi.GPIO as GPIO
import signal
import uuid  # Random
import base64
import requests
import json
from pirc522 import RFID
import os
from CentralFn import Central_Fn , SendJSON
from popup2 import Dialog_Fail
from popup1 import Dialog_Success
from urllib.request import urlopen ,URLError

g = SendJSON()
f = Central_Fn()

cam_preview = f.OpenCam()
detector = dlib.get_frontal_face_detector()


color_green = (0, 255, 0)
line_width = 1
image_height = 100
image_width = 100

run = True
# facedetecting = True

unique_filename = str(uuid.uuid4())
buzzer_pin = 5
#
final_body = dict()

class Ui_Numpad(object):
    def checkConnection(self):
            try:
                urlopen('http://www.google.com', timeout=1)
                return True
            except URLError as err:
                
                return False
    def dialogError(self):
        print("Numpad")
        Dialog = QtWidgets.QDialog()
        ui = Dialog_Fail()
        ui.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()
    def checkRFID(self,rfidNum):
        self.textEdit_status.clear()
        try:
                # self.textEdit_status.insertPlainText("เชื่อมต่อสำเร็จ")
                ruid = rfidNum
                base64img = 'TEST RETURN'
                url = g.apiAddress() + '/in/checkstd/'
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
                    self.textEdit_status.insertPlainText("ไม่พบข้อมูลผู้ใช้")
                    self.dialogError()
                    return 0
    
        self.faceDetect(final_body['rfid'], final_body['user_id'])

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
        self.textEdit_2.setPixmap(pixmap)

    def dialogSuccess(self):
        print("Numpad")
        Dialog = QtWidgets.QDialog()
        ui = Dialog_Success()
        ui.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()

    def takeImg(self, RFID,uid, crop):
        # pathdir = 'Image/'
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
            self.Result.clear()
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
                    if(len(dets) == 1):
                        print("ถ่ายรูป")
                        self.takeImg(rfid,uid,crop)
                        facedetecting = False
                # cv2.imshow('Face Detection', img)

                if cv2.waitKey(1) == 27:
                    break  # esc to quit
        # cv2.destroyAllWindows()


    def pressOne(self, Form):
        self.Result.insertPlainText("1")

    def pressTwo(self, Form):
        self.Result.insertPlainText("2")

    def pressThree(self, Form):
        self.Result.insertPlainText("3")

    def pressFour(self, Form):
        self.Result.insertPlainText("4")

    def pressFive(self, Form):
        self.Result.insertPlainText("5")

    def pressSix(self, Form):
        self.Result.insertPlainText("6")

    def pressSeven(self, Form):
        self.Result.insertPlainText("7")

    def pressEight(self, Form):
        self.Result.insertPlainText("8")

    def pressNine(self, Form):
        self.Result.insertPlainText("9")

    def pressZero(self, Form):
        self.Result.insertPlainText("0")

    def pressDoubleZero(self, Form):
        self.Result.insertPlainText("00")

    def pressClear(self, Form):
        self.Result.clear()

    def closeIt(self, Form):

        Form.hide()
    def pressDel(self, Form):
        fullNum = self.Result.toPlainText()
        fullNum = fullNum[:-1]
        self.Result.clear()
        self.Result.insertPlainText(fullNum)
        print(fullNum)

    def pressEnter(self, Form):
        number = self.Result.toPlainText()
        if (number == ''):
            print('เลขมันว่าง')
        elif (number != ''):
            isConnect = self.checkConnection()
            if (isConnect == True):
                self.checkRFID(number)
            elif(isConnect == False):
                self.textEdit_status.clear()
                self.textEdit_status.insertPlainText("ไม่มีการเชื่อมต่ออินเทอร์เน็ต")
                return False
                

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 409)

        ############################################# Button 1 ##############################################################
        self.Button_1 = QtWidgets.QPushButton(Form)
        self.Button_1.setGeometry(QtCore.QRect(10, 240, 91, 81))
        self.Button_1.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:1 rgba(60, 60, 60, 255));\n"
            "color: rgb(255, 255, 255);\n"
            "font: 24pt \".SF NS Text\";")
        self.Button_1.setObjectName("Button_1")
        self.Button_1.clicked.connect(self.pressOne)
        ############################################# Button 1 ##############################################################

        ############################################# Button 2 ##############################################################
        self.Button_2 = QtWidgets.QPushButton(Form)
        self.Button_2.setGeometry(QtCore.QRect(100, 240, 91, 81))
        self.Button_2.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:1 rgba(60, 60, 60, 255));\n"
            "color: rgb(255, 255, 255);\n"
            "font: 24pt \".SF NS Text\";")
        self.Button_2.setObjectName("Button_2")
        self.Button_2.clicked.connect(self.pressTwo)
        ############################################# Button 2 ##############################################################

        ############################################# Button 3 ##############################################################
        self.Button_3 = QtWidgets.QPushButton(Form)
        self.Button_3.setGeometry(QtCore.QRect(190, 240, 91, 81))
        self.Button_3.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:1 rgba(60, 60, 60, 255));\n"
            "color: rgb(255, 255, 255);\n"
            "font: 24pt \".SF NS Text\";")
        self.Button_3.setObjectName("Button_3")
        self.Button_3.clicked.connect(self.pressThree)
        ############################################# Button 3 ##############################################################

        ############################################# Button 5 ##############################################################
        self.Button_5 = QtWidgets.QPushButton(Form)
        self.Button_5.setGeometry(QtCore.QRect(100, 160, 91, 81))
        self.Button_5.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:1 rgba(60, 60, 60, 255));\n"
            "color: rgb(255, 255, 255);\n"
            "font: 24pt \".SF NS Text\";")
        self.Button_5.setObjectName("Button_5")
        self.Button_5.clicked.connect(self.pressFive)
        ############################################# Button 5 ##############################################################

        ############################################# Button 6 ##############################################################
        self.Button_6 = QtWidgets.QPushButton(Form)
        self.Button_6.setGeometry(QtCore.QRect(190, 160, 91, 81))
        self.Button_6.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:1 rgba(60, 60, 60, 255));\n"
            "color: rgb(255, 255, 255);\n"
            "font: 24pt \".SF NS Text\";")
        self.Button_6.setObjectName("Button_6")
        self.Button_6.clicked.connect(self.pressSix)

        ############################################# Button 6 ##############################################################

        ############################################# Button 4 ##############################################################
        self.Button_4 = QtWidgets.QPushButton(Form)
        self.Button_4.setGeometry(QtCore.QRect(10, 160, 91, 81))
        self.Button_4.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:1 rgba(60, 60, 60, 255));\n"
            "color: rgb(255, 255, 255);\n"
            "font: 24pt \".SF NS Text\";")
        self.Button_4.setObjectName("Button_4")
        self.Button_4.clicked.connect(self.pressFour)

        ############################################# Button 4 ##############################################################

        ############################################# Button 8 ##############################################################
        self.Button_8 = QtWidgets.QPushButton(Form)
        self.Button_8.setGeometry(QtCore.QRect(100, 80, 91, 81))
        self.Button_8.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:1 rgba(60, 60, 60, 255));\n"
            "color: rgb(255, 255, 255);\n"
            "font: 24pt \".SF NS Text\";")
        self.Button_8.setObjectName("Button_8")
        self.Button_8.clicked.connect(self.pressEight)

        ############################################# Button 8 ##############################################################

        ############################################# Button 9 ##############################################################
        self.Button_9 = QtWidgets.QPushButton(Form)
        self.Button_9.setGeometry(QtCore.QRect(190, 80, 91, 81))
        self.Button_9.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:1 rgba(60, 60, 60, 255));\n"
            "color: rgb(255, 255, 255);\n"
            "font: 24pt \".SF NS Text\";")
        self.Button_9.setObjectName("Button_9")
        self.Button_9.clicked.connect(self.pressNine)

        ############################################# Button 9 ##############################################################

        ############################################# Button 7 ##############################################################
        self.Button_7 = QtWidgets.QPushButton(Form)
        self.Button_7.setGeometry(QtCore.QRect(10, 80, 91, 81))
        self.Button_7.setAutoFillBackground(False)
        self.Button_7.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:1 rgba(60, 60, 60, 255));\n"
            "color: rgb(255, 255, 255);\n"
            "font: 24pt \".SF NS Text\";")
        self.Button_7.setAutoDefault(False)
        self.Button_7.setObjectName("Button_7")
        self.Button_7.clicked.connect(self.pressSeven)

        ############################################# Button 7 ##############################################################

        ############################################# Button 00 ##############################################################
        self.Button_00 = QtWidgets.QPushButton(Form)
        self.Button_00.setGeometry(QtCore.QRect(100, 320, 181, 81))
        self.Button_00.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:1 rgba(60, 60, 60, 255));\n"
            "color: rgb(255, 255, 255);\n"
            "font: 24pt \".SF NS Text\";")
        self.Button_00.setObjectName("Button_00")
        self.Button_00.clicked.connect(self.pressDoubleZero)

        ############################################# Button 00 ##############################################################

        ############################################# Top Result ##############################################################
        self.Result = QtWidgets.QTextEdit(Form)
        self.Result.setGeometry(QtCore.QRect(10, 10, 451, 61))
        self.Result.setPlaceholderText("กรุณากรอกรหัสนักศึกษา")
        self.Result.setStyleSheet("font: 25pt \".SF NS Text\";\n"
                                  "")
        self.Result.setObjectName("Result")
        ############################################# Top Result ##############################################################
        ############################################# Button Done ##############################################################
        self.Button_Done = QtWidgets.QPushButton(Form)
        self.Button_Done.setGeometry(QtCore.QRect(280, 320, 181, 81))
        self.Button_Done.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:1 rgba(50, 142, 50, 255));\n"
            "font: 22pt \".SF NS Text\";\n"
            "color: rgb(255, 255, 255);\n"
            "")
        self.Button_Done.setObjectName("Button_Done")
        self.Button_Done.clicked.connect(self.pressEnter)
        ############################################# Button Done ##############################################################

        ############################################# Button Cancel ##############################################################
        self.Button_Cancel = QtWidgets.QPushButton(Form)
        self.Button_Cancel.setGeometry(QtCore.QRect(280, 240, 181, 81))
        self.Button_Cancel.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(238, 83, 79, 255));\n"
            "color: rgb(255, 255, 255);\n"
            "font: 18pt \".SF NS Text\";")
        self.Button_Cancel.setObjectName("Button_Cancel")
        # self.Button_Cancel.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.Button_Cancel.clicked.connect(lambda : self.closeIt(Form))

        ############################################# Button Cancel ##############################################################

        ############################################# Button Clear ##############################################################
        self.Button_Clear = QtWidgets.QPushButton(Form)
        self.Button_Clear.setGeometry(QtCore.QRect(280, 160, 181, 81))
        self.Button_Clear.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:1 rgba(60, 60, 60, 255));\n"
            "color: rgb(255, 255, 255);\n"
            "font: 18pt \".SF NS Text\";")
        self.Button_Clear.setObjectName("Button_Clear")
        self.Button_Clear.clicked.connect(self.pressClear)

        ############################################# Button Clear ##############################################################

        ############################################# Button Del ##############################################################
        self.Button_Del = QtWidgets.QPushButton(Form)
        self.Button_Del.setGeometry(QtCore.QRect(280, 80, 181, 81))
        self.Button_Del.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:1 rgba(60, 60, 60, 255));\n"
            "color: rgb(255, 255, 255);\n"
            "font: 18pt \".SF NS Text\";")
        self.Button_Del.setObjectName("Button_Del")
        self.Button_Del.clicked.connect(self.pressDel)
        ############################################# Button Del ##############################################################

        ############################################# Button 0 ##############################################################
        self.Button_0 = QtWidgets.QPushButton(Form)
        self.Button_0.setGeometry(QtCore.QRect(10, 320, 91, 81))
        self.Button_0.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:1 rgba(60, 60, 60, 255));\n"
            "color: rgb(255, 255, 255);\n"
            "font: 24pt \".SF NS Text\";")
        self.Button_0.setObjectName("Button_0")
        self.Button_0.clicked.connect(self.pressZero)

        ############################################# Button 0 ##############################################################
        self.labeltop = QtWidgets.QLabel(Form)
        self.labeltop.setGeometry(QtCore.QRect(530, 10, 291, 31))
        self.labeltop.setStyleSheet("font: 20pt \".SF NS Text\";")
        self.labeltop.setObjectName("labeltop")

        self.textEdit_2 = QtWidgets.QLabel(Form)
        self.textEdit_2.setGeometry(QtCore.QRect(480, 50, 301, 221))
        self.textEdit_2.setObjectName("textEdit_2")

        self.labelbuttom = QtWidgets.QLabel(Form)
        self.labelbuttom.setGeometry(QtCore.QRect(600, 270, 291, 31))
        self.labelbuttom.setStyleSheet("font: 20pt \".SF NS Text\";")
        self.labelbuttom.setObjectName("labelbuttom")

        self.textEdit_status = QtWidgets.QTextBrowser(Form)
        self.textEdit_status.setGeometry(QtCore.QRect(480, 310, 301, 91))
        self.textEdit_status.setStyleSheet("font: 18pt \".SF NS Text\";")
        self.textEdit_status.setObjectName("textEdit_3")


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)



    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "ระบบประทับเวลาด้วยใบหน้า"))
        self.Button_1.setText(_translate("Form", "1"))
        self.Button_2.setText(_translate("Form", "2"))
        self.Button_3.setText(_translate("Form", "3"))
        self.Button_5.setText(_translate("Form", "5"))
        self.Button_6.setText(_translate("Form", "6"))
        self.Button_4.setText(_translate("Form", "4"))
        self.Button_8.setText(_translate("Form", "8"))
        self.Button_9.setText(_translate("Form", "9"))
        self.Button_7.setText(_translate("Form", "7"))
        self.Button_00.setText(_translate("Form", "00"))
        self.Result.setHtml(_translate("Form",
                                       "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                       "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                       "p, li { white-space: pre-wrap; }\n"
                                       "</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:36pt; font-weight:400; font-style:normal;\">\n"
                                       "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:13pt;\"><br /></p></body></html>"))
        self.Button_Done.setText(_translate("Form", "Done"))
        self.Button_Cancel.setText(_translate("Form", "Cancel"))
        self.Button_Clear.setText(_translate("Form", "Clear"))
        self.Button_Del.setText(_translate("Form", "Del"))
        self.Button_0.setText(_translate("Form", "0"))
        self.labeltop.setText(_translate("Form", "กรุณาปรับใบหน้าให้ตรง"))
        self.labelbuttom.setText(_translate("Form", "สถานะ"))
class MyApp(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_Numpad()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())

