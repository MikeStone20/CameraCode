import time
from datetime import datetime
from threading import Thread, Event, RLock

from PyQt5 import QtCore, QtGui, QtWidgets
import cv2

from Camera import Camera
from Arduino import Arduino
import Constant
import FeUtils as utils
from UI import Ui_MainWindow
from camera2 import Camera_2


class CameraSys(QtWidgets.QMainWindow):
    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()

        # System internal flags
        self.isUIReady = False;
        self.isArduinoReady = False;
        self.isCameraReady = False;

        # Bring up the UI
        # If UI is not avaiable, then there is no point running this program any longer.
        try :
            
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.isUIReady = True
        except Exception as e :
            print("MAIN: " + str(e))
            print("MAIN: Unknown error when setting up UI")
            QtCore.QCoreApplication.exit(-1)
            return

        #self.ui.statusbar.showMessage("Initializing UI...") - Not needed 

        # Connecting to arduino
        # Program will carry on if no arduino is connected
        self.arduino = Arduino()
        result = -1 #self.arduino.connect()
        if  result == -1 :
            print("MAIN: Arduino not found, LED related function will be turned off")
        else :
            self.isArduinoReady = True
            self.arduino.turnOffLED()

        # Loading constants
        self.displaySize = Constant.SCREEN_DISPLAY_RES

        # Open camera
        # Program will carry on even if there is no camera detected
        self.cam = Camera(1)
        
        self.cam_2 = Camera(2)

        # Local instance of the new values
        self.cameraGain = self.cam.gain
        self.cameraHue = self.cam.hue
        self.cameraContrast = self.cam.contrast
        self.cameraFocus = self.cam.focus
        self.cameraBrightness = self.cam.brightness
        self.cameraExposure = self.cam.exposure

        self.cameraGain_2 = self.cam_2.gain
        self.cameraHue_2 = self.cam_2.hue
        self.cameraContrast_2 = self.cam_2.contrast
        self.cameraFocus_2 = self.cam_2.focus
        self.cameraBrightness_2 = self.cam_2.brightness
        self.cameraExposure_2 = self.cam_2.exposure

        # Threads
        # Camera thread control
        self.cameraThread = Thread(group = None, target = self.capture, name = "Camera System, Camera")
        self.cameraThreadKiller = Event()
        self.cameraLock = RLock()

        self.frame = None
        self.videoFrame = None
        
        #Cam 2 thread 
        self.cameraThread_2 = Thread(group = None, target = self.capture_2, name = "Camera System, Camera")
        self.cameraThreadKiller_2 = Event()
        self.cameraLock_2 = RLock()
        
        self.frame_2 = None
        self.videoFrame_2 = None

        # Flags remembering the startup initialization
        self.savePictureStartUpFlag = False
        self.startingTime = time.time()
        self.lastShotTime = time.time()

        # Control for picture saving
        self.ledOnTime = Constant.DEFAULT_LED_ON_TIME
        self.ledOffTime = Constant.DEFAULT_LED_OFF_TIME
        self.isLEDOn = False
        self.pictureSavingInterval = Constant.DEFAULT_SAVE_INTERVAL
        self.pictureSavingTimer = QtCore.QTimer(self)

        # Display thread control (unfortunately this need to be within main thread)
        self.displayUpdater = Event()
        self.displayUpdater.clear()
        self.displayTimer = QtCore.QTimer(self)
        self.startDisplay()

        self.startCameraThread_2()
        self.startCameraThread()
        self.startSavingPicture()
       

        # File dialog Configuration
        self.fileDialog = QtWidgets.QFileDialog()
        self.fileDialog.setFileMode(QtWidgets.QFileDialog.Directory)
        self.savePath = Constant.FILE_PREFIX

        # Bond interaction needs to be called at last.
        self.bondInteraction()
        #self.updateUI()

    def bondInteraction(self):
        # Bonding push buttons
        if not self.isArduinoReady :
            self.ui.pbLight.setEnabled(False)
        else :
            self.ui.pbLight.setCheckable(True)
        #self.ui.pbLight.clicked.connect(self.switchLED)
        self.ui.cameraSettings_1.clicked.connect(self.updateCameraParam)
        self.ui.cameraSettings_2.clicked.connect(self.updateCameraParam2)
        

         # Bonding line edits
       
        """self.ui.leFocus.editingFinished.connect(self.updateLineFocus)
        self.ui.leBrightness.editingFinished.connect(self.updateLineBrightness)
        self.ui.leHue.editingFinished.connect(self.updateLineHue)
        self.ui.leContrast.editingFinished.connect(self.updateLineContrast)
        self.ui.leExposure.editingFinished.connect(self.updateLineExposure)
        self.ui.leGain.editingFinished.connect(self.updateLineGain)"""

    # Update the UI with the current settings
    """def updateUI(self):
        self.ui.lFocus.setText('Focus = ' + str(self.cam.focus))
        self.ui.lBrightness.setText('Brightness = ' + str(self.cam.brightness))
        self.ui.lHue.setText('Hue = ' + str(self.cam.hue))
        self.ui.lContrast.setText('Contrast = ' + str(self.cam.contrast))
        self.ui.lExposure.setText('Exposure = ' + str(self.cam.exposure))
        self.ui.lGain.setText('Gain = ' + str(self.cam.gain))"""

    def updateCameraParam(self):
        self.cam.focus = self.cameraFocus
        self.cam.brightness = self.cameraBrightness
        self.cam.hue = self.cameraHue
        self.cam.contrast = self.cameraContrast
        self.cam.exposure = self.cameraExposure
        self.cam.gain = self.cameraGain
        self.cam.loadCameraDynParam()
        #self.updateUI()
        
    def updateCameraParam2(self):
        self.cam_2.focus = self.cameraFocus_2
        self.cam_2.brightness = self.cameraBrightness_2
        self.cam_2.hue = self.cameraHue_2
        self.cam_2.contrast = self.cameraContrast_2
        self.cam_2.exposure = self.cameraExposure_2
        self.cam_2.gain = self.cameraGain_2
        self.cam_2.loadCameraDynParam()
        #self.ui.pbClickToApply.setEnabled(True)
        #self.updateUI()
        

    # Group functions for line edits
    """def updateLineFocus(self):
        number = utils.isNumber(self.ui.leFocus.text())
        if number :
            self.cameraFocus = number
            if self.cameraFocus != self.cam.focus :
                self.ui.pbClickToApply.setEnabled(True)

    def updateLineBrightness(self):
        number = utils.isNumber(self.ui.leBrightness.text())
        if number :
            self.cameraBrightness = number
            if self.cameraBrightness != self.cam.brightness :
                self.ui.pbClickToApply.setEnabled(True)

    def updateLineHue(self):
        number = utils.isNumber(self.ui.leHue.text())
        if number :
            self.cameraHue = number
            if self.cameraHue != self.cam.hue :
                self.ui.pbClickToApply.setEnabled(True)

    def updateLineContrast(self):
        number = utils.isNumber(self.ui.leContrast.text())
        if number :
            self.cameraContrast = number
            if self.cameraContrast != self.cam.contrast :
                self.ui.pbClickToApply.setEnabled(True)

    def updateLineExposure(self):
        number = utils.isNumber(self.ui.leExposure.text())
        if number :
            self.cameraExposure = number
            if self.cameraExposure != self.cam.exposure :
                self.ui.pbClickToApply.setEnabled(True)

    def updateLineGain(self):
        number = utils.isNumber(self.ui.leGain.text())
        if number :
            self.cameraGain = number
            if self.cameraGain != self.cam.gain :
                self.ui.pbClickToApply.setEnabled(True)"""

    # Camera thread control functions:
    def startCameraThread(self):
        if not self.cameraThread.isAlive() :
            if not self.cam.isCameraOpened() :
                self.cam.openCamera()
            self.cameraThread = Thread(group = None, target = self.capture, name = "Camera System, Camera")

        try :
            self.cameraThread.start()
        except RuntimeError as e :
            print("Runtime Error: ({0}): {1}".format(e.errno, e.strerror))
            
    #Camera Thread Start for Camera 2
    def startCameraThread_2(self):
        if not self.cameraThread_2.isAlive():
            if not self.cam_2.isCameraOpened():
                self.cam_2.openCamera()
            self.cameraThread_2 = Thread(group = None, target = self.capture_2, name = "Camera System, Camera2")
        
        try:
            self.cameraThread_2.start()
        except RuntimeError as e:
            print("Runtime Error: ({0}): {1}".format(e.errno, e.strerror))
    
    
    # Stop Camera Thread
    def stopCameraThread(self):
        self.cameraThreadKiller.set()
    
    # Stop Camera Thread 2
    def stopCameraThread_2(self):
        self.cameraThreadKiller_2.set()

    # Capture thread function
    def capture(self):
        while not self.cameraThreadKiller.wait(0.001) :
            self.cameraLock.acquire()
            self.frame = self.cam.captureOnce()
            self.videoFrame = cv2.resize(self.frame, self.displaySize)
            self.cameraLock.release()
            self.displayUpdater.set()

        self.cam.release()
        self.cameraThreadKiller.clear()
        
    # Capture Thread function 2    
    def capture_2(self):
        while not self.cameraThreadKiller_2.wait(0.001):
            self.cameraLock_2.acquire()
            self.frame_2 = self.cam_2.captureOnce()
            self.videoFrame_2 = cv2.resize(self.frame_2,self.displaySize)
            self.cameraLock_2.release()
            self.displayUpdater.set()
        
        self.cam_2.release()
        self.cameraThreadKiller_2.clear()
            

    # Display control functions
    def startDisplay(self):
        if self.displayTimer.isActive() :
            self.displayTimer.stop()
        self.displayTimer.setInterval(0.001)
        self.displayTimer.setSingleShot(False)
        self.displayTimer.timeout.connect(self.display_2)
        self.displayTimer.timeout.connect(self.display)
        
        self.displayTimer.start()

    def display(self) :
        if self.displayUpdater.isSet() :
            self.cameraLock.acquire()
            self.ui.cviCamera.render(self.videoFrame)
            self.displayUpdater.clear()
            self.cameraLock.release()
            
    def display_2(self) :
        if self.displayUpdater.isSet() :
            self.cameraLock_2.acquire()
            self.ui.cviCamera_2.render(self.videoFrame_2)
            self.displayUpdater.clear()
            self.cameraLock_2.release()

    # Picture saving function
    def startSavingPicture(self) :
        if self.pictureSavingTimer.isActive() :
            self.pictureSavingTimer.stop()
        self.pictureSavingTimer.setInterval(0.5)
        self.pictureSavingTimer.setSingleShot(False)
        self.pictureSavingTimer.timeout.connect(self.savePicture)
        self.pictureSavingTimer.start()

    def savePicture(self):
        if self.displayUpdater.isSet() :
            if self.savePictureStartUpFlag :
                self.lastShotTime = time.time()
            else :
                timeNow = time.time()
                if ( timeNow - self.lastShotTime ) > self.ledOnTime and not self.isLEDOn:
                    if self.isArduinoReady :
                        self.arduino.turnOnLED()
                        self.isLEDOn = True
                elif ( timeNow - self.lastShotTime ) > self.pictureSavingInterval :
                    filename = self.savePath + '\\' + datetime.now().strftime('%m%d%yD%HH%MM') + '.png'
                    print("Saving capture to file" + filename)
                    self.cameraLock.acquire()
                    self.cameraLock_2.acquire()
                    cv2.imwrite(filename, self.frame, [cv2.IMWRITE_PNG_COMPRESSION, Constant.PNG_COMPRESSION_LEVEL])
                    cv2.imwrite(filename, self.frame_2, [cv2.IMWRITE_PNG_COMPRESSION, Constant.PNG_COMPRESSION_LEVEL])
                    self.ui.cviPhoto.render(self.videoFrame)
                    self.ui.cviPhoto_2.render(self.videoFrame_2)
                    self.cameraLock.release()
                    self.cameraLock_2.release()
                    self.lastShotTime = timeNow
                    if self.isArduinoReady :
                        self.arduino.turnOffLED()
                        self.isLEDOn = False

    def getSaveDirectory(self):
        self.fileDialog.getOpenFileName()

    def switchLED(self):
        if self.isArduinoReady :
            if self.isLEDOn :
                self.arduino.turnOffLED()
                self.ui.pbLight.setText("Turn on light")
                self.isLEDOn = False
            else :
                self.arduino.turnOnLED()
                self.ui.pbLight.setText("Turn off light")
                self.isLEDOn = True

    # Overriden close event
    def closeEvent(self, event) :
        self.stopCameraThread()
        self.stopCameraThread_2()
        if self.isArduinoReady :
            self.arduino.disconnect()
        print("Closing event accepted")
        time.sleep(1)
        event.accept()
        
    #Camera 2 Control functions

    
    
        