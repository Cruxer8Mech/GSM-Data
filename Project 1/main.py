import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon
from ui_main import Ui_MainWindow
import ctypes

myappid = 'tahiralauddin.gsm-data-receiver.1.0.0' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class Main(QMainWindow):

    def __init__(self):
        super().__init__()

        # Set window title

        # Set window geometry
        self.setGeometry(100, 100, 500, 300)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowIcon(QIcon("logo.jpg"))

        self.Ui_components()

    def Ui_components(self):
        # Close software window
        self.ui.exitBtn.clicked.connect(self.close)
        self.ui.closeBtn.clicked.connect(self.close)

        self.ui.readBtn.clicked.connect(lambda: self.showPopup())
        self.ui.helpBtn.clicked.connect(lambda: self.showPopup(message="Telegram @ItsCvv"))
        self.ui.showDataBtn.clicked.connect(lambda: self.showPopup(message="No Connected!"))
        self.ui.connectToATMBtn.clicked.connect(lambda: self.showPopup(message="No ATMs detected within range!"))
        self.ui.connectToPOSBtn.clicked.connect(lambda: self.showPopup(message="No POS Systems detected within range!"))
        self.ui.errorCheckBtn.clicked.connect(lambda: self.showPopup(message="Errors Cleared"))
        self.ui.saveDBBtn.clicked.connect(lambda: self.showPopup(message="Saved to Database!"))
        self.ui.importDBBtn.clicked.connect(lambda: self.showPopup(message="Imported Successfully!"))
        self.ui.showDataBtn.clicked.connect(lambda: self.showPopup(message="No Connected!"))
        
        # Progress feature
        self.ui.refreshNetworkBtn.clicked.connect(lambda: self.showPopup(message="Refreshed Succesfully!", progress=True))
        self.ui.connectBtn.clicked.connect(lambda: self.showPopup(message="Connected to GSM (No Sim detected)!", progress=True, connected=True))
        self.ui.resetNetworkBtn.clicked.connect(lambda: self.showPopup(message="Reset Succesfully!", progress=True))

        self.ui.progressBar.setValue(0)


    def showPopup(self, title='BETA GSM RECIEVER ATM NETWORK 1.1', message="Data imported successfully!", **kwargs):
        if kwargs.get('progress'):
            self.restartProgressBar()

        QMessageBox.information(self, title, message)
        if kwargs.get('connected'):
            self.ui.statusLabel.setText("CONNECTED")

    def restartProgressBar(self):
        import time
        for i in range(100):
            time.sleep(0.05)
            self.ui.progressBar.setValue(i+1)
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
