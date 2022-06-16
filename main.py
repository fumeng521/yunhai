import sys

from PyQt5 import QtGui, QtCore, QtWidgets
from model.mainModel import MainModel

app = QtWidgets.QApplication(sys.argv)
windowMain = MainModel()
windowMain.show()
sys.exit(app.exec_())