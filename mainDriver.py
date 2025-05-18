import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5 import QtCore
from resources import resources_qrc
from addresidentui import Ui_addResidentDialog
from addcomplaintui import Ui_addComplaintDialog
from addofficialui import Ui_addOfficialDialog
from database.database import Database
from ComplaSys_ui import Ui_MainWindow

class AddComplaintDialog(QDialog, Ui_addComplaintDialog):
    def __init__(self, parent = None):
        super().__init__( parent)
        self.setupUi(self)
        self.db = Database()
        self.addcomplaint_save_button.clicked.connect(self.save_complaint)
        self.addcomplaint_cancel_button.clicked.connect(self.reject)
    
    def save_complaint(self):
        try:
            complaint_id = self.addcomplaint_complaintID_input.text()
            resident_id = self.addcomplaint_residentID_input.text()
            category = self.addcomplaint_category_box.currentText()
            date = self.addcomplaint_date_box.date().toString("yyyy-dd-MM")
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
        dialog = QDialog(self)
        ui = Ui_addResidentDialog()
        ui.setupUi(dialog)
        dialog.exec_()
        
    def add_complaints(self):
        dialog = QDialog(self)
        ui = Ui_addComplaintDialog()
        ui.setupUi(dialog)
        dialog.exec_()

    def add_officials(self):
        dialog = QDialog(self)
        ui = Ui_addOfficialDialog()
        ui.setupUi(dialog)
        dialog.exec_()

    def show_exit_message(self):
        reply = QMessageBox.question(self, 'Exit', 'Are you sure you want to exit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
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
