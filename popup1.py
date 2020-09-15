# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'popup.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Dialog_Success(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 220)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(110, 170, 81, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.labelbuttom = QtWidgets.QLabel(Dialog)
        self.labelbuttom.setGeometry(QtCore.QRect(60, 130, 291, 31))
        self.labelbuttom.setStyleSheet("font: 25pt \".SF NS Text\";")
        self.labelbuttom.setObjectName("labelbuttom")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(90, -10, 121, 151))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Tick_Mark_Dark-512.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.labelbuttom.setText(_translate("Dialog", "ทำรายการสำเร็จ"))

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     Dialog = QtWidgets.QDialog()
#     ui = Dialog_Success()
#     ui.setupUi(Dialog)
#     Dialog.show()
#     sys.exit(app.exec_())

