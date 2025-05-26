

from PyQt5.QtWidgets import QDialog  # or from PySide2.QtWidgets import QDialog, depending on your framework
from uipyfiles.infoofficialui import Ui_infoOfficialDialog  # adjust the import path as needed
from database.database import Database

class InfoOfficialDialog(QDialog, Ui_infoOfficialDialog):
    def __init__(self, official, db=None):
        super().__init__()
        self.setupUi(self)
        self.official = official
        self.db = db


    def display_info(self):
        print(self.official)
        self.infoofficial_officialID_input.setText(self.official[0])
        self.infoofficial_firstname_input.setText(self.official[1])
        self.infoofficial_lastname_input.setText(self.official[2])
        self.infoofficial_contact_input.setText(self.official[3])
        self.infoofficial_position_input.setCurrentText(self.official[4])
        
        # Make input fields not editable
        self.infoofficial_officialID_input.setReadOnly(True)
        self.infoofficial_firstname_input.setReadOnly(True)
        self.infoofficial_lastname_input.setReadOnly(True)
        self.infoofficial_contact_input.setReadOnly(True)
        self.infoofficial_position_input.setEnabled(False)
        self.infoofficial_caseshandled_input.setReadOnly(True)