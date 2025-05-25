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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.db = Database()
        # Restrict Complaint ID to ####-####
        regex = QRegExp(r"^\d{4}-\d{4}$")
        validator = QRegExpValidator(regex)
        self.addcomplaint_complaintID_input.setValidator(validator)
        self.addcomplaint_addentry_button.clicked.connect(self.save_complaint)

        # Populate resident ID combo box
        self.populate_resident_ids()

    def populate_resident_ids(self):
        self.addcomplaint_residentID_input.clear()
        self.db.cursor.execute("SELECT resident_id FROM Resident")
        resident_ids = self.db.cursor.fetchall()
        for rid in resident_ids:
            self.addcomplaint_residentID_input.addItem(str(rid[0]))

    def save_complaint(self):
        try:
            complaint_id = self.addcomplaint_complaintID_input.text()
            if not complaint_id or not self.addcomplaint_complaintID_input.hasAcceptableInput():
                QMessageBox.warning(self, "Input Error", "Complaint ID must be in the format ####-#### (8 digits).")
                return
            resident_id = self.addcomplaint_residentID_input.currentText()
            category = self.addcomplaint_category_input.currentText()
            date = self.addcomplaint_date_input.date().toString("yyyy-dd-MM")
            description = self.addcomplaint_description_input.toPlaintext()
            location = self.addcomplaint_location_input.toPlaintext()
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
            sql = '''INSERT INTO Complaint
                (complaint_id, date_time, complaint_desc, resident_id, complaint_category, complaint_status, location)
                VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            self.db.cursor.execute(sql,complaint)
            self.db.conn.commit()
            QMessageBox.information(self, "Success", "Complaint added successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add complaint:\n{e}")


