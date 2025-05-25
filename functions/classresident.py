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
        self.addresident_save_button.clicked.connect(self.save_resident)
        self.addresident_cancel_button.clicked.connect(self.reject)
        self.addresident_upload_button.clicked.connect(self.browse_photo)
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

    def edit_resident(self):
        selected = self.resident_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Edit Resident", "Please select a resident to edit.")
            return
        resident_id = self.resident_table.item(selected, 0).text()
        db = Database()
        db.cursor.execute("SELECT * FROM Resident WHERE resident_id = %s", (resident_id,))
        data = db.cursor.fetchone()
        if not data:
            QMessageBox.warning(self, "Edit Resident", "Resident not found.")
            return
        dialog = AddResidentDialog(self)
        # Pre-fill dialog fields
        dialog.addresident_residentID_input.setText(str(data[0]))
        dialog.addresident_firstname_input.setText(str(data[1]))
        dialog.addresident_lastname_input.setText(str(data[2]))
        dialog.addresident_age_input.setText(str(data[3]))
        dialog.addresident_dob_input.setDate(QtCore.QDate.fromString(str(data[4]), "yyyy-MM-dd"))
        dialog.addresident_photo_label.setText(str(data[5]))
        dialog.addresident_address_input.setPlainText(str(data[6]))
        dialog.addresident_contact_input.setText(str(data[7]))
        dialog.addresident_sex_input.setCurrentText(str(data[8]))
        # Disable editing of resident_id
        dialog.addresident_residentID_input.setEnabled(False)
        if dialog.exec_() == QDialog.Accepted:
            # Update the record
            updated = (
                dialog.addresident_firstname_input.text(),
                dialog.addresident_lastname_input.text(),
                dialog.addresident_age_input.text(),
                dialog.addresident_dob_input.date().toString("yyyy-MM-dd"),
                dialog.addresident_photo_label.text(),
                dialog.addresident_address_input.toPlainText(),
                dialog.addresident_contact_input.text(),
                dialog.addresident_sex_input.currentText(),
                resident_id
            )
            db.cursor.execute('''UPDATE Resident SET first_name=%s, last_name=%s, age=%s, birth_date=%s, photo_cred=%s, address=%s, contact=%s, sex=%s WHERE resident_id=%s''', updated)
            db.conn.commit()
            self.load_residents()

    def delete_resident(self):
        selected = self.resident_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Delete Resident", "Please select a resident to delete.")
            return
        resident_id = self.resident_table.item(selected, 0).text()
        reply = QMessageBox.question(self, "Delete Resident", f"Delete resident {resident_id}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            db = Database()
            db.cursor.execute("DELETE FROM Resident WHERE resident_id = %s", (resident_id,))
            db.conn.commit()
            self.load_residents()

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