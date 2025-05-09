import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5 import QtCore
from resources import resources_qrc
from addresidentui import Ui_addResidentDialog
from addcomplaintui import Ui_addComplaintDialog

from ComplaSys_ui import Ui_MainWindow

class MainClass(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #Font
        font_id = QFontDatabase.addApplicationFont("resources/Gilroy-Medium.ttf")
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
        self.settBtn.clicked.connect(self.show_settings)
        self.abtBtn.clicked.connect(self.show_about)
        self.faqBtn.clicked.connect(self.show_faq)
        self.exBtn.clicked.connect(self.show_exit_message)

        #add dialogs (to be changed)
        self.addResBtn.clicked.connect(self.add_residents)
        self.addCompBtn.clicked.connect(self.add_complaints)
        
        #Datettime
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)
        self.updateDateTime()

    def updateDateTime(self):
        current = QDateTime.currentDateTime()
        formatted = current.toString("ddd, MMM d, h:mm AP")
        self.labelDateTime1.setText(formatted)
        self.labelDateTime2.setText(formatted)
        self.labelDateTime3.setText(formatted)
        self.labelDateTime4.setText(formatted)
        self.labelDateTime5.setText(formatted)
        self.labelDateTime6.setText(formatted)
        self.labelDateTime7.setText(formatted)

    def add_complaints(self):
        dialog = QDialog(self)
        ui = Ui_addComplaintDialog()
        ui.setupUi(dialog)
        dialog.exec_()

    def add_residents(self):
        dialog = QDialog(self)
        ui = Ui_addResidentDialog()
        ui.setupUi(dialog)
        dialog.exec_()

    def show_exit_message(self):
        reply = QMessageBox.question(self, 'Exit', 'Are you sure you want to exit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
            
    def show_home(self):
        self.stackedWidget.setCurrentIndex(0)

    def show_residents(self):
        self.stackedWidget.setCurrentIndex(1)

    def show_complaints(self):
        self.stackedWidget.setCurrentIndex(2)

    def show_officials(self):
        self.stackedWidget.setCurrentIndex(3)

    def show_settings(self):
        self.stackedWidget.setCurrentIndex(4)

    def show_about(self):
        self.stackedWidget.setCurrentIndex(5)
    
    def show_faq(self):
        self.stackedWidget.setCurrentIndex(6)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainClass()
    main.show()
    sys.exit(app.exec_())
