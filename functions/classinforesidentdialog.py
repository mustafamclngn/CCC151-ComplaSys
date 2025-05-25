from PyQt5.QtWidgets import QDialog
from uipyfiles.inforesidentui import Ui_infoResidentDialog
from PyQt5.QtCore import QDate

class InfoResidentDialog(QDialog, Ui_infoResidentDialog):
    def __init__(self, resident):
        super().__init__()
        self.setupUi(self)
        self.resident = resident

        # Make input fields not editable
        self.inforesident_residentID_input.setReadOnly(True)
        self.inforesident_firstname_input.setReadOnly(True)
        self.inforesident_lastname_input.setReadOnly(True)
        self.inforesident_age_input.setReadOnly(True)
        self.inforesident_dob_input.setReadOnly(True)
        self.inforesident_address_input.setReadOnly(True)
        self.inforesident_contact_input.setReadOnly(True)
        self.inforesident_sex_input.setEnabled(False)


    def display_info(self):
        self.inforesident_residentID_input.setText(self.resident[0])
        self.inforesident_firstname_input.setText(self.resident[1])
        self.inforesident_lastname_input.setText(self.resident[2])
        self.inforesident_age_input.setText(str(self.resident[3]))
        self.inforesident_dob_input.setDate(self.resident[4])
        self.inforesident_address_input.setText(self.resident[6])
        self.inforesident_contact_input.setText(self.resident[7])
        self.inforesident_sex_input.setCurrentText(self.resident[8])