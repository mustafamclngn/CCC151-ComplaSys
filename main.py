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
from uipyfiles.editcomplaintui import Ui_editComplaintDialog
from uipyfiles.editofficialui import Ui_editOfficialDialog
from uipyfiles.editresidentui import Ui_editResidentDialog
from uipyfiles.mainui import Ui_MainWindow

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

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


class AddComplaintDialog(QDialog, Ui_addComplaintDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.db = Database()
        # Restrict Complaint ID to ####-####
        regex = QRegExp(r"^\d{4}-\d{4}$")
        validator = QRegExpValidator(regex)
        self.addcomplaint_complaintID_input.setValidator(validator)
        self.addcomplaint_save_button.clicked.connect(self.save_complaint)
        self.addcomplaint_cancel_button.clicked.connect(self.reject)

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

            
class MainClass(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #Font
        font_id = QFontDatabase.addApplicationFont("resource/Gilroy-Medium.ttf")
        if font_id == -1:
            print("Failed to load font.")
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            custom_font = QFont(font_family, 12)
            app.setFont(custom_font)

        #Automatic on dashboard button when load
        QTimer.singleShot(0, self.homeBtn.click)
        self.homeBtn.clicked.connect(self.show_home)
        self.resBtn.clicked.connect(self.show_residents)
        self.compBtn.clicked.connect(self.show_complaints)
        self.offiBtn.clicked.connect(self.show_officials)
        self.abtBtn.clicked.connect(self.show_about)
        self.exBtn.clicked.connect(self.show_exit_message)

        #add dialogs (to be changed)
        self.addResBtn.clicked.connect(self.add_residents)
        self.addCompBtn.clicked.connect(self.add_complaints)
        self.addOffiBtn.clicked.connect(self.add_officials)

        #edit dialogs (to be changed)
        self.updResBtn.clicked.connect(self.edit_residents)
        self.updCompBtn.clicked.connect(self.edit_complaints)
        self.updOffiBtn.clicked.connect(self.edit_officials)

        #Datettime
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)
        self.updateDateTime()
        
        #Delete Buttons
        self.delResBtn.clicked.connect(self.delete_resident)
        self.delCompBtn.clicked.connect(self.delete_complaint)
        self.delOffiBtn_2.clicked.connect(self.delete_official)

        #Edit Buttons
        self.updResBtn.clicked.connect(self.edit_resident)
        self.updCompBtn.clicked.connect(self.edit_complaint)
        self.updOffiBtn_2.clicked.connect(self.edit_official)

    def updateDateTime(self):
        current = QDateTime.currentDateTime()
        formatted = current.toString("dddd, MMM d, h:mm AP")
        self.labelDateTime1.setText(formatted)
        self.labelDateTime2.setText(formatted)

#edit dialogs
    def edit_residents(self):
        dialog = QDialog(self)
        ui = Ui_editResidentDialog()
        ui.setupUi(dialog)
        dialog.exec_()

    def edit_complaints(self):
        dialog = QDialog(self)
        ui = Ui_editComplaintDialog()
        ui.setupUi(dialog)
        dialog.exec_()

    def edit_officials(self):
        dialog = QDialog(self)
        ui = Ui_editOfficialDialog()
        ui.setupUi(dialog)
        dialog.exec_()

#add dialogs
    def add_residents(self):
        dialog = AddResidentDialog(self)
        dialog.exec_()
        
    def add_complaints(self):
        dialog = AddComplaintDialog(self)
        dialog.exec_()

    def add_officials(self):
        dialog = AddOfficialDialog(self)
        dialog.exec_()

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

    def load_complaints(self):
        db = Database()  # Create a new Database instance
        self.complaint_table.setRowCount(0)
        db.cursor.execute("SELECT * FROM Complaint")
        complaints = db.cursor.fetchall()
        for row_num, row_data in enumerate(complaints):
            self.complaint_table.insertRow(row_num)
            self.complaint_table.setItem(row_num, 0, QTableWidgetItem(str(row_data[0])))  # ComplaintID
            self.complaint_table.setItem(row_num, 1, QTableWidgetItem(str(row_data[3])))  # ResidentID
            self.complaint_table.setItem(row_num, 2, QTableWidgetItem(str(row_data[4])))  # Category
            self.complaint_table.setItem(row_num, 3, QTableWidgetItem(str(row_data[2])))  # Description
            self.complaint_table.setItem(row_num, 4, QTableWidgetItem(str(row_data[1])))  # DateTime
            self.complaint_table.setItem(row_num, 5, QTableWidgetItem(str(row_data[6])))  # Location
            self.complaint_table.setItem(row_num, 6, QTableWidgetItem(str(row_data[5])))  # Status

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

    def show_exit_message(self):
        reply = QMessageBox.question(self, 'Exit', 'Are you sure you want to exit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
            
    def show_home(self):
        self.stackedWidget.setCurrentIndex(0)

    def show_residents(self):
        self.stackedWidget.setCurrentIndex(1)
        self.load_residents()

    def show_complaints(self):
        self.stackedWidget.setCurrentIndex(2)
        self.load_complaints()

    def show_officials(self):
        self.stackedWidget.setCurrentIndex(3)
        self.load_officials()

    def show_about(self):
        self.stackedWidget.setCurrentIndex(4)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainClass()
    main.show()
    sys.exit(app.exec_())
