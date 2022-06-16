import sys
import time

from PyQt5 import QtWidgets, QtGui, QtCore
from views.main import Ui_MainWindow
from selenium import webdriver
from model.searchThread import searchT
from model.searchThread import downMusic


class MainModel(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainModel, self).__init__()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.resultTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.resultTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.resultTable.customContextMenuRequested.connect(self.rightMenu)
        self.searchBtn.clicked.connect(lambda : self.search())
    def rightMenu(self, pos):
        row_num = -1
        for i in self.resultTable.selectionModel().selection().indexes():
            row_num = i.row()

        if row_num < 500:  # 表格生效的行数，501行点击右键，不会弹出菜单
            menu = QtWidgets.QMenu()  # 实例化菜单
            item1 = menu.addAction(u"下载")
            action = menu.exec_(self.resultTable.mapToGlobal(pos))
        else:
            return
        if action == item1:
            row = self.resultTable.selectedItems()
            id = row[0].text()
            name = row[1].text()
            singer = row[2].text()
            self.down = downMusic(id, name, singer)
            self.down._result.connect(self.resultUpdate)
            self.down.start()
    def resultUpdate(self, text):
        QtWidgets.QMessageBox.information(self, "温馨提示", text)
    def search(self):
        self.searchBtn.setEnabled(False)
        self.searchBtn.setText("搜索中...")
        self.T = searchT(self.textInput.text())
        self.T.resultDict.connect(self.updateDict)
        self.T.start()
    def updateDict(self, dict):
        self.searchBtn.setEnabled(True)
        self.searchBtn.setText("开始搜索")
        print(dict)
        self.resultTable.clearContents()
        self.resultTable.setRowCount(len(dict))
        for i in range(len(dict)):
            self.resultTable.setItem(i, 0, QtWidgets.QTableWidgetItem(dict[i]["songid"]))
            self.resultTable.setItem(i, 1, QtWidgets.QTableWidgetItem(dict[i]["songName"]))
            self.resultTable.setItem(i, 2, QtWidgets.QTableWidgetItem(dict[i]["singerName"]))
            self.resultTable.setItem(i, 3, QtWidgets.QTableWidgetItem(dict[i]["album"]))
            self.resultTable.setItem(i, 4, QtWidgets.QTableWidgetItem(dict[i]["sc"]))

    def showEvent(self, event):
        print("开启了页面")
    def closeEvent(self, event):
        sys.exit(0)