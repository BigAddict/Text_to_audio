import ctypes
myappid = 'addict.texttoaudio.bigaddict.v1.0.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
## IMPORTS
########################################################################
import os
import sys
########################################################################
# IMPORT GUI FILE
from ui_interface import *
########################################################################
########################################################################
# IMPORT Custom widgets
from Custom_Widgets.Widgets import *
########################################################################
# IMPORT QtCore
from PyQt5.QtCore import QRunnable, QObject, QThreadPool, pyqtSignal as Signal, pyqtSlot as Slot
import backend
# INITIALIZE APP SETTINGS
settings = QSettings()
########################################################################
## MAIN FUNCTION OF THE APP
class MySignals(QObject):
    convertion_completed = Signal(bool)

class Worker1(QRunnable):
    def __init__(self, voice, rate, pitch, text, file):
        super().__init__()
        try:
            self.filename = file
            self.voice = voice
            self.rate = rate
            self.pitch = pitch
            self.words = text
            self.signals = MySignals()
        except Exception as e:
            print(e)
    
    @Slot()
    def run(self):
        try:
            self.engine = backend.Text_To_Audio(self.voice, self.rate, self.pitch)
            backend.Text_To_Audio.convert_to_audio(self.engine, self.words, self.filename)
            self.signals.convertion_completed.emit(True)
        except Exception as e:
            print(e)

########################################################################
## MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Text To Audio")
        self.ui.convertBtn.clicked.connect(self.start_jobs)
        ########################################################################
        # APPLY JSON STYLESHEET
        ########################################################################
        # self = QMainWindow class
        # self.ui = Ui_MainWindow / user interface class
        #Use this if you only have one json file named "style.json" inside the root directory, "json" directory or "jsonstyles" folder.
        loadJsonStyle(self, self.ui) 

        # Use this to specify your json file(s) path/name
        # loadJsonStyle(self, self.ui, jsonFiles = {
        #     "mystyle.json", "style.json"
        #     }) 

        ########################################################################

        #######################################################################
        # SHOW WINDOW
        #######################################################################
        self.show() 

        #######################################################################
        # UPDATE THE APP SETTINGS LOADED FROM THE JSON STYLESHEET
        # ITS IMPORTANT TO RUN THIS AFTER SHOWING THE WINDOW
        # THIS PROCESS WILL RUN IN A SEPARATE THREAD WHEN GENERATING NEW ICONS
        # TO PREVENT THE WINDOW FROM BEING UNRESPONSIVE
        ########################################################################
        # self = QMainWindow class
        QAppSettings.updateAppSettings(self)


    def start_jobs(self):
        pool = QThreadPool.globalInstance()
        self.voice = self.ui.comboBox.currentText()
        self.rate = int(self.ui.rateSpn.value())
        self.pitch = float(self.ui.pitchSpn.value())
        self.words = self.ui.plainTextEdit.toPlainText()
        self.filename = self.ui.filename_edit.text()
        convertion_worker = Worker1(self.voice, self.rate, self.pitch, self.words, self.filename)
        self.ui.convertBtn.setDisabled(True)
        convertion_worker.signals.convertion_completed.connect(self.complete)
        pool.start(convertion_worker)

    def complete(self):
        self.ui.convertBtn.setEnabled(True)
        self.ui.plainTextEdit.clear()
        self.ui.filename_edit.clear()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Your text is converted to audio")
        msg.setWindowTitle("Convertion complete")
        msg.setStandardButtons(QMessageBox.Cancel)
        value = msg.exec()
        







########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ########################################################################
    ## 
    ########################################################################
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
########################################################################
## END===>
########################################################################  
