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

from database.database import printTime, warnMessageBox, infoMessageBox, errorMessageBox
from resource import resource_qrc

from uipyfiles.addresidentui import Ui_addResidentDialog
from uipyfiles.addcomplaintui import Ui_addComplaintDialog
from uipyfiles.addofficialui import Ui_addOfficialDialog
from uipyfiles.mainui import Ui_MainWindow

from utils import all_fields_filled, cancel_dialog

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
        # Restrict Resident ID to YYYY-####
        regex = QRegExp(r"^\d{4}-\d{4}$")
        validator = QRegExpValidator(regex)
        self.addcomplaint_residentID_input.setValidator(validator)

        #Auto-generate Resident ID
        new_id = self.db.generate_id("complaints")
        self.addcomplaint_complaintID_input.setText(new_id)
        # (Optional) Allow editing:
        self.addcomplaint_complaintID_input.setEnabled(True)

        #Cancel Button
        self.addcomplaint_cancel_button.clicked.connect(lambda: cancel_dialog(self))

    def save_complaint(self):
        fields = [
            self.addcomplaint_complaintID_input,
            self.addcomplaint_date_input,
            self.addcomplaint_description_input,
            self.addcomplaint_residentID_input,
            self.addcomplaint_category_input,
            self.addcomplaint_status_input,
            self.addcomplaint_location_input
        ]
        if not all_fields_filled(fields):
            warnMessageBox(self, "Input Error", "Please fill in all required fields.")
            return
        try:
            complaint_id = self.addcomplaint_complaintID_input.text()
            if not complaint_id or not self.addcomplaint_complaintID_input.hasAcceptableInput():
                warnMessageBox(self, "Input Error", "Complaint ID must be in the format ####-#### (8 digits).")
                return

            #Duplication of ID
            self.db.cursor.execute("SELECT 1 FROM complaints WHERE complaint_id = %s", (complaint_id,))
            if self.db.cursor.fetchone():
                warnMessageBox(self, "Duplicate ID", "Complaint ID already exists. Please enter a unique ID.")
                return

            #Check Res_ID REQUIRED
            resident_id = self.addcomplaint_residentID_input.text()
            if not resident_id.strip():
                warnMessageBox(self, "Input Error", "Resident ID is required.")
                return
            
            #Check if Resident ID exists
            self.db.cursor.execute("SELECT 1 FROM residents WHERE resident_id = %s", (resident_id,))
            if not self.db.cursor.fetchone():
                warnMessageBox(self, "Input Error", "Resident ID does not exist. Please enter a valid Resident ID.")
                return
            
            #ID must follow pattern YYYY-####
            resident_id = self.addcomplaint_residentID_input.text()
            if not resident_id or not self.addcomplaint_residentID_input.hasAcceptableInput():
                warnMessageBox(self, "Input Error", "Resident ID must be in the format YYYY-#### (8 digits).")
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
            infoMessageBox(self, "Success", "Complaint added successfully!")
            self.accept()
        except Exception as e:
            errorMessageBox(self, "Error", f"Failed to add complaint:\n{e}")

