

from PyQt5.QtWidgets import QDialog  # or from PySide2.QtWidgets import QDialog, depending on your framework
from uipyfiles.infoofficialui import Ui_infoOfficialDialog  # adjust the import path as needed

class InfoOfficialDialog(QDialog, Ui_infoOfficialDialog):
    def __init__(self, official, db):
        super().__init__()
        self.setupUi(self)
        self.official = official
        self.inputEnabled(False)  
        self.db = db

        self.edit_mode = False
        self.saveOffiBtn.clicked.connect(self.saveButtonClicked)
        self.updOffiBtn.clicked.connect(self.editButtonClicked)

    def display_info(self):
        print(self.official)
        self.infoofficial_officialID_input.setText(self.official[0])
        self.infoofficial_firstname_input.setText(self.official[1])
        self.infoofficial_lastname_input.setText(self.official[2])
        self.infoofficial_contact_input.setText(self.official[3])
        self.infoofficial_position_input.setCurrentText(self.official[4])
        


    def inputEnabled(self, enabled):
        # Make input fields not editable
        self.infoofficial_officialID_input.setReadOnly(not enabled)
        self.infoofficial_firstname_input.setReadOnly(not enabled)
        self.infoofficial_lastname_input.setReadOnly(not enabled)
        self.infoofficial_contact_input.setReadOnly(not enabled)
        self.infoofficial_position_input.setEnabled(enabled)
        self.infoofficial_caseshandled_input.setReadOnly(not enabled)


    def saveButtonClicked(self):
        if self.edit_mode:
            self.edit_mode = False
            self.inputEnabled(False)

            # Change button color
            self.saveOffiBtn.setStyleSheet("background-color: rgb(230, 230, 230); color:black;")
            self.updOffiBtn.setStyleSheet("background-color: rgb(148, 255, 148); color: black;")
            self.delOffiBtn.setStyleSheet("background-color: rgb(255, 179, 179); color: black;")

            # Update Database with new official information
            updated_official = (
                self.infoofficial_officialID_input.text(),
                self.infoofficial_firstname_input.text(),
                self.infoofficial_lastname_input.text(),
                self.infoofficial_contact_input.text(),
                self.infoofficial_position_input.currentText()
            )
            self.db.update_barangay_official(updated_official)
            print(updated_official)
    def editButtonClicked(self):
        if not self.edit_mode:
            self.edit_mode = True
            self.inputEnabled(True)

            # Change button color
            self.saveOffiBtn.setStyleSheet("background-color: rgb(148, 255, 148); color: black;")
            self.updOffiBtn.setStyleSheet("background-color: rgb(230, 230, 230); color:black;")
            self.delOffiBtn.setStyleSheet("background-color: rgb(255, 179, 179); color: black;")

