#! /usr/local/bin/python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qx.ui'
#
# Created: Fri Jul 11 21:26:23 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from qxConnection import Connection
from qxDataProcessing import DataProcessing
import cv2

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(663, 580)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.frameLabel = QtGui.QLabel(self.centralwidget)
        self.frameLabel.setGeometry(QtCore.QRect(10, 10, 640, 480))
        self.frameLabel.setAutoFillBackground(True)
        self.frameLabel.setText(_fromUtf8(""))
        self.frameLabel.setIndent(-1)
        self.frameLabel.setObjectName(_fromUtf8("frameLabel"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(110, 500, 223, 32))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.startVideoButton = QtGui.QPushButton(self.widget)
        self.startVideoButton.setObjectName(_fromUtf8("startVideoButton"))
        self.horizontalLayout.addWidget(self.startVideoButton)
        self.stopVideoButton = QtGui.QPushButton(self.widget)
        self.stopVideoButton.setObjectName(_fromUtf8("stopVideoButton"))
        self.horizontalLayout.addWidget(self.stopVideoButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 663, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName(_fromUtf8("menuTools"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionConfiguration = QtGui.QAction(MainWindow)
        self.actionConfiguration.setObjectName(
            _fromUtf8("actionConfiguration"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionClose)
        self.menuTools.addAction(self.actionConfiguration)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionClose, QtCore.SIGNAL(
            _fromUtf8("triggered()")), MainWindow.close)
        self.startVideoButton.clicked.connect(self.start_video)
        self.stopVideoButton.clicked.connect(self.stop_video)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self._file_grabber = cv2.VideoWriter(
            'output.avi', cv2.cv.CV_FOURCC('M','J','P','G'), 20.0, (640, 480))

        self.create_connection()
        self._timer = QtCore.QTimer(MainWindow)
        self._timer.timeout.connect(self.draw_images)
        self._timer.start(30)
        MainWindow.update()

    def start_video(self):
        self._video_flag = True

    def stop_video(self):
        self._file_grabber.release()
        self._video_flag = False

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.startVideoButton.setText(
            _translate("MainWindow", "Start Video", None))
        self.stopVideoButton.setText(
            _translate("MainWindow", "Stop Video", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit", None))
        self.menuView.setTitle(_translate("MainWindow", "View", None))
        self.menuTools.setTitle(_translate("MainWindow", "Tools", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionClose.setText(_translate("MainWindow", "Close", None))
        self.actionConfiguration.setText(
            _translate("MainWindow", "Configuration", None))

    def create_connection(self):
        try:
            print "start"
            self._connect = Connection()
            print "connected"
            ip_stream = self._connect.get_ip_stream("startLiveview")
            self._package = DataProcessing(ip_stream)
            self._video_flag = False

        except:
            return None

    def convert_frame(self, frame):
        try:
            height, width = frame.shape[:2]
            img = QtGui.QImage(
                frame, width, height, QtGui.QImage.Format_RGB888)
            img = QtGui.QPixmap.fromImage(img)
            return img

        except:
            return None

    def draw_images(self):
        opencv_img = self._package.grab_image()
        if self._video_flag == True:
            self._file_grabber(opencv_img)
        qt_img = self.convert_frame(opencv_img)
        self.frameLabel.setPixmap(qt_img)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
