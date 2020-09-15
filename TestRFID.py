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
from CentralFn import Central_Fn
from pirc522 import RFID
import base64
import time



cam_preview = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()


color_green = (0, 255, 0)
line_width = 2
image_height = 100
image_width = 100

facedetecting = True

unique_filename = str(uuid.uuid4())
buzzer_pin = 5


f = Central_Fn()

cam_preview = f.OpenCam()

class Ui_Form(object):
    def takeImg(self, RFID, crop):
        print('DEF takeIMG : RFID is : ' + RFID)
        retval, buffer = cv2.imencode('.jpg', crop)
        jpg_as_text = base64.b64encode(buffer)
        a = jpg_as_text.decode('utf-8')
        imgdata = base64.b64decode(jpg_as_text)
        filename = str(uuid.uuid4())
        with open(filename, 'wb') as f:
            f.write(imgdata)
        print("UID :" + RFID)
        print(jpg_as_text)
        res = instance.sendJSON(RFID, a)
        if (res == 200):
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(buzzer_pin, GPIO.IN)
            GPIO.setup(buzzer_pin, GPIO.OUT)
            GPIO.output(buzzer_pin, True)
            time.sleep(0.3)
            GPIO.cleanup()
    def faceDetect(self, uid):
        # cam_preview.set(3, 320)  # set width
        # cam_preview.set(4, 180)  # set height
        print(uid)
        print('DEF faceDetect : RFID is : ' + uid)
        if (uid != ''):
            global facedetecting
            while facedetecting:
                print("In While Loop : ")
                ret_val, img = cam_preview.read()
                gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                dets = detector(gray_image)
                for det in dets:
                    cv2.rectangle(img, (det.left(), det.top()), (det.right(), det.bottom()), color_green, line_width)
                    crop = img[det.top():det.bottom(), det.left():det.right()]
                    print(crop)
                    if len(crop) != 0:
                        print("ถ่ายรูป")
                        self.takeImg(uid, crop)
                        facedetecting = False
                # cv2.imshow('Face Detection', img)

                if cv2.waitKey(1) == 27:
                    break  # esc to quit
        cv2.destroyAllWindows()
    def clickRFID(self):
        run = True
        rdr = RFID()
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
                # print("Card read UID: " + str(uid[0]) + "," + str(uid[1]) + "," + str(uid[2]) + "," + str(uid[3]))
                # print("Setting tag")
                # util.set_tag(uid)
                # print("\nAuthorizing")
                # # util.auth(rdr.auth_a, [0x12, 0x34, 0x56, 0x78, 0x96, 0x92])
                # util.auth(rdr.auth_b, [0x74, 0x00, 0x52, 0x35, 0x00, 0xFF])
                # print("\nReading")
                # util.read_out(4)
                # print("\nDeauthorizing")
                # util.deauth()
                fullUID = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
                print ("FullUID :: " + fullUID)
                self.textEdit_rfid.insertPlainText(fullUID)
                run = False
        rdr.cleanup()
    def sendTextRFID(self):
        num = self.textEdit_rfid.toPlainText()
        if (num != ''):
            self.faceDetect(num)
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
        self.textEdit_status = QtWidgets.QTextEdit(Form)
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
        self.textEdit_rfid.setStyleSheet("font: 36pt \".SF NS Text\";\n"
"")
        self.textEdit_rfid.setObjectName("textEdit_rfid")
        self.Button_Cancel = QtWidgets.QPushButton(Form)
        self.Button_Cancel.setGeometry(QtCore.QRect(20, 340, 171, 51))
        self.Button_Cancel.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(238, 83, 79, 255));\n"
"color: rgb(255, 255, 255);\n"
"font: 18pt \".SF NS Text\";")
        self.Button_Cancel.setObjectName("Button_Cancel")
        self.Button_Done = QtWidgets.QPushButton(Form)
        self.Button_Done.setGeometry(QtCore.QRect(280, 340, 181, 51))
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
        Form.setWindowTitle(_translate("Form", "Form"))
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
        self.ui = Ui_Form()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())
