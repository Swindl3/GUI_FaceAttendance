# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'popup2.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

class Dialog_Fail(QDialog):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 220)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(110, 170, 81, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.labelbuttom = QtWidgets.QLabel(Dialog)
        self.labelbuttom.setGeometry(QtCore.QRect(70, 130, 291, 31))
        self.labelbuttom.setStyleSheet("font: 22pt \".SF NS Text\";")
        self.labelbuttom.setObjectName("labelbuttom")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(90, 10, 121, 111))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("X.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.buttonBox.accepted.connect(Dialog.accept)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.labelbuttom.setText(_translate("Dialog", "ทำรายการไม่สำเร็จ"))

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     Dialog = QtWidgets.QDialog()
#     ui = Dialog_Fail()
#     ui.setupUi(Dialog)
#     Dialog.show()
#     sys.exit(app.exec_())


