import shutil
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from uipyfiles.inforesidentui import Ui_infoResidentDialog
from PyQt5.QtCore import QDate
from database.database import printTime, warnMessageBox, infoMessageBox, errorMessageBox
import os

class InfoResidentDialog(QDialog, Ui_infoResidentDialog):
    def __init__(self, resident, db):
        super().__init__()
        self.setupUi(self)
        self.resident = resident
        self.db = db
        self.edit_mode = False
        self.inputEnabled(False)  


        self.saveResBtn.clicked.connect(self.saveButtonClicked)
        self.updResBtn.clicked.connect(self.editButtonClicked)
        self.delResBtn.clicked.connect(self.deleteButtonClicked)
        self.inforesident_view_button.clicked.connect(self.view_photo)
        self.inforesident_upload_button.clicked.connect(self.uploadPhotoButtonClicked)


    def display_info(self):
        self.inforesident_residentID_input.setText(self.resident[0])
        self.inforesident_firstname_input.setText(self.resident[1])
        self.inforesident_lastname_input.setText(self.resident[2])
        self.inforesident_age_input.setText(str(self.resident[3]))
        self.inforesident_dob_input.setDate(self.resident[4])
        self.inforesident_photo_label.setText(self.resident[5]) 
        self.inforesident_address_input.setText(self.resident[6])
        self.inforesident_contact_input.setText(self.resident[7])
        self.inforesident_sex_input.setCurrentText(self.resident[8])

    def inputEnabled(self, enabled):
        # Make input fields not editable
        self.inforesident_residentID_input.setReadOnly(not enabled)
        self.inforesident_firstname_input.setReadOnly(not enabled)
        self.inforesident_lastname_input.setReadOnly(not enabled)
        self.inforesident_age_input.setReadOnly(not enabled)
        self.inforesident_dob_input.setReadOnly(not enabled)
        self.inforesident_address_input.setReadOnly(not enabled)
        self.inforesident_contact_input.setReadOnly(not enabled)
        self.inforesident_sex_input.setEnabled(enabled)

    def saveButtonClicked(self):
        if self.edit_mode:
            self.edit_mode = False
            self.inputEnabled(False)

            self.file_path = self.inforesident_photo_label.text()
            if self.file_path != self.db.get_element_by_id('residents', self.inforesident_residentID_input.text())[5]:
                local_dir = os.path.join('.', 'photos')
                if not os.path.exists(local_dir):
                    os.makedirs(local_dir)

                ext = os.path.splitext(self.file_path)[1]
                self.photo_path = os.path.join(local_dir, self.inforesident_residentID_input.text() + ext)

                if self.photo_path != self.file_path:
                    shutil.copy(self.file_path, self.photo_path)
                    os.remove(self.db.get_element_by_id('residents', self.inforesident_residentID_input.text())[5])  # Remove old photo file
                    self.inforesident_photo_label.setText(self.photo_path)


            # Change button color
            self.saveResBtn.setStyleSheet("background-color: rgb(230, 230, 230); color:black;")
            self.updResBtn.setStyleSheet("background-color: rgb(148, 255, 148); color: black;")
            self.delResBtn.setStyleSheet("background-color: rgb(255, 179, 179); color: black;")

            # Update Database with new resident information
            updated_resident = (
                self.inforesident_residentID_input.text(),
                self.inforesident_firstname_input.text(),
                self.inforesident_lastname_input.text(),
                self.inforesident_dob_input.date().toPyDate(),
                self.inforesident_photo_label.text(),
                self.inforesident_address_input.toPlainText(),
                self.inforesident_contact_input.text(),
                self.inforesident_sex_input.currentText()
            )
            printTime("Updating resident information in the database")
            self.db.update_resident(updated_resident)

    def editButtonClicked(self):
        if not self.edit_mode:
            self.edit_mode = True
            self.inputEnabled(True)

            # Change button color
            self.saveResBtn.setStyleSheet("background-color: rgb(148, 255, 148); color: black;")
            self.updResBtn.setStyleSheet("background-color: rgb(230, 230, 230); color:black;")
            self.delResBtn.setStyleSheet("background-color: rgb(230, 230, 230); color:black;")


    def deleteButtonClicked(self):
        if not self.edit_mode:
            reply = QMessageBox.question(
                self,
                "Confirm Deletion",
                '<span style="color:white;">Are you sure you want to delete this resident?</span>',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            # Set the stylesheet to make the text white
            for widget in self.findChildren(QMessageBox):
                widget.setStyleSheet("QLabel{ color : white; }")

            if reply == QMessageBox.Yes:

                # Delete the resident's photo file if it exists
                photo_path = self.resident[5]
                if photo_path and os.path.isfile(photo_path):
                    try:
                        os.remove(photo_path)
                        printTime(f"Deleted photo file: {photo_path}")
                    except Exception as e:
                        printTime(f"Failed to delete photo file: {photo_path}. Error: {e}")

                printTime("Deleting resident from the database")
                self.db.remove_resident(self.resident[0])
                printTime("Resident deleted successfully")
                self.accept()

    def uploadPhotoButtonClicked(self):
        if self.edit_mode:
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
                self.inforesident_photo_label.setText(file_path)
                self.file_path = file_path
            else:
                warnMessageBox(self, "No File Selected", "Please select a photo file.")

    def view_photo(self):
        file_path = self.inforesident_photo_label.text()
        if os.path.isfile(file_path):
            os.startfile(file_path)
        else:
            QMessageBox.warning(self, "File Not Found", "The photo file does not exist.")

