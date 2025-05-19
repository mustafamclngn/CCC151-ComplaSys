import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5 import QtCore
from resources import resources_qrc
from addresidentui import Ui_addResidentDialog
from addcomplaintui import Ui_addComplaintDialog
from addofficialui import Ui_addOfficialDialog
from database.database import Database
from ComplaSys_ui import Ui_MainWindow

class AddOfficialDialog(QDialog, Ui_addOfficialDialog):
    def __init__(self, parent = None, db = None):
        super().__init__(parent)
        self.setupUi(self)
        self.DB = db
        self.addofficial_save_button.clicked.connect(self.save_official)
        self.addofficial_cancel_button.clicked.connect(self.reject)

    def save_official(self):
        try:
            official_id = self.addofficial_officialID_input.text()
            first_name = self.addofficial_firstname_input.text()
            last_name = self.addofficial_lastname_input.text()
            contact = self.addofficial_contact_input.text()
            position = self.addofficial_position_box.currentText()

            official = (
                official_id,
                first_name,
                last_name,
                contact,
                position
            )

            sql = '''INSERT INTO barangay_officials
                (official_id, first_name, last_name, contact, position)
                VALUES (%s, %s, %s, %s, %s)'''
            self.DB.cursor.execute(sql, official)
            self.DB.conn.commit()
            QMessageBox.information(self, "Success", "Official added successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add official:\n{e}")
        
class AddResidentDialog(QDialog, Ui_addResidentDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.setupUi(self)
        self.DB = db
        self.addresident_save_button.clicked.connect(self.save_resident)
        self.addresident_cancel_button.clicked.connect(self.reject)
    
    def save_resident(self):
        try:
            resident_id = self.addresident_residentID_input.text()
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
                birth_date,
                age,
                photo_cred,
                address,
                contact,
                sex
            )

            sql = '''INSERT INTO residents
                (resident_id, first_name, last_name, birth_date, age, photo_cred, address, contact, sex)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            self.DB.cursor.execute(sql, resident)
            self.DB.conn.commit()
            QMessageBox.information(self, "Success", "Resident added successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add resident:\n{e}")



class AddComplaintDialog(QDialog, Ui_addComplaintDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.setupUi(self)
        self.DB = db
        self.addcomplaint_save_button.clicked.connect(self.save_complaint)
        self.addcomplaint_cancel_button.clicked.connect(self.reject)
    
    def save_complaint(self):
        try:
            complaint_id = self.addcomplaint_complaintID_input.text()
            resident_id = self.addcomplaint_residentID_input.text()
            category = self.addcomplaint_category_box.currentText()
            date = self.addcomplaint_date_box.date().toString("yyyy-MM-dd")
            description = self.addcomplaint_description_input.toPlainText()
            location = self.addcomplaint_location_input.text()
            status = self.addcomplaint_satus_box.currentText()
            
            complaint = (
                complaint_id,
                date,
                description,
                resident_id,
                category,
                status,
                location
            )
            sql = '''INSERT INTO complaints
                (complaint_id, date_time, complaint_desc, resident_id, complaint_category, complaint_status, location)
                VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            self.DB.cursor.execute(sql,complaint)
            self.DB.conn.commit()
            QMessageBox.information(self, "Success", "Complaint added successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add complaint:\n{e}")

            
class MainClass(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        try:
            self.DB = Database()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to connect to database:\n{e}")
        #Font
        font_id = QFontDatabase.addApplicationFont("resources/Gilroy-Medium.ttf")
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
        self.settBtn.clicked.connect(self.show_settings)
        self.abtBtn.clicked.connect(self.show_about)
        self.faqBtn.clicked.connect(self.show_faq)
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

    def updateDateTime(self):
        current = QDateTime.currentDateTime()
        formatted = current.toString("ddd, MMM d, h:mm AP")
        self.labelDateTime1.setText(formatted)
        self.labelDateTime2.setText(formatted)
        self.labelDateTime3.setText(formatted)
        self.labelDateTime4.setText(formatted)
        self.labelDateTime5.setText(formatted)
        self.labelDateTime6.setText(formatted)
        self.labelDateTime7.setText(formatted)

#add dialogs
    def add_residents(self):
        dialog = AddResidentDialog(self, db=self.DB)
        dialog.exec_()
        
    def add_complaints(self):
        dialog = AddComplaintDialog(self, db=self.DB)
        dialog.exec_()

    def add_officials(self):
        dialog = AddOfficialDialog(self, self.DB)
        dialog.exec_()

    def show_exit_message(self):
        reply = QMessageBox.question(self, 'Exit', 'Are you sure you want to exit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.DB.close_connection()
            self.close()
            
    def show_home(self):
        self.stackedWidget.setCurrentIndex(0)

    def show_residents(self):
        self.stackedWidget.setCurrentIndex(1)

    def show_complaints(self):
        self.stackedWidget.setCurrentIndex(2)

    def show_officials(self):
        self.stackedWidget.setCurrentIndex(3)

    def show_settings(self):
        self.stackedWidget.setCurrentIndex(4)

    def show_about(self):
        self.stackedWidget.setCurrentIndex(5)
    
    def show_faq(self):
        self.stackedWidget.setCurrentIndex(6)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainClass()
    main.show()
    sys.exit(app.exec_())
