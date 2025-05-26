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

from uipyfiles.addresidentui import Ui_addResidentDialog
from uipyfiles.addcomplaintui import Ui_addComplaintDialog
from uipyfiles.addofficialui import Ui_addOfficialDialog
from uipyfiles.mainui import Ui_MainWindow

class AddComplaintDialog(QDialog, Ui_addComplaintDialog):
    def __init__(self, parent=None, db=None):
        print("Opening AddComplaintDialog")  # Debug print
        super().__init__(parent)
        self.setupUi(self)
        self.db = db
        # Restrict Complaint ID to ####-####
        regex = QRegExp(r"^\d{4}-\d{4}$")
        validator = QRegExpValidator(regex)
        self.addcomplaint_complaintID_input.setValidator(validator)
        self.addcomplaint_addentry_button.clicked.connect(self.save_complaint)

        # Populate resident ID combo box
        self.populate_resident_ids()
        self.addcomplaint_date_input.setDateTime(QtCore.QDateTime.currentDateTime())

    def populate_resident_ids(self):
        self.addcomplaint_residentID_input.clear()

    def save_complaint(self):
        try:
            complaint_id = self.addcomplaint_complaintID_input.text()
            if not complaint_id or not self.addcomplaint_complaintID_input.hasAcceptableInput():
                QMessageBox.warning(self, "Input Error", "Complaint ID must be in the format ####-#### (8 digits).")
                return
            resident_id = self.addcomplaint_residentID_input.text()
            category = self.addcomplaint_category_input.currentText()
            date = self.addcomplaint_date_input.date().toString("yyyy-MM-dd")
            description = self.addcomplaint_description_input.toPlainText()
            location = self.addcomplaint_location_input.toPlainText()
            status = self.addcomplaint_status_input.currentText()
            
            complaint = (
                complaint_id,
                date,
                description,
                resident_id,
                category,
                status,
                location
            )
            self.db.insert_complaint(complaint)
            QMessageBox.information(self, "Success", "Complaint added successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add complaint:\n{e}")
            print(f"Error: {e}")

