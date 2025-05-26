from PyQt5.QtWidgets import QDialog, QMessageBox
from uipyfiles.infocomplaintui import Ui_infoComplaintDialog
from database.database import printTime

class InfoComplaintDialog(QDialog, Ui_infoComplaintDialog):


    def __init__(self, complaint, db):
        super().__init__()
        self.setupUi(self)
        self.complaint = complaint
        self.db = db

        self.edit_mode = False
        self.saveCompBtn.clicked.connect(self.saveButtonClicked)
        self.updCompBtn.clicked.connect(self.editButtonClicked)
        self.delCompBtn.clicked.connect(self.deleteButtonClicked)


    def display_info(self):
        self.infocomplaint_complaintID_input.setText(self.complaint[0])
        self.infocomplaint_date_input.setDate(self.complaint[1])
        self.infocomplaint_description_input.setText(self.complaint[2])
        self.infocomplaint_residentID_input.setText(self.complaint[3])
        self.infocomplaint_category_input.setCurrentText(self.complaint[4])
        self.infocomplaint_status_input.setCurrentText(self.complaint[5])
        self.infocomplaint_location_input.setText(self.complaint[6])

        self.inputEnabled(False)

    def inputEnabled(self, enabled):
        # Make input fields editable
        self.infocomplaint_complaintID_input.setReadOnly(not enabled)
        self.infocomplaint_date_input.setEnabled(enabled)
        self.infocomplaint_description_input.setReadOnly(not enabled)
        self.infocomplaint_residentID_input.setEnabled(enabled)
        self.infocomplaint_category_input.setEnabled(enabled)
        self.infocomplaint_status_input.setEnabled(enabled)
        self.infocomplaint_location_input.setReadOnly(not enabled)
        self.infocomplaint_accuses_input.setReadOnly(not enabled)
        self.infocomplaint_handledby_input.setReadOnly(not enabled)

    def editButtonClicked(self):
        if not self.edit_mode:
            self.edit_mode = True
            self.inputEnabled(True)

            # Change button color
            self.saveCompBtn.setStyleSheet("background-color: rgb(148, 255, 148); color: black;")
            self.updCompBtn.setStyleSheet("background-color: rgb(230, 230, 230); color:black;")
            self.delCompBtn.setStyleSheet("background-color: rgb(230, 230, 230); color: black;")

    def saveButtonClicked(self):
        if self.edit_mode:
            self.edit_mode = False
            self.inputEnabled(False)

            # Change button color
            self.saveCompBtn.setStyleSheet("background-color: rgb(230, 230, 230); color:black;")
            self.updCompBtn.setStyleSheet("background-color: rgb(148, 255, 148); color: black;")
            self.delCompBtn.setStyleSheet("background-color: rgb(255, 179, 179); color: black;")

            # Update Database with new complaint information
            updated_complaint = (
                self.infocomplaint_complaintID_input.text(),
                self.infocomplaint_date_input.date().toPyDate(),
                self.infocomplaint_description_input.toPlainText(),
                self.infocomplaint_residentID_input.text(),
                self.infocomplaint_category_input.currentText(),
                self.infocomplaint_status_input.currentText(),
                self.infocomplaint_location_input.toPlainText(),
            )
            # Here you would typically call a method to update the database with updated_complaint
            self.db.update_complaint(updated_complaint)

    def deleteButtonClicked(self):
        if not self.edit_mode:
            reply = QMessageBox.question(
                self,
                "Confirm Deletion",
                '<span style="color:white;">Are you sure you want to delete this complaint?</span>',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            # Set the stylesheet to make the text white
            for widget in self.findChildren(QMessageBox):
                widget.setStyleSheet("QLabel{ color : white; }")

            if reply == QMessageBox.Yes:
                printTime("Deleting complaint from the database")
                self.db.remove_complaint(self.infocomplaint_complaintID_input.text())
                self.accept()