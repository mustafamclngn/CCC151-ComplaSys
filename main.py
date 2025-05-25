import sys

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5 import QtCore

from database.database import Database
from resource import resource_qrc

from uipyfiles.inforesidentui import Ui_infoResidentDialog
from uipyfiles.infocomplaintui import Ui_infoComplaintDialog
from uipyfiles.infoofficialui import Ui_infoOfficialDialog
from uipyfiles.mainui import Ui_MainWindow
from uipyfiles.addcomplaintui import Ui_addComplaintDialog
from uipyfiles.addresidentui import Ui_addResidentDialog
from uipyfiles.addofficialui import Ui_addOfficialDialog

from functions.classcomplaint import AddComplaintDialog
from functions.classofficial import AddOfficialDialog
from functions.classresident import AddResidentDialog
            
class MainClass(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #Font
        font_id = QFontDatabase.addApplicationFont("resource/Gilroy-Medium.ttf")
        if font_id == -1:
            print("Failed to load font.")
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            custom_font = QFont(font_family, 12)
            app.setFont(custom_font)

        #Automatic on dashboard button when load
        QTimer.singleShot(0, self.homeBtn.click)
        self.homeBtn.clicked.connect(self.show_home)
        self.resBtn.clicked.connect(self.show_residents)
        self.compBtn.clicked.connect(self.show_complaints)
        self.offiBtn.clicked.connect(self.show_officials)
        self.abtBtn.clicked.connect(self.show_about)
        self.exBtn.clicked.connect(self.show_exit_message)

        #add dialogs (to be changed)
        self.addResBtn.clicked.connect(self.add_residents)
        self.addCompBtn.clicked.connect(self.add_complaints)
        self.addOffiBtn.clicked.connect(self.add_officials)
        
        #Datettime
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)
        self.updateDateTime()
        
        #Delete Buttons
        self.delResBtn.clicked.connect(self.delete_resident)
        self.delCompBtn.clicked.connect(self.delete_complaint)
        self.delOffiBtn_2.clicked.connect(self.delete_official)

        #Edit Buttons
        self.updResBtn.clicked.connect(self.edit_resident)
        self.updCompBtn.clicked.connect(self.edit_complaint)
        self.updOffiBtn_2.clicked.connect(self.edit_official)

    def updateDateTime(self):
        current = QDateTime.currentDateTime()
        formatted = current.toString("ddd, MMM d, h:mm AP")
        self.labelDateTime1.setText(formatted)
        self.labelDateTime2.setText(formatted)

#add dialogs
    def add_residents(self):
        dialog = AddResidentDialog(self)
        dialog.exec_()
        
    def add_complaints(self):
        dialog = AddComplaintDialog(self)
        dialog.exec_()

    def add_officials(self):
        dialog = AddOfficialDialog(self)
        dialog.exec_()

    def show_exit_message(self):
        reply = QMessageBox.question(self, 'Exit', 'Are you sure you want to exit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
            
    def show_home(self):
        self.stackedWidget.setCurrentIndex(0)

    def show_residents(self):
        self.stackedWidget.setCurrentIndex(1)
        self.load_residents()

    def show_complaints(self):
        self.stackedWidget.setCurrentIndex(2)
        self.load_complaints()

    def show_officials(self):
        self.stackedWidget.setCurrentIndex(3)
        self.load_officials()

    def show_about(self):
        self.stackedWidget.setCurrentIndex(4)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainClass()
    main.show()
    sys.exit(app.exec_())
