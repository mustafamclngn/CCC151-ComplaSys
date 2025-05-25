from PyQt5.QtWidgets import QDialog
from uipyfiles.infocomplaintui import Ui_infoComplaintDialog

class InfoComplaintDialog(QDialog, Ui_infoComplaintDialog):


    def __init__(self, complaint):
        super().__init__()
        self.setupUi(self)
        self.complaint = complaint

    def display_info(self):
        self.infocomplaint_complaintID_input.setText(self.complaint[0])
        self.infocomplaint_date_input.setDate(self.complaint[1])
        self.infocomplaint_description_input.setText(self.complaint[2])
        self.infocomplaint_residentID_input.setCurrentText(self.complaint[3])
        self.infocomplaint_category_input.setCurrentText(self.complaint[4])
        self.infocomplaint_status_input.setCurrentText(self.complaint[5])
        self.infocomplaint_location_input.setText(self.complaint[6])

        # Make input fields not editable
        self.infocomplaint_complaintID_input.setReadOnly(True)
        self.infocomplaint_date_input.setEnabled(False)
        self.infocomplaint_description_input.setReadOnly(True)
        self.infocomplaint_residentID_input.setEnabled(False)
        self.infocomplaint_category_input.setEnabled(False)
        self.infocomplaint_status_input.setEnabled(False)
        self.infocomplaint_location_input.setReadOnly(True)
        self.infocomplaint_accuses_input.setReadOnly(True)
        self.infocomplaint_handledby_input.setReadOnly(True)
