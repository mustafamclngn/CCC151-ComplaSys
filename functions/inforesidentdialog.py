import shutil
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from uipyfiles.inforesidentui import Ui_infoResidentDialog
from PyQt5.QtCore import QDate
from database.database import printTime, warnMessageBox, infoMessageBox, errorMessageBox
import os

from utils import all_fields_filled

class InfoResidentDialog(QDialog, Ui_infoResidentDialog):
    def __init__(self, resident, db):
        super().__init__()
        self.setupUi(self)
        self.resident = resident
        self.old_res_id = resident[0]  # Store the original resident ID for updates
        self.db = db
        self.edit_mode = False
        self.inputEnabled(False)  

        self.inforesident_age_input.setEnabled(False)

        self.saveResBtn.clicked.connect(self.saveButtonClicked)
        self.updResBtn.clicked.connect(self.editButtonClicked)
        self.delResBtn.clicked.connect(self.deleteButtonClicked)
        self.inforesident_view_button.clicked.connect(self.view_photo)
        self.inforesident_upload_button.clicked.connect(self.uploadPhotoButtonClicked)

        self.display_info()

    def updateResident(self):
        self.resident = self.db.get_element_by_id('residents', self.inforesident_residentID_input.text())

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
        self.inforesident_residentID_input.setReadOnly(True)
        self.inforesident_firstname_input.setReadOnly(not enabled)
        self.inforesident_lastname_input.setReadOnly(not enabled)
        self.inforesident_dob_input.setReadOnly(not enabled)
        self.inforesident_address_input.setReadOnly(not enabled)
        self.inforesident_contact_input.setReadOnly(not enabled)
        self.inforesident_sex_input.setEnabled(enabled)

    def saveButtonClicked(self):
        if self.edit_mode:
            self.edit_mode = False
            self.inputEnabled(False)

            # Check if resident still exists
            resident = self.db.get_element_by_id('residents', self.inforesident_residentID_input.text())
            if resident is None:
                warnMessageBox(self, "Error", "Resident not found in database. It may have been deleted.")
                return

            self.file_path = self.inforesident_photo_label.text() # New photo path
            old_photo_path = self.db.get_element_by_id('residents', self.old_res_id)[5]
            if self.file_path != old_photo_path:
                local_dir = os.path.join('.', 'photos')
                if not os.path.exists(local_dir):
                    os.makedirs(local_dir)

                ext = os.path.splitext(self.file_path)[1]
                self.photo_path = os.path.join(local_dir, self.inforesident_residentID_input.text() + ext)

                if self.photo_path != self.file_path:
                    try:
                        shutil.copy(self.file_path, self.photo_path)
                        # Only remove the old photo if it exists and is different from the new photo
                        if old_photo_path and os.path.isfile(old_photo_path) and old_photo_path != self.photo_path:
                            os.remove(old_photo_path)  # Remove old photo file
                        self.inforesident_photo_label.setText(self.photo_path)
                    except Exception as e:
                        errorMessageBox(self, "File Error", f"Failed to copy photo file: {e}")
                        return
            # fields to validate if present or not
            fields = [
                self.inforesident_residentID_input,
                self.inforesident_firstname_input,
                self.inforesident_lastname_input,
                self.inforesident_dob_input,
                self.inforesident_photo_label,
                self.inforesident_address_input,
                self.inforesident_contact_input,
                self.inforesident_sex_input
            ]
            if not all_fields_filled(fields):
                warnMessageBox(self, "Input Error", "Please fill in all required fields.")
                return

            # Change button color
            self.saveResBtn.setStyleSheet("background-color: rgb(230, 230, 230); color:black;")
            self.updResBtn.setStyleSheet("background-color: rgb(255, 217, 148); color: black;")
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
            for i in updated_resident:
                if i == "":
                    errorMessageBox(self, "Empty Field", "Please fill in all fields.")
                    self.editButtonClicked()
                    return
            if not self.db.check_unique_id('residents', self.inforesident_residentID_input.text()) and self.inforesident_residentID_input.text() != self.old_res_id:
                errorMessageBox(self, "Duplicate Resident ID", "The resident ID already exists. Please use a different ID.")
                return
            printTime("Updating resident information in the database")
            self.db.update_resident(self.old_res_id, updated_resident)
            self.display_info()
            self.accept()


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
            if self.db.check_if_resident_accused(self.resident[0]):
                reply = QMessageBox.question(
                    self,
                    "Confirm Deletion",
                    '<span style="color:black;">This resident is being accused currently, are you sure?</span>',
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                if reply == QMessageBox.No:
                    return

            reply = QMessageBox.question(
                self,
                "Confirm Deletion",
                '<span style="color:black;">Are you sure you want to delete this resident?</span>',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

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

