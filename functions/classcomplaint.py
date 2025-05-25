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
from uipyfiles.infocomplaintui import Ui_infoComplaintDialog

class AddComplaintDialog(QDialog, Ui_infoComplaintDialog):
    def __init__(self, parent=None):
        print("Opening AddComplaintDialog")  # Debug print
        super().__init__(parent)
        self.setupUi(self)
        self.db = Database()
        # Restrict Complaint ID to ####-####
        regex = QRegExp(r"^\d{4}-\d{4}$")
        validator = QRegExpValidator(regex)
        self.addcomplaint_complaintID_input.setValidator(validator)
        self.saveCompBtn.clicked.connect(self.save_complaint)
        #self.addcomplaint_cancel_button.clicked.connect(self.reject)
        self.delCompBtn.clicked.connect(self.delete_complaint)

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
            description = self.addcomplaint_description_input.text()
            location = self.addcomplaint_location_input.text()
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

    def delete_complaint(self):
        selected = self.complaint_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Delete Complaint", "Please select a complaint to delete.")
            return
        complaint_id = self.complaint_table.item(selected, 0).text()
        reply = QMessageBox.question(self, "Delete Complaint", f"Delete complaint {complaint_id}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            db = Database()
            db.cursor.execute("DELETE FROM Complaint WHERE complaint_id = %s", (complaint_id,))
            db.conn.commit()
            self.load_complaints()

    def edit_complaint(self):
        selected = self.complaint_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Edit Complaint", "Please select a complaint to edit.")
            return
        complaint_id = self.complaint_table.item(selected, 0).text()
        db = Database()
        db.cursor.execute("SELECT * FROM Complaint WHERE complaint_id = %s", (complaint_id,))
        data = db.cursor.fetchone()
        if not data:
            QMessageBox.warning(self, "Edit Complaint", "Complaint not found.")
            return
        dialog = AddComplaintDialog(self)
        # Pre-fill dialog fields
        dialog.addcomplaint_complaintID_input.setText(str(data[0]))
        dialog.addcomplaint_date_input.setDate(QtCore.QDate.fromString(str(data[1]), "yyyy-MM-dd"))
        dialog.addcomplaint_description_input.setText(str(data[2]))
        dialog.addcomplaint_residentID_input.setCurrentText(str(data[3]))
        dialog.addcomplaint_category_input.setCurrentText(str(data[4]))
        dialog.addcomplaint_status_input.setCurrentText(str(data[5]))
        dialog.addcomplaint_location_input.setText(str(data[6]))
        # Disable editing of complaint_id
        dialog.addcomplaint_complaintID_input.setEnabled(False)
        if dialog.exec_() == QDialog.Accepted:
            updated = (
                dialog.addcomplaint_date_input.date().toString("yyyy-MM-dd"),
                dialog.addcomplaint_description_input.text(),
                dialog.addcomplaint_residentID_input.currentText(),
                dialog.addcomplaint_category_input.currentText(),
                dialog.addcomplaint_status_input.currentText(),
                dialog.addcomplaint_location_input.text(),
                complaint_id
            )
            db.cursor.execute('''UPDATE Complaint SET date_time=%s, complaint_desc=%s, resident_id=%s, complaint_category=%s, complaint_status=%s, location=%s WHERE complaint_id=%s''', updated)
            db.conn.commit()
            self.load_complaints()
