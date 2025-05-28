

from PyQt5.QtWidgets import QDialog, QMessageBox  
from uipyfiles.infoofficialui import Ui_infoOfficialDialog  # adjust the import path as needed
from database.database import printTime, warnMessageBox, infoMessageBox, errorMessageBox

class InfoOfficialDialog(QDialog, Ui_infoOfficialDialog):
    def __init__(self, official, db):
        super().__init__()
        self.setupUi(self)
        self.official = official
        self.old_official_id = official[0]  # Store the original official ID for updates
        self.inputEnabled(False)  
        self.db = db

        self.edit_mode = False
        self.saveOffiBtn.clicked.connect(self.saveButtonClicked)
        self.updOffiBtn.clicked.connect(self.editButtonClicked)
        self.delOffiBtn.clicked.connect(self.deleteButtonClicked)

        self.infoofficial_caseshandled_input.setPlaceholderText("None")

    def display_info(self):
        self.infoofficial_officialID_input.setText(self.official[0])
        self.infoofficial_firstname_input.setText(self.official[1])
        self.infoofficial_lastname_input.setText(self.official[2])
        self.infoofficial_contact_input.setText(self.official[3])
        self.infoofficial_position_input.setCurrentText(self.official[4])
        self.displayHandles()
        


    def inputEnabled(self, enabled):
        # Make input fields not editable
        self.infoofficial_officialID_input.setReadOnly(True)
        self.infoofficial_firstname_input.setReadOnly(not enabled)
        self.infoofficial_lastname_input.setReadOnly(not enabled)
        self.infoofficial_contact_input.setReadOnly(not enabled)
        self.infoofficial_position_input.setEnabled(enabled)
        self.infoofficial_caseshandled_input.setReadOnly(True)


    def saveButtonClicked(self):
        if self.edit_mode:
            self.edit_mode = False
            self.inputEnabled(False)

            # Change button color
            self.saveOffiBtn.setStyleSheet("background-color: rgb(230, 230, 230); color:black;")
            self.updOffiBtn.setStyleSheet("background-color: rgb(255, 217, 148); color: black;")
            self.delOffiBtn.setStyleSheet("background-color: rgb(255, 179, 179); color: black;")

            # Update Database with new official information
            updated_official = (
                self.infoofficial_officialID_input.text(),
                self.infoofficial_firstname_input.text(),
                self.infoofficial_lastname_input.text(),
                self.infoofficial_contact_input.text(),
                self.infoofficial_position_input.currentText()
            )
            for i in updated_official:
                if not i.strip():
                    warnMessageBox(self, "Empty Field", "Please fill in all fields.")
                    self.editButtonClicked()
                    return
            if not self.db.check_unique_id('barangay_officials', self.infoofficial_officialID_input.text()) and self.infoofficial_officialID_input.text() != self.old_official_id:
                errorMessageBox(self, "Duplicate Official ID", "The official ID already exists. Please use a different ID.")
                return
            self.db.update_barangay_official(self.old_official_id, updated_official)
            self.accept()
    def editButtonClicked(self):
        if not self.edit_mode:
            self.edit_mode = True
            self.inputEnabled(True)

            # Change button color
            self.saveOffiBtn.setStyleSheet("background-color: rgb(148, 255, 148); color: black;")
            self.updOffiBtn.setStyleSheet("background-color: rgb(230, 230, 230); color:black;")
            self.delOffiBtn.setStyleSheet("background-color: rgb(230, 230, 230); color: black;")

    def deleteButtonClicked(self):
        if not self.edit_mode:
            reply = QMessageBox.question(
                self,
                "Confirm Deletion",
                '<span style="color:black;">Are you sure you want to delete this complaint?</span>',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.db.remove_barangay_official(self.infoofficial_officialID_input.text())
                self.accept()

    def displayHandles(self):
        handles = self.db.get_handles_elements(attribute='barangay_official_id', id=self.infoofficial_officialID_input.text())
        self.infoofficial_caseshandled_input.clear()
        for handler in handles:
            complaint = self.db.get_element_by_id('complaints', handler[1])
            self.infoofficial_caseshandled_input.append(f"[{complaint[0]}]  {complaint[2][:25]}")