from PyQt5 import QtWidgets
from front.gui import AppWindow

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = AppWindow()
    ui.show()
    sys.exit(app.exec_())
