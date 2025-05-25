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
    def __init__(self,parent = None):
        print("Opening AddOfficialDialog")  # Debug print
        super().__init__(parent)
        self.setupUi(self)
        self.db = Database()
        #Restrict Resident ID to ####-####
        regex = QRegExp(r"^\d{4}-\d{4}$")
        validator = QRegExpValidator(regex)
        self.addresident_residentID_input.setValidator(validator)
        self.addresident_photo_button.clicked.connect(self.browse_photo)
        self.addresident_addentry_button.clicked.connect(self.save_resident)
        # Contact number validation
        contact_regex = QRegExp(r"^\d{11}$")
        contact_validator = QRegExpValidator(contact_regex)
        self.addresident_contact_input.setValidator(contact_validator)
         # Age validation: only 3 digits (0-999)
        age_validator = QIntValidator(0, 122)
        self.addresident_age_input.setValidator(age_validator)
    
    def save_resident(self):
        try:
            resident_id = self.addresident_residentID_input.text()
            if not resident_id or not self.addresident_residentID_input.hasAcceptableInput():
                QMessageBox.warning(self, "Input Error", "Resident ID must be in the format ####-#### (8 digits).")
                return
            first_name = self.addresident_firstname_input.text()
            last_name = self.addresident_lastname_input.text()
            birth_date = self.addresident_dob_input.date().toString("yyyy-MM-dd")
            age = self.addresident_age_input.text()
            photo_cred = self.addresident_photo_label.text() #may be changed depends on testing
            address = self.addresident_address_input.toPlainText()
            contact = self.addresident_contact_input.text()
            sex = self.addresident_sex_input.currentText()
            
            
            resident = (
                resident_id,
                first_name,
                last_name,
                age,
                birth_date,
                photo_cred,
                address,
                contact,
                sex
            )

            sql = '''INSERT INTO Resident
                (resident_id, first_name, last_name, age, birth_date, photo_cred, address, contact, sex)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            self.db.cursor.execute(sql, resident)
            self.db.conn.commit()
            QMessageBox.information(self, "Success", "Resident added successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add resident:\n{e}")
    
    def browse_photo(self):
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



