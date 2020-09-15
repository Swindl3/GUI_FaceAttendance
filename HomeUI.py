# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'faceattendance.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from NumpadUI import Ui_Numpad
from TagUI import Ui_Tag
import os

class Ui_Form(object):
  
    def NumpadWindow(self):
        print ("Numpad")
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Numpad()
        self.ui.setupUi(self.window)
        self.window.show()
    def TagWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Tag()
        self.ui.setupUi(self.window)
        self.window.show()
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 409)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setSizeIncrement(QtCore.QSize(10, 10))
        Form.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(180,180, 180, 255));")
        self.FillNumber = QtWidgets.QPushButton(Form)
        self.FillNumber.clicked.connect(self.NumpadWindow)
        self.FillNumber.setGeometry(QtCore.QRect(420, 140, 324, 221))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FillNumber.sizePolicy().hasHeightForWidth())
        self.FillNumber.setSizePolicy(sizePolicy)
        self.FillNumber.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily(".SF NS Text")
        font.setPointSize(40)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.FillNumber.setFont(font)
        self.FillNumber.setMouseTracking(False)
        # self.FillNumber.setTabletTracking(False)
        self.FillNumber.setToolTipDuration(0)
        self.FillNumber.setAutoFillBackground(False)
        self.FillNumber.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(20, 190, 255, 1));\n"
"font: 40pt \".SF NS Text\";\n"
"color: rgb(255, 255, 255);")
        self.FillNumber.setObjectName("FillNumber")
        self.RFID = QtWidgets.QPushButton(Form)
        self.RFID.setGeometry(QtCore.QRect(40, 140, 324, 221))
        self.RFID.clicked.connect(self.TagWindow)
        font = QtGui.QFont()
        font.setPointSize(60)
        self.RFID.setFont(font)
        self.RFID.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(56, 56, 255, 0.7));\n"
"color: rgb(255, 255, 255);")
        self.RFID.setAutoRepeatInterval(100)
        self.RFID.setObjectName("RFID")
        self.label_1 = QtWidgets.QLabel(Form)
        self.label_1.setGeometry(QtCore.QRect(140, 30, 611, 81))
        self.label_1.setStyleSheet("font: 45pt \".SF NS Text\";")
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(90, 370, 241, 41))
        self.label_2.setStyleSheet("font: 18pt \".SF NS Text\";")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(450, 370, 321, 41))
        self.label_3.setStyleSheet("font: 18pt \".SF NS Text\";")
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 0, 121, 111))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("RMUTI.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "ระบบประทับเวลาด้วยใบหน้า"))
        self.FillNumber.setText(_translate("Form", "Fill Number"))
        self.RFID.setText(_translate("Form", "RFID"))
        self.label_1.setText(_translate("Form", "ระบบประทับเวลาด้วยใบหน้า"))
        self.label_2.setText(_translate("Form", "ทำรายการด้วยการแท็กบัตร"))
        self.label_3.setText(_translate("Form", "ทำรายการด้วยการกรอกรหัสนักศึกษา"))


