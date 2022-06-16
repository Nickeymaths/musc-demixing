import sys

from PyQt5.QtWidgets import QApplication
from .gui import MainWindow
from .app import Application


def main():
    app = Application()

    qapp = QApplication(sys.argv)
    gui = MainWindow(app)
    gui.show()
    sys.exit(qapp.exec_())


if __name__ == '__main__':
    main()