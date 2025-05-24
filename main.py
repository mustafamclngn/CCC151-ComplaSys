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

        #Datettime
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)
        self.updateDateTime()

    def updateDateTime(self):
        current = QDateTime.currentDateTime()
        formatted = current.toString("dddd, MMM d, h:mm AP")
        self.labelDateTime1.setText(formatted)
        self.labelDateTime2.setText(formatted)

    def show_exit_message(self):
        msg = QMessageBox()
        msg.setStyleSheet("color: white; background-color: rgb(0, 0, 10);")
        msg.setWindowTitle('Exit')
        msg.setText('Are you sure you want to exit?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        reply = msg.exec_()
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

    def show_about(self):
        self.stackedWidget.setCurrentIndex(4)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainClass()
    main.show()
    sys.exit(app.exec_())
