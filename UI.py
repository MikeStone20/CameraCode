# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'camsys.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(2400, 1800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.camPanel = QtWidgets.QWidget(self.centralwidget)
        self.camPanel.setMinimumSize(QtCore.QSize(560, 0))
        self.camPanel.setMaximumSize(QtCore.QSize(720, 700))
        self.camPanel.setObjectName("camPanel")
        
        self.camPanel = QtWidgets.QWidget(self.centralwidget)
        self.camPanel.setMinimumSize(QtCore.QSize(560, 0))
        self.camPanel.setMaximumSize(QtCore.QSize(750, 750))
        self.camPanel.setObjectName("camPanel2")
        
        self.verticalLayout =  QtWidgets.QVBoxLayout(self.camPanel)
        self.verticalLayout.setContentsMargins(0, 20, 0, 20)
        self.verticalLayout.setSpacing(27)
        self.verticalLayout.setObjectName("verticalLayout")
        
        
        self.cviCamera = CVImageWidget(self.camPanel)
        self.cviCamera.setMaximumSize(QtCore.QSize(560, 315))
        self.cviCamera.setObjectName("cviCamera")
        self.verticalLayout.addWidget(self.cviCamera)
        
        self.cviPhoto = CVImageWidget(self.camPanel)
        self.cviPhoto.setMaximumSize(QtCore.QSize(560, 315))
        self.cviPhoto.setObjectName("cviPhoto")
        self.verticalLayout.addWidget(self.cviPhoto)
        self.horizontalLayout.addWidget(self.camPanel)
        
        #Cam2
        
        self.camPanel_2 = QtWidgets.QWidget(self.centralwidget)
        self.camPanel_2.setMinimumSize(QtCore.QSize(560, 0))
        self.camPanel_2.setMaximumSize(QtCore.QSize(720, 700))
        self.camPanel_2.setObjectName("camPanel_1")
        
        self.camPanel_2 = QtWidgets.QWidget(self.centralwidget)
        self.camPanel_2.setMinimumSize(QtCore.QSize(560, 0))
        self.camPanel_2.setMaximumSize(QtCore.QSize(750, 750))
        self.camPanel_2.setObjectName("camPanel_2")
        
        self.verticalLayout_2 =  QtWidgets.QVBoxLayout(self.camPanel_2)
        self.verticalLayout_2.setContentsMargins(0, 20, 0, 20)
        self.verticalLayout_2.setSpacing(27)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        
        self.cviCamera_2 = CVImageWidget(self.camPanel_2)
        self.cviCamera_2.setMaximumSize(QtCore.QSize(560, 315))
        self.cviCamera_2.setObjectName("cviCamera_2")
        self.verticalLayout_2.addWidget(self.cviCamera_2)
        
        self.cviPhoto_2 = CVImageWidget(self.camPanel_2)
        self.cviPhoto_2.setMaximumSize(QtCore.QSize(560, 315))
        self.cviPhoto_2.setObjectName("cviPhoto_2")
        self.verticalLayout_2.addWidget(self.cviPhoto_2)
        self.horizontalLayout.addWidget(self.camPanel_2)
        
        
        self.controlPanel = QtWidgets.QWidget(self.centralwidget)
        self.controlPanel.setMaximumSize(QtCore.QSize(16777215, 700))
        self.controlPanel.setObjectName("controlPanel")
        
        self.verticalLayout = QtWidgets.QVBoxLayout(self.controlPanel)
        self.verticalLayout.setContentsMargins(205, 200, 10, 200)
        self.verticalLayout.setObjectName("verticalLayout")
        
        #self.pbLight = QtWidgets.QPushButton(self.controlPanel)
        #self.pbLight.setObjectName("pbLight")
        #self.verticalLayout_2.addWidget(self.pbLight)
        self.horizontalLayout.addWidget(self.controlPanel)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        #self.lCameraSettings.setText(_translate("MainWindow", "Camera Settings"))
        #self.pbClickToApply.setText(_translate("MainWindow", "Change Camera Setting"))
        #self.lFocus.setText(_translate("MainWindow", "Focus"))
        #self.lBrightness.setText(_translate("MainWindow", "Brightness"))
        #self.lHue.setText(_translate("MainWindow", "Hue"))
        #self.lContrast.setText(_translate("MainWindow", "Contrast"))
        #self.lExposure.setText(_translate("MainWindow", "Exposure"))
        #self.lGain.setText(_translate("MainWindow", "Gain"))
        #self.label_3.setText(_translate("MainWindow", "Save Picture to ..."))
        #self.pbBrowse.setText(_translate("MainWindow", "Browse"))
        #self.lSavingInterval.setText(_translate("MainWindow", "Saving Interval :"))
        #self.lTimeUntil.setText(_translate("MainWindow", "Time until next picture :"))
        #self.pbLight.setText(_translate("MainWindow", "Turn on light"))
        #self.pbSaveDefault.setText(_translate("MainWindow", "Save current settings as default"))
        #self.pbExit.setText(_translate("MainWindow", "Exit"))
      
        

from CVImageWidget import CVImageWidget