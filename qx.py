# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qx.ui'
#
# Created: Fri Jul 11 21:26:23 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
from qxConnection import Connection
from qxDataProcessing import DataProcessing
import cv2
import datetime

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(663, 580)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frameLabel = QtGui.QLabel(self.centralwidget)
        self.frameLabel.setGeometry(QtCore.QRect(10, 10, 640, 480))
        self.frameLabel.setAutoFillBackground(True)
        self.frameLabel.setIndent(-1)
        self.frameLabel.setObjectName("frameLabel")
        self.startButton = QtGui.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(40, 510, 114, 32))
        self.startButton.setObjectName("startButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 663, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionClose)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionClose, QtCore.SIGNAL("triggered()"), MainWindow.close)
        QtCore.QObject.connect(self.startButton, QtCore.SIGNAL("clicked()"), self.draw_images)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.create_connection()
        self._timer = QtCore.QTimer(MainWindow)
    	self._timer.timeout.connect(self.draw_images)
    	self._timer.start(100)
    	MainWindow.update()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.startButton.setText(QtGui.QApplication.translate("MainWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))

    def convertFrame(self, frame):
        try:
            height,width = frame.shape[:2]
            img = QtGui.QImage(frame, width, height, QtGui.QImage.Format_RGB888)
            img = QtGui.QPixmap.fromImage(img)
            return img
        except:
            return None

    def create_connection(self):
    	print "start"
        self._connect = Connection()
        print "connected"
        ip_stream = self._connect.get_ip_stream("startLiveview")
        self._package = DataProcessing(ip_stream)


    def draw_images(self):
        opencv_img = self._package.grab_image()
        qt_img = self.convertFrame(opencv_img)
        self.frameLabel.setPixmap(qt_img)



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
