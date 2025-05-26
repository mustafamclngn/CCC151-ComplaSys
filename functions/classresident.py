import os
import shutil
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

class AddResidentDialog(QDialog, Ui_addResidentDialog):
    def __init__(self,parent = None, db=None):
        print("Opening AddResidentDialog")  # Debug print
        super().__init__(parent)
        self.setupUi(self)
        self.db = db
        #Restrict Resident ID to ####-####
        regex = QRegExp(r"^\d{4}-\d{4}$")
        validator = QRegExpValidator(regex)
        self.addresident_residentID_input.setValidator(validator)
        self.addresident_upload_button.clicked.connect(self.browse_photo)
        self.addresident_addentry_button.clicked.connect(self.save_resident)
        # Contact number validation
        contact_regex = QRegExp(r"^\d{11}$")
        contact_validator = QRegExpValidator(contact_regex)
        self.addresident_contact_input.setValidator(contact_validator)

        #Auto-generate Resident ID
        new_id = self.db.generate_id("residents")
        self.addresident_residentID_input.setText(new_id)
        # (Optional) Allow editing:
        self.addresident_residentID_input.setEnabled(True)

        self.file_path = None
        self.photo_path = None

    def save_resident(self):
        try:
            if self.file_path:
                local_dir = os.path.join('.', 'photos')
                if not os.path.exists(local_dir):
                    os.makedirs(local_dir)
                ext = os.path.splitext(self.file_path)[1]
                self.photo_path = os.path.join(local_dir, self.addresident_residentID_input.text() + ext)
                shutil.copy(self.file_path, self.photo_path)


            resident_id = self.addresident_residentID_input.text()
            if not resident_id or not self.addresident_residentID_input.hasAcceptableInput():
                QMessageBox.warning(self, "Input Error", "Resident ID must be in the format ####-#### (8 digits).")
                return

            # --- Check if Resident ID already exists ---
            self.db.cursor.execute("SELECT 1 FROM residents WHERE resident_id = %s", (resident_id,))
            if self.db.cursor.fetchone():
                QMessageBox.warning(self, "Duplicate ID", "Resident ID already exists. Please enter a unique ID.")
                return
                    
            first_name = self.addresident_firstname_input.text()
            last_name = self.addresident_lastname_input.text()
            birth_date = self.addresident_dob_input.date().toString("yyyy-MM-dd")
            #age = self.addresident_age_input.text()
            photo_cred = self.photo_path
            address = self.addresident_address_input.toPlainText()
            contact = self.addresident_contact_input.text()
            sex = self.addresident_sex_input.currentText()
            
            
            resident = (
                resident_id,
                first_name,
                last_name,
                birth_date,
                photo_cred,
                address,
                contact,
                sex
            )
            self.db.insert_resident(resident)  # Insert into the database
            QMessageBox.information(self, "Success", "Resident added successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add resident:\n{e}")
    
    def browse_photo(self):
        print("Button Clicked")
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Photo",
            "",
            "Image Files (*.jpg *.jpeg *.png)",
            options=options
        )
        if file_path:
            self.addresident_photo_label.setText(file_path)
            self.file_path = file_path

            



