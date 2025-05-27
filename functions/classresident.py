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

from database.database import printTime, warnMessageBox, infoMessageBox, errorMessageBox
from resource import resource_qrc

from uipyfiles.addresidentui import Ui_addResidentDialog
from uipyfiles.addcomplaintui import Ui_addComplaintDialog
from uipyfiles.addofficialui import Ui_addOfficialDialog
from uipyfiles.mainui import Ui_MainWindow

from utils import all_fields_filled, cancel_dialog

class AddResidentDialog(QDialog, Ui_addResidentDialog):
    def __init__(self,parent = None, db=None):
        printTime("Initializing add resident dialog")
        super().__init__(parent)
        self.setupUi(self)
        self.db = db
        #Restrict Resident ID to ####-####
        regex = QRegExp(r"^\d{4}-\d{4}$")
        validator = QRegExpValidator(regex)
        self.addresident_residentID_input.setValidator(validator)
        self.addresident_upload_button.clicked.connect(self.browse_photo)
        self.addresident_addentry_button.clicked.connect(self.save_resident)
        self.addresident_view_button.clicked.connect(self.view_photo)
        self.addresident_dob_input.editingFinished.connect(self.on_dob_editing_finished)
        # Contact number validation
        contact_regex = QRegExp(r"^\d{11}$")
        contact_validator = QRegExpValidator(contact_regex)
        self.addresident_contact_input.setValidator(contact_validator)

        #Auto-generate Resident ID
        new_id = self.db.generate_id("residents")
        self.addresident_residentID_input.setText(new_id)
        # (Optional) Allow editing:
        self.addresident_residentID_input.setEnabled(True)
        self.addresident_age_input.setEnabled(False)

        self.file_path = None
        self.photo_path = None

        #Cancel button
        self.addresident_cancel_button.clicked.connect(lambda: cancel_dialog(self))

    def save_resident(self):
        fields = [
            self.addresident_residentID_input,
            self.addresident_firstname_input,
            self.addresident_lastname_input,
            self.addresident_dob_input,
            self.addresident_photo_label,
            self.addresident_address_input,
            self.addresident_contact_input,
            self.addresident_sex_input
    ]
        if not all_fields_filled(fields):
            warnMessageBox(self, "Input Error", "Please fill in all required fields.")
            return
        
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
                warnMessageBox(self, "Input Error", "Resident ID must be in the format ####-#### (8 digits).")
                return

            # Check if Resident ID already exists 
            self.db.cursor.execute("SELECT 1 FROM residents WHERE resident_id = %s", (resident_id,))
            if self.db.cursor.fetchone():
                warnMessageBox(self, "Duplicate ID", "Resident ID already exists. Please enter a unique ID.")
                return
            
            # Check if photo_cred is provided
            if not self.photo_path:
                warnMessageBox(self, "Input Error", "Please upload a photo for the resident.")
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
            infoMessageBox(self, "Success", "Resident added successfully!")
            self.accept()
        except Exception as e:
            errorMessageBox(self, "Error", f"Failed to add resident:\n{e}")
    
    def browse_photo(self):
        printTime("Opening file dialog to select photo")
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

            
    def view_photo(self):
        file_path = self.addresident_photo_label.text()
        if os.path.isfile(file_path):
            os.startfile(file_path)
        else:
            warnMessageBox(self, "File Not Found", "The selected photo file does not exist.")


    def on_dob_editing_finished(self):
        age = self.db.calculate_age(self.addresident_dob_input.date().toString("yyyy-MM-dd"))
        self.addresident_age_input.setText(str(age))
