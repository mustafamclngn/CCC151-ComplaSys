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
from uipyfiles.addofficialui import Ui_addOfficialDialog
from uipyfiles.mainui import Ui_MainWindow
from database.database import Database
from resource import resource_qrc

class AddOfficialDialog(QDialog, Ui_addOfficialDialog):
    def __init__(self,parent = None, db=None):
        print("Opening AddOfficialDialog")  # Debug print
        super().__init__(parent)
        self.setupUi(self)
        self.db = db
        #Restrict Official ID to ####-####
        regex = QRegExp(r"^\d{4}-\d{4}$")
        validator = QRegExpValidator(regex)
        self.addofficial_officialID_input.setValidator(validator)
        self.addofficial_addentry_button.clicked.connect(self.save_official)
        # Contact number validation
        contact_regex = QRegExp(r"^\d{11}$")
        contact_validator = QRegExpValidator(contact_regex)
        self.addofficial_contact_input.setValidator(contact_validator)

        #Auto-generate Official ID
        new_id = self.db.generate_id("barangay_officials")
        self.addofficial_officialID_input.setText(new_id)
        # (Optional) Allow editing:
        self.addofficial_officialID_input.setEnabled(True)
        
    def save_official(self):
        try:
            official_id = self.addofficial_officialID_input.text().strip()
            if not official_id or not self.addofficial_officialID_input.hasAcceptableInput():
                QMessageBox.warning(self, "Input Error", "Official ID must be in the format ####-#### (8 digits).")
                return
                    # --- Check if Official ID already exists ---
            self.db.cursor.execute("SELECT 1 FROM barangay_officials WHERE barangay_official_id = %s", (official_id,))
            if self.db.cursor.fetchone():
                QMessageBox.warning(self, "Duplicate ID", "Official ID already exists. Please enter a unique ID.")
                return
        # -------------------------------------------
            first_name = self.addofficial_firstname_input.text()
            last_name = self.addofficial_lastname_input.text()
            contact = self.addofficial_contact_input.text()
            position = self.addofficial_position_input.currentText()

            official = (
                official_id,
                first_name,
                last_name,
                contact,
                position
            )
            self.db.insert_barangay_official(official)
            QMessageBox.information(self, "Success", "Official added successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add official:\n{e}")



