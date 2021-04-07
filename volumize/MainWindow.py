# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'volumize/ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(628, 422)
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.widget_4 = QtWidgets.QWidget(self.centralwidget)
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.widget_4)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.lineEdit_inputFolder = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_inputFolder.setObjectName("lineEdit_inputFolder")
        self.gridLayout.addWidget(self.lineEdit_inputFolder, 0, 1, 1, 1)
        self.pushButton_inputFolder = QtWidgets.QPushButton(self.widget_4)
        self.pushButton_inputFolder.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/folder-plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_inputFolder.setIcon(icon)
        self.pushButton_inputFolder.setObjectName("pushButton_inputFolder")
        self.gridLayout.addWidget(self.pushButton_inputFolder, 0, 2, 1, 1)
        self.lineEdit_mangaTitle = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_mangaTitle.setObjectName("lineEdit_mangaTitle")
        self.gridLayout.addWidget(self.lineEdit_mangaTitle, 3, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.widget_4)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.lineEdit_outputFolder = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_outputFolder.setObjectName("lineEdit_outputFolder")
        self.gridLayout.addWidget(self.lineEdit_outputFolder, 1, 1, 1, 1)
        self.pushButton_outputFolder = QtWidgets.QPushButton(self.widget_4)
        self.pushButton_outputFolder.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/folder-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_outputFolder.setIcon(icon1)
        self.pushButton_outputFolder.setObjectName("pushButton_outputFolder")
        self.gridLayout.addWidget(self.pushButton_outputFolder, 1, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget_4)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.checkBox_showFiles = QtWidgets.QCheckBox(self.widget_4)
        self.checkBox_showFiles.setObjectName("checkBox_showFiles")
        self.verticalLayout_2.addWidget(self.checkBox_showFiles)
        self.horizontalLayout_3.addWidget(self.widget_4)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.doubleSpinBox_volumeNo = QtWidgets.QDoubleSpinBox(self.widget_2)
        self.doubleSpinBox_volumeNo.setMaximum(1000.0)
        self.doubleSpinBox_volumeNo.setProperty("value", 1.0)
        self.doubleSpinBox_volumeNo.setObjectName("doubleSpinBox_volumeNo")
        self.horizontalLayout_2.addWidget(self.doubleSpinBox_volumeNo)
        spacerItem2 = QtWidgets.QSpacerItem(116, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addWidget(self.widget_2)
        self.listView_chapters = QtWidgets.QListView(self.widget)
        self.listView_chapters.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listView_chapters.setObjectName("listView_chapters")
        self.verticalLayout.addWidget(self.listView_chapters)
        self.widget_3 = QtWidgets.QWidget(self.widget)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout.setContentsMargins(0, -1, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_compile = QtWidgets.QPushButton(self.widget_3)
        self.pushButton_compile.setObjectName("pushButton_compile")
        self.horizontalLayout.addWidget(self.pushButton_compile)
        self.progressBar = QtWidgets.QProgressBar(self.widget_3)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.verticalLayout.addWidget(self.widget_3)
        self.horizontalLayout_3.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Volumize"))
        self.label_3.setText(_translate("MainWindow", "Output Folder:"))
        self.lineEdit_inputFolder.setToolTip(_translate("MainWindow", "<html><head/><body><p>Full path to the folder containing manga</p></body></html>"))
        self.pushButton_inputFolder.setToolTip(_translate("MainWindow", "<html><head/><body><p>Select a folder containing the manga to archive</p></body></html>"))
        self.lineEdit_mangaTitle.setToolTip(_translate("MainWindow", "<html><head/><body><p>Manga title, used to name the CBZ archives</p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "Select Folder:"))
        self.lineEdit_outputFolder.setToolTip(_translate("MainWindow", "<html><head/><body><p>Full path to where you\'d like to store the CBZ archives</p></body></html>"))
        self.pushButton_outputFolder.setToolTip(_translate("MainWindow", "<html><head/><body><p>Select a folder to store the CBZ archives</p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "Manga Title:"))
        self.checkBox_showFiles.setToolTip(_translate("MainWindow", "<html><head/><body><p>Opens the file location after archiving</p></body></html>"))
        self.checkBox_showFiles.setText(_translate("MainWindow", "Show files in folder when complete"))
        self.label.setToolTip(_translate("MainWindow", "<html><head/><body><p>Volume number for current selection</p></body></html>"))
        self.label.setText(_translate("MainWindow", "Volume no:"))
        self.doubleSpinBox_volumeNo.setToolTip(_translate("MainWindow", "<html><head/><body><p>Volume number for current selection</p></body></html>"))
        self.pushButton_compile.setToolTip(_translate("MainWindow", "<html><head/><body><p>Archive the selected chapters</p></body></html>"))
        self.pushButton_compile.setText(_translate("MainWindow", "Compile"))
from . import resources_rc
