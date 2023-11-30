import sys
from PyQt5.QtWidgets import QMainWindow, QSizePolicy,\
                        QMessageBox, QPushButton, \
                        QApplication, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, pyqtSignal
from ui_main import Ui_MainWindow
from ui_invisible_window import Ui_MainWindow as Ui_InvisibleWindow
from portWindow import Ui_MainWindow as Ui_PortWindow
from supportedATMs import Ui_MainWindow as Ui_SupportedATMWindow
from settingsWindow import Ui_MainWindow as Ui_SettingsWindow
import ctypes

myappid = 'tahiralauddin.gsm-rs232-bank.1.0.0' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


from PyQt5.QtCore import QEvent, QObject

class ClickEventFilter(QObject):
    def eventFilter(self, watched, event):
        # If it's a mouse click event, ignore it.
        if event.type() == QEvent.MouseButtonPress:
            return True
        return False


class Main(QMainWindow):

    GSMSignal = pyqtSignal()
    ATMSignal = pyqtSignal()
    TowerSignal = pyqtSignal()
    scannableSignal = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Set window title

        # Set window geometry
        self.setGeometry(100, 100, 500, 300)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowIcon(QIcon("images/logo.jpg"))

        self.Ui_components()
        # Signals
        self.GSMSignal.connect(self.connectStatus)
        self.ATMSignal.connect(self.addWeakSignals)
        self.TowerSignal.connect(self.addStrongSignals)
        self.scannableSignal.connect(self.readyForScan)

        # Default values
        self.connectedToGSM = False
        self.connectedToATM = False
        self.connectedToTower = False
        self.scannable = False
        self.atmName = "TD Bank"
        self.info = open('info.html').read()

        # In your main window or widget class, create an instance of the event filter
        self.clickEventFilter = ClickEventFilter()

    def Ui_components(self):
        # Close software window
        self.ui.exitBtn.clicked.connect(self.close)

        self.ui.startBtn.clicked.connect(lambda: self.restartProgressBar(callback=self.scannableSignal))
        self.ui.invisibleBtn.clicked.connect(self.openInvisibleWindow)
        self.ui.connectPCToGSMBtn.clicked.connect(self.connectToGSM)
        self.ui.connectGSMToATMBtn.clicked.connect(self.connectToATM)
        self.ui.connectToTowerBtn.clicked.connect(self.connectToTower)
        self.ui.disconnectAllBtn.clicked.connect(self.disconnectAll)
        self.ui.portBtn.clicked.connect(self.openPortWindow)
        self.ui.settingsBtn.clicked.connect(self.openSettingsWindow)
        self.ui.supportedBtn.clicked.connect(self.openSupportedATMsWindow)
        self.ui.fileLocationBtn.clicked.connect(self.openFileLocation)
        self.ui.downloadPacketsBtn.clicked.connect(self.openDownloadPackets)
        self.ui.scanBtn.clicked.connect(self.showInformation)

        # self.ui.portBtn.clicked.connect()
        self.ui.progressBar.setValue(0)
    
    def openFileLocation(self):
        self.showPopup(message=r"File Location C:\Users\MyPC\Documents\GSM Software")

    def openDownloadPackets(self):
        self.showPopup(message=r"Saved to C:\Users\MyPC\Documents\GSM Software\Recieved")
    
    def readyForScan(self):
        self.scannable = True
        self.showPopup(message="Ready! Select 'Scan'")

    def showPopup(self, title='GSM RS232 BANK SOFTWARE', message="Data imported successfully!", **kwargs):
        if kwargs.get('progress'):
            self.restartProgressBar()

        QMessageBox.information(self, title, message)
        if kwargs.get('connected'):
            pass

    def restartProgressBar(self, **kwargs):
        from threading import Thread
        Thread(target=self.runProgressBar, kwargs=kwargs).start()

    # def runProgressBar(self, **kwargs):
    #     import time
    #     for i in range(100):
    #         time.sleep(0.0)
    #         self.ui.progressBar.setValue(i+1)


    # Then in your runProgressBar method:
    def runProgressBar(self, **kwargs):
        import time
        # # Install event filter on all buttons
        # for button in self.findChildren(QPushButton):
        #     print(button)
        #     button.installEventFilter(self.clickEventFilter)
        
        # Run your progress loop
        for i in range(100):
            time.sleep(0.05)  # It's good practice to have a small delay
            self.ui.progressBar.setValue(i + 1)
        
        # # Remove event filter from all buttons
        # for button in self.findChildren(QPushButton):
        #     button.removeEventFilter(self.clickEventFilter)

        # If there is a keyword argument with key as 'callback'
        # Get it's value, which is going to be a Signal
        # Emit the singal
        if value:=kwargs.get('callback'):
            value.emit()

    def addWeakSignals(self):
        self.pushButton_14 = QPushButton(self.ui.frame_6)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_14.sizePolicy().hasHeightForWidth())
        self.pushButton_14.setSizePolicy(sizePolicy)
        self.pushButton_14.setStyleSheet("background: transparent;")
        self.pushButton_14.setText("")
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(".\\images/weak-signal.png"), QIcon.Normal, QIcon.Off)
        self.pushButton_14.setIcon(icon1)
        self.pushButton_14.setIconSize(QSize(25, 25))
        self.pushButton_14.setObjectName("pushButton_14")
        self.ui.horizontalLayout_7.addWidget(self.pushButton_14)

        # Success message
        QMessageBox.information(self, 'Success Message', 'GSM connected to ATM Successfully!')
        

    def addStrongSignals(self):
        self.bankATMLabel = QLabel(self.ui.frame_7)
        self.bankATMLabel.setStyleSheet("color: lightgrey;\n"
"font-family: \'Roboto\', sans-serif; /* A modern, friendly sans-serif font */\n"
"font-size: 15px;")
        self.bankATMLabel.setObjectName("bankATMLabel")
        self.ui.horizontalLayout_5.addWidget(self.bankATMLabel)
        
        self.pushButton_13 = QPushButton(self.ui.frame_7)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_13.sizePolicy().hasHeightForWidth())
        self.pushButton_13.setSizePolicy(sizePolicy)
        self.pushButton_13.setStyleSheet("background: transparent;")
        self.pushButton_13.setText("")
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(".\\images/strong-signal.png"), QIcon.Normal, QIcon.Off)
        self.pushButton_13.setIcon(icon2)
        self.pushButton_13.setIconSize(QSize(25, 25))
        self.pushButton_13.setObjectName("pushButton_13")
        self.ui.horizontalLayout_5.addWidget(self.pushButton_13)
        self.bankATMLabel.setText(self.atmName)

        # Success message
        QMessageBox.information(self, 'Success Message', 'Successfully!')
        self.connectedToTower = True
        self.ui.scanBtn.setStyleSheet("color: green")

    def openInvisibleWindow(self):
        self.invisibleWindow = InvisibleWindow(self)
        self.invisibleWindow.setWindowTitle("GSM Bank Software")
        self.invisibleWindow.show()

    def openPortWindow(self):
        self.portWindow = PortWindow(self)
        self.portWindow.setWindowTitle("GSM Bank Software")
        self.portWindow.show()
        
    def openSettingsWindow(self):
        self.settingsWindow = SettingsWindow(self)
        self.settingsWindow.setWindowTitle("GSM Bank Software")
        self.settingsWindow.show()

    def openSupportedATMsWindow(self):
        self.supportedATMsWindow = SupportedATMsWindow(self)
        self.supportedATMsWindow.setWindowTitle("GSM Bank Software")
        self.supportedATMsWindow.setFixedSize(QSize(425, 330))
        self.supportedATMsWindow.show()

    def saveATM(self, name):
        self.atmName = name

    def saveInfo(self, info):
        self.info = info

    def connectToGSM(self):
        self.restartProgressBar(callback=self.GSMSignal)
    
    def connectStatus(self):
        QMessageBox.information(self, 'Success Message', 'PC connected to GSM Successfully!')
        self.ui.statusLabel.setText("Connected")
        self.ui.statusLabel.setStyleSheet("color: green")
        self.connectedToGSM = True
        
    def connectToATM(self):
        if self.connectedToGSM:
            if not self.connectedToATM:
                self.restartProgressBar(callback=self.ATMSignal)
                self.connectedToATM = True
        else:
            QMessageBox.warning(self, 'Warning Message', 'Connect to GSM first!')

    def connectToTower(self):
        if self.connectedToGSM and self.connectedToATM:
            if not self.connectedToTower:
                self.restartProgressBar(callback=self.TowerSignal)
        else:
            QMessageBox.warning(self, 'Warning Message', 'Connect to GSM & ATM first!')

    def showInformation(self):
        if self.connectedToATM and self.connectedToGSM \
            and self.connectedToTower and self.scannable:
            self.showPopup(message=self.info)
        else:
            QMessageBox.warning(self, 'Warning Message', 'Connect Devices first!')

    def disconnectAll(self):
        self.connectedToATM = False
        self.connectedToGSM = False
        self.connectedToTower = False
        self.scannable = False

        self.ui.statusLabel.setText("Disconnected")
        self.ui.statusLabel.setStyleSheet("color: red;")
        self.ui.scanBtn.setStyleSheet("")

        try:
            self.pushButton_13.close()
            self.pushButton_14.close()
            self.bankATMLabel.close()

        except:
            # Tried to disconnect before connecting
            pass
        
class InvisibleWindow(QMainWindow):

    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent=parent)
        self.ui = Ui_InvisibleWindow()
        self.ui.setupUi(self)

        self.Ui_components()

    def Ui_components(self):
        self.ui.saveATMBtn.clicked.connect(lambda: self.parent.saveATM(self.ui.textEdit.toPlainText()))
        self.ui.saveInfoBtn.clicked.connect(lambda: self.parent.saveInfo(self.ui.textEdit_2.toHtml()))

      
class PortWindow(QMainWindow):

    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent=parent)
        self.ui = Ui_PortWindow()
        self.ui.setupUi(self)

        self.Ui_components()

    def Ui_components(self):
        self.ui.pushButton.clicked.connect(self.close)
        # self.ui.saveATMBtn.clicked.connect(lambda: self.parent.saveATM(self.ui.textEdit.toPlainText()))
        # self.ui.saveInfoBtn.clicked.connect(lambda: self.parent.saveInfo(self.ui.textEdit_2.toHtml()))



class SupportedATMsWindow(QMainWindow):

    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent=parent)
        self.ui = Ui_SupportedATMWindow()
        self.ui.setupUi(self)

        self.Ui_components()

    def Ui_components(self):
        pass

      
class SettingsWindow(QMainWindow):

    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent=parent)
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)

        self.Ui_components()

    def Ui_components(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
