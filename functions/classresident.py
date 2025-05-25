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
from uipyfiles.inforesidentui import Ui_infoResidentDialog

class AddResidentDialog(QDialog, Ui_infoResidentDialog):
    def __init__(self,parent = None):
        print("Opening AddResidentDialog")  # Debug print
        super().__init__(parent)
        self.setupUi(self)
        self.db = Database()
        #Restrict Resident ID to ####-####
        regex = QRegExp(r"^\d{4}-\d{4}$")
        validator = QRegExpValidator(regex)
        self.inforesident_residentID_input.setValidator(validator)
        self.saveResBtn.clicked.connect(self.save_resident)
        #self.addresident_cancel_button.clicked.connect(self.reject)
        #self.addresident_upload_button.clicked.connect(self.browse_photo)
        # Contact number validation
        contact_regex = QRegExp(r"^\d{11}$")
        contact_validator = QRegExpValidator(contact_regex)
        self.inforesident_contact_input.setValidator(contact_validator)
         # Age validation: only 3 digits (0-999)
        age_validator = QIntValidator(0, 122)
        self.inforesident_age_input.setValidator(age_validator)
        self.delResBtn.clicked.connect(self.delete_resident)
    
    def save_resident(self):
        try:
            resident_id = self.inforesident_residentID_input.text()
            if not resident_id or not self.inforesident_residentID_input.hasAcceptableInput():
                QMessageBox.warning(self, "Input Error", "Resident ID must be in the format ####-#### (8 digits).")
                return 
            first_name = self.inforesident_firstname_input.text()
            last_name = self.inforesident_lastname_input.text()
            birth_date = self.inforesident.date().toString("yyyy-MM-dd")
            age = self.inforesident_age_input.text()
            photo_cred = self.inforesident_photo_label.text() #may be changed depends on testing
            address = self.inforesident_address_input.toPlainText()
            contact = self.inforesident_contact_input.text()
            sex = self.inforesident_sex_input.currentText()
            
            
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
            self.inforesident_photo_label.setText(file_path)

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
        dialog = Ui_infoResidentDialog(self)
        # Pre-fill dialog fields
        dialog.inforesident_residentID_input.setText(str(data[0]))
        dialog.inforesident_firstname_input.setText(str(data[1]))
        dialog.inforesident_lastname_input.setText(str(data[2]))
        dialog.inforesident_age_input.setText(str(data[3]))
        dialog.inforesident_dob_input.setDate(QtCore.QDate.fromString(str(data[4]), "yyyy-MM-dd"))
        dialog.inforesident_photo_label.setText(str(data[5]))
        dialog.inforesident_address_input.setPlainText(str(data[6]))
        dialog.inforesident_contact_input.setText(str(data[7]))
        dialog.inforesident_sex_input.setCurrentText(str(data[8]))
        # Disable editing of resident_id
        dialog.inforesident_residentID_input.setEnabled(False)
        if dialog.exec_() == QDialog.Accepted:
            # Update the record
            updated = (
                dialog.inforesident_firstname_input.text(),
                dialog.inforesident_lastname_input.text(),
                dialog.inforesident_age_input.text(),
                dialog.inforesident_dob_input.date().toString("yyyy-MM-dd"),
                dialog.inforesident_photo_label.text(),
                dialog.inforesident_address_input.toPlainText(),
                dialog.inforesident_contact_input.text(),
                dialog.inforesident_sex_input.currentText(),
                resident_id
            )
            db.cursor.execute('''UPDATE Resident SET first_name=%s, last_name=%s, age=%s, birth_date=%s, photo_cred=%s, address=%s, contact=%s, sex=%s WHERE resident_id=%s''', updated)
            db.conn.commit()
            self.load_residents()
