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
    def __init__(self,parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.db = Database()
        #Restrict Official ID to ####-####
        regex = QRegExp(r"^\d{4}-\d{4}$")
        validator = QRegExpValidator(regex)
        self.addofficial_officialID_input.setValidator(validator)
        self.addofficial_save_button.clicked.connect(self.save_official)
        self.addofficial_cancel_button.clicked.connect(self.reject)
        # Contact number validation
        contact_regex = QRegExp(r"^\d{11}$")
        contact_validator = QRegExpValidator(contact_regex)
        self.addofficial_contact_input.setValidator(contact_validator)

    def save_official(self):
        try:
            official_id = self.addofficial_officialID_input.text().strip()
            if not official_id or not self.addofficial_officialID_input.hasAcceptableInput():
                QMessageBox.warning(self, "Input Error", "Official ID must be in the format ####-#### (8 digits).")
                return
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

            sql = '''INSERT INTO BarangayOfficials
                (official_id, first_name, last_name, contact, position)
                VALUES (%s, %s, %s, %s, %s)'''
            self.db.cursor.execute(sql, official)
            self.db.conn.commit()
            QMessageBox.information(self, "Success", "Official added successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add official:\n{e}")

    def edit_official(self):
        selected = self.official_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Edit Official", "Please select an official to edit.")
            return
        official_id = self.official_table.item(selected, 0).text()
        db = Database()
        db.cursor.execute("SELECT * FROM BarangayOfficials WHERE official_id = %s", (official_id,))
        data = db.cursor.fetchone()
        if not data:
            QMessageBox.warning(self, "Edit Official", "Official not found.")
            return
        dialog = AddOfficialDialog(self)
        # Pre-fill dialog fields
        dialog.addofficial_officialID_input.setText(str(data[0]))
        dialog.addofficial_firstname_input.setText(str(data[1]))
        dialog.addofficial_lastname_input.setText(str(data[2]))
        dialog.addofficial_contact_input.setText(str(data[3]))
        dialog.addofficial_position_input.setCurrentText(str(data[4]))
        # Disable editing of official_id
        dialog.addofficial_officialID_input.setEnabled(False)
        if dialog.exec_() == QDialog.Accepted:
            updated = (
                dialog.addofficial_firstname_input.text(),
                dialog.addofficial_lastname_input.text(),
                dialog.addofficial_contact_input.text(),
                dialog.addofficial_position_input.currentText(),
                official_id
            )
            db.cursor.execute('''UPDATE BarangayOfficials SET first_name=%s, last_name=%s, contact=%s, position=%s WHERE official_id=%s''', updated)
            db.conn.commit()
            self.load_officials()

    def delete_official(self):
        selected = self.official_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Delete Official", "Please select an official to delete.")
            return
        official_id = self.official_table.item(selected, 0).text()
        reply = QMessageBox.question(self, "Delete Official", f"Delete official {official_id}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            db = Database()
            db.cursor.execute("DELETE FROM BarangayOfficials WHERE official_id = %s", (official_id,))
            db.conn.commit()
            self.load_officials()

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

