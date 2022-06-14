import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic


class AppSpleeter(QWidget):
    def __int__(self):
        super.__init__()
        uic.loadUi('./interface.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    appSpleeter = AppSpleeter()
    appSpleeter.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("Closing window...")
