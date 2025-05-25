import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5 import QtCore
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIntValidator

from database.database import Database
from resource import resource_qrc

from uipyfiles.infocomplaintui import Ui_infoComplaintDialog
from uipyfiles.infoofficialui import Ui_infoOfficialDialog
from uipyfiles.inforesidentui import Ui_infoResidentDialog
from uipyfiles.mainui import Ui_MainWindow

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

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

        # Add Dialogs
        self.addResBtn.clicked.connect(self.add_residents)
        self.addCompBtn.clicked.connect(self.add_complaints)
        self.addOffiBtn.clicked.connect(self.add_officials)

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

#add dialogs
    def add_residents(self):
        dialog = AddResidentDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_residents() #Refresh after adding
        
    def add_complaints(self):
        dialog = AddComplaintDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_complaints() #Refresh after adding

    def add_officials(self):
        dialog = AddOfficialDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_officials() #Refresh after adding

    def load_residents(self):
        db = Database()  # Create a new Database instance
        self.resident_table.setRowCount(0)
        db.cursor.execute("SELECT * FROM Resident")
        residents = db.cursor.fetchall()
        for row_num, row_data in enumerate(residents):
            self.resident_table.insertRow(row_num)
            self.resident_table.setItem(row_num, 0, QTableWidgetItem(str(row_data[0])))  # ResidentID
            self.resident_table.setItem(row_num, 1, QTableWidgetItem(str(row_data[1])))  # FirstName
            self.resident_table.setItem(row_num, 2, QTableWidgetItem(str(row_data[2])))  # LastName
            self.resident_table.setItem(row_num, 3, QTableWidgetItem(str(row_data[3])))  # Age
            self.resident_table.setItem(row_num, 4, QTableWidgetItem(str(row_data[8])))  # Sex
            self.resident_table.setItem(row_num, 5, QTableWidgetItem(str(row_data[4])))  # Birthdate
            self.resident_table.setItem(row_num, 6, QTableWidgetItem(str(row_data[7])))  # Contact
            self.resident_table.setItem(row_num, 7, QTableWidgetItem(str(row_data[6])))  # Address
            self.resident_table.setItem(row_num, 8, QTableWidgetItem(str(row_data[5])))  # Credentials (photo_cred)

    def load_complaints(self):
        db = Database()  # Create a new Database instance
        self.complaint_table.setRowCount(0)
        db.cursor.execute("SELECT * FROM Complaint")
        complaints = db.cursor.fetchall()
        for row_num, row_data in enumerate(complaints):
            self.complaint_table.insertRow(row_num)
            self.complaint_table.setItem(row_num, 0, QTableWidgetItem(str(row_data[0])))  # ComplaintID
            self.complaint_table.setItem(row_num, 1, QTableWidgetItem(str(row_data[3])))  # ResidentID
            self.complaint_table.setItem(row_num, 2, QTableWidgetItem(str(row_data[4])))  # Category
            self.complaint_table.setItem(row_num, 3, QTableWidgetItem(str(row_data[2])))  # Description
            self.complaint_table.setItem(row_num, 4, QTableWidgetItem(str(row_data[1])))  # DateTime
            self.complaint_table.setItem(row_num, 5, QTableWidgetItem(str(row_data[6])))  # Location
            self.complaint_table.setItem(row_num, 6, QTableWidgetItem(str(row_data[5])))  # Status

    def load_officials(self):
        db = Database()  # Create a new Database instance
        self.official_table.setRowCount(0)
        db.cursor.execute("SELECT * FROM BarangayOfficials")
        officials = db.cursor.fetchall()
        for row_num, row_data in enumerate(officials):
            self.official_table.insertRow(row_num)
            self.official_table.setItem(row_num, 0, QTableWidgetItem(str(row_data[0])))  # OFFICIALID
            self.official_table.setItem(row_num, 1, QTableWidgetItem(str(row_data[4])))  # POSITION
            self.official_table.setItem(row_num, 2, QTableWidgetItem(str(row_data[1])))  # FIRSTNAME
            self.official_table.setItem(row_num, 3, QTableWidgetItem(str(row_data[2])))  # LASTNAME
            self.official_table.setItem(row_num, 4, QTableWidgetItem(str(row_data[3])))  # CONTACT

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
