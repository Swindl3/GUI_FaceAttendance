import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from HomeUI import Ui_Form

class MyApp(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

if 0 == 0:
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())