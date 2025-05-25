import sys

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5 import QtCore

from database.database import Database
from resource import resource_qrc

from uipyfiles.inforesidentui import Ui_infoResidentDialog
from uipyfiles.infocomplaintui import Ui_infoComplaintDialog
from uipyfiles.infoofficialui import Ui_infoOfficialDialog
from uipyfiles.mainui import Ui_MainWindow
from uipyfiles.addcomplaintui import Ui_addComplaintDialog
from uipyfiles.addresidentui import Ui_addResidentDialog
from uipyfiles.addofficialui import Ui_addOfficialDialog

from functions.classcomplaint import AddComplaintDialog
from functions.classofficial import AddOfficialDialog
from functions.classresident import AddResidentDialog
from functions.inforesidentdialog import InfoResidentDialog
from functions.infocomplaintdialog import InfoComplaintDialog
# from functions.infoofficialdialog import InfoOfficialDialog
from datetime import datetime
            
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
        
        #Datettime
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)
        self.updateDateTime()
        
        #Delete Buttons
       # self.delResBtn.clicked.connect(self.delete_resident)
       # self.delCompBtn.clicked.connect(self.delete_complaint)
       # self.delOffiBtn_2.clicked.connect(self.delete_official)

        #Edit Buttons
        #self.updResBtn.clicked.connect(self.edit_resident)
        #self.updCompBtn.clicked.connect(self.edit_complaint)
        #self.updOffiBtn_2.clicked.connect(self.edit_official)

        self.db = Database()
        self.resident_table.itemClicked.connect(self.on_resident_item_clicked)
        self.official_table.itemClicked.connect(self.on_official_item_clicked)
        self.complaint_table.itemClicked.connect(self.on_complaint_item_clicked)

    def updateDateTime(self):
        current = QDateTime.currentDateTime()
        formatted = current.toString("ddd, MMM d, h:mm AP")
        self.labelDateTime1.setText(formatted)
        self.labelDateTime2.setText(formatted)

#add dialogs
    def add_residents(self):
        dialog = AddResidentDialog(self, db=self.db)
        dialog.exec_()
        
    def add_complaints(self):
        dialog = AddComplaintDialog(self, db=self.db)
        dialog.exec_()

    def add_officials(self):
        dialog = AddOfficialDialog(self, db=self.db)
        dialog.exec_()

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

    def edit_resident(self):
        selected = self.resident_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Edit Resident", "Please select a resident to edit.")
            return
        resident_id = self.resident_table.item(selected, 0).text()
        db = self.db
        db.cursor.execute("SELECT * FROM residents WHERE resident_id = %s", (resident_id,))
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
            db.cursor.execute('''UPDATE residents SET first_name=%s, last_name=%s, age=%s, birth_date=%s, photo_cred=%s, address=%s, contact=%s, sex=%s WHERE resident_id=%s''', updated)
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
            db = self.db
            db.cursor.execute("DELETE FROM residents WHERE resident_id = %s", (resident_id,))
            db.conn.commit()
            self.load_residents()

    def load_residents(self):
        self.resident_table.setRowCount(0)
        for row_num, row_data in enumerate(self.db.get_elements()):
            birth_year = None
            try:
                birth_date = row_data[4]
                if birth_date:
                    birth_year = int(str(birth_date)[:4])
            except Exception:
                birth_year = None
            age = ""
            if birth_year:
                age = str(datetime.now().year - birth_year)
            self.db.update_resident_age(row_data[0], age)  # Update age based on birth date
            self.resident_table.insertRow(row_num)
            self.resident_table.setItem(row_num, 0, QTableWidgetItem(str(row_data[0])))  # ResidentID
            self.resident_table.setItem(row_num, 1, QTableWidgetItem(str(row_data[1])))  # FirstName
            self.resident_table.setItem(row_num, 2, QTableWidgetItem(str(row_data[2])))  # LastName
            self.resident_table.setItem(row_num, 3, QTableWidgetItem(str(row_data[3])))  # Age
            self.resident_table.setItem(row_num, 4, QTableWidgetItem(str(row_data[8])))  # Sex
            self.resident_table.setItem(row_num, 5, QTableWidgetItem(str(row_data[7])))  # Birthdate
            self.resident_table.setItem(row_num, 6, QTableWidgetItem(str(row_data[4])))  # Contact
            self.resident_table.setItem(row_num, 7, QTableWidgetItem(str(row_data[6])))  # Address
            self.resident_table.setItem(row_num, 8, QTableWidgetItem(str(row_data[5])))  # Credentials (photo_cred)
        
    def on_resident_item_clicked(self, item):
        row = item.row()
        col = item.column()
        value = item.text()
        row_values = [self.resident_table.item(row, c).text() for c in range(self.resident_table.columnCount())]
        print("Full row data:", row_values)
        dialog = InfoResidentDialog(self.db.get_element_by_id("residents", row_values[0]))
        dialog.display_info()
        dialog.exec_()  

    def edit_official(self):
        selected = self.official_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Edit Official", "Please select an official to edit.")
            return
        official_id = self.official_table.item(selected, 0).text()
        db = self.db 
        db.cursor.execute("SELECT * FROM barangay_officials WHERE official_id = %s", (official_id,))
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
            db = self.db
            db.cursor.execute("DELETE FROM BarangayOfficials WHERE official_id = %s", (official_id,))
            db.conn.commit()
            self.load_officials()

    def load_officials(self):
        db = self.db 
        self.official_table.setRowCount(0)
        for row_num, row_data in enumerate(db.get_elements(table="barangay_officials", column="last_name", order="ASC")):
            self.official_table.insertRow(row_num)
            self.official_table.setItem(row_num, 0, QTableWidgetItem(str(row_data[0])))  # OFFICIALID
            self.official_table.setItem(row_num, 1, QTableWidgetItem(str(row_data[4])))  # POSITION
            self.official_table.setItem(row_num, 2, QTableWidgetItem(str(row_data[1])))  # FIRSTNAME
            self.official_table.setItem(row_num, 3, QTableWidgetItem(str(row_data[2])))  # LASTNAME
            self.official_table.setItem(row_num, 4, QTableWidgetItem(str(row_data[3])))  # CONTACT

    def on_official_item_clicked(self, item):
        row = item.row()
        col = item.column()
        value = item.text()
        row_values = [self.official_table.item(row, c).text() for c in range(self.official_table.columnCount())]
        print("Full row data:", row_values)
        dialog = Ui_infoOfficialDialog(self.db.get_element_by_id("barangay_officials", row_values[0]))
        dialog.display_info()
        dialog.exec_()

    def edit_complaint(self):
        selected = self.complaint_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Edit Complaint", "Please select a complaint to edit.")
            return
        complaint_id = self.complaint_table.item(selected, 0).text()
        db = self.db
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

    def delete_complaint(self):
        selected = self.complaint_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Delete Complaint", "Please select a complaint to delete.")
            return
        complaint_id = self.complaint_table.item(selected, 0).text()
        reply = QMessageBox.question(self, "Delete Complaint", f"Delete complaint {complaint_id}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            db = self.db
            db.cursor.execute("DELETE FROM Complaint WHERE complaint_id = %s", (complaint_id,))
            db.conn.commit()
            self.load_complaints()

    def load_complaints(self):
        db = self.db  # Create a new Database instance
        self.complaint_table.setRowCount(0)
        for row_num, row_data in enumerate(db.get_elements(table="complaints", column="date_time", order="DESC")):
            self.complaint_table.insertRow(row_num)
            self.complaint_table.setItem(row_num, 0, QTableWidgetItem(str(row_data[0])))  # ComplaintID
            self.complaint_table.setItem(row_num, 1, QTableWidgetItem(str(row_data[3])))  # ResidentID
            self.complaint_table.setItem(row_num, 2, QTableWidgetItem(str(row_data[4])))  # Category
            self.complaint_table.setItem(row_num, 3, QTableWidgetItem(str(row_data[2])))  # Description
            self.complaint_table.setItem(row_num, 4, QTableWidgetItem(str(row_data[1])))  # DateTime
            self.complaint_table.setItem(row_num, 5, QTableWidgetItem(str(row_data[6])))  # Location
            self.complaint_table.setItem(row_num, 6, QTableWidgetItem(str(row_data[5])))  # Status
            

    def on_complaint_item_clicked(self, item):
        row = item.row()
        col = item.column()
        value = item.text()
        row_values = self.db.get_element_by_id("complaints", self.complaint_table.item(row, 0).text())
        print("Full row data:", row_values)
        dialog = InfoComplaintDialog(row_values)
        dialog.display_info()
        dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainClass()
    main.show()
    sys.exit(app.exec_())
