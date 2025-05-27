import datetime
from PyQt5.QtWidgets import QDialog, QMessageBox
from uipyfiles.infocomplaintui import Ui_infoComplaintDialog
from database.database import printTime, warnMessageBox, infoMessageBox, errorMessageBox

class InfoComplaintDialog(QDialog, Ui_infoComplaintDialog):


    def __init__(self, complaint, db):
        super().__init__()
        self.setupUi(self)
        self.complaint = complaint
        self.db = db

        self.edit_mode = False

        # CONNECT EVENTS FOR BUTTONS
        self.saveCompBtn.clicked.connect(self.saveButtonClicked)
        self.updCompBtn.clicked.connect(self.editButtonClicked)
        self.delCompBtn.clicked.connect(self.deleteButtonClicked)
        self.infocomplaint_addID_button.clicked.connect(self.addIdButtonClicked)
        self.infocomplaint_deleteID_button.clicked.connect(self.deleteIdButtonClicked)

        self.infocomplaint_accuses_input.setReadOnly(True)
        self.infocomplaint_handledby_input.setReadOnly(True)

        self.infocomplaint_accusehandle_input.addItems(["Accuses", "Handles"])


    def display_info(self):
        self.infocomplaint_complaintID_input.setText(self.complaint[0])
        self.infocomplaint_date_input.setDate(self.complaint[1])
        self.infocomplaint_description_input.setText(self.complaint[2])
        self.infocomplaint_residentID_input.setText(self.complaint[3])
        self.infocomplaint_category_input.setCurrentText(self.complaint[4])
        self.infocomplaint_status_input.setCurrentText(self.complaint[5])
        self.infocomplaint_location_input.setText(self.complaint[6])

        self.inputEnabled(False)
        self.displayRelationships()

    def inputEnabled(self, enabled):
        # Make input fields editable
        self.infocomplaint_complaintID_input.setReadOnly(not enabled)
        self.infocomplaint_date_input.setEnabled(enabled)
        self.infocomplaint_description_input.setReadOnly(not enabled)
        self.infocomplaint_residentID_input.setEnabled(enabled)
        self.infocomplaint_category_input.setEnabled(enabled)
        self.infocomplaint_status_input.setEnabled(enabled)
        self.infocomplaint_location_input.setReadOnly(not enabled)
        self.infocomplaint_accusehandle_input.setEnabled(enabled)
        self.infocomplaint_accusehandleID_input.setEnabled(enabled)

        if enabled:
            self.infocomplaint_addID_button.setStyleSheet("color: black;")
            self.infocomplaint_deleteID_button.setStyleSheet("color: black;")
        elif not enabled:
            self.infocomplaint_addID_button.setStyleSheet("color: rgb(130, 130, 130);")
            self.infocomplaint_deleteID_button.setStyleSheet("color: rgb(130, 130, 130);")
        

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


    def addIdButtonClicked(self):
        if self.edit_mode:
            id = self.infocomplaint_accusehandleID_input.text()
            myTuple = (id, self.infocomplaint_complaintID_input.text())
            if self.infocomplaint_accusehandle_input.currentText() == "Accuses":

                if self.db.check_unique_id('residents', id): # ID must exist in the residents table
                    errorMessageBox(self, "Error", f"ID [{id}:{myTuple[1]}] does not exist in the database.")
                    return
                
                if not self.db.check_unique_accuse(myTuple): # ID must not already be an accuser for this complaint
                    errorMessageBox(self, "Error", f"ID [{id}:{myTuple[1]}] is already an accuser for this complaint.")
                    return
                self.db.insert_accuse(myTuple)
                infoMessageBox(self, "Success", f"ID [{id}:{myTuple[1]}] has been added as an accuser for this complaint.")
            elif self.infocomplaint_accusehandle_input.currentText() == "Handles":
                if self.db.check_unique_id('barangay_officials', id): # ID must exist in the officials table
                    errorMessageBox(self, "Error", f"ID [{id}:{myTuple[1]}] does not exist in the database.")
                    return
                
                if not self.db.check_unique_handle(myTuple): # ID must not already be an handler for this complaint
                    errorMessageBox(self, "Error", f"ID [{id}:{myTuple[1]}] is already an accuser for this complaint.")
                    return
                self.db.insert_handle((id, self.infocomplaint_complaintID_input.text(), datetime.datetime.now()))
                infoMessageBox(self, "Success", f"ID [{id}:{myTuple[1]}] has been added as a handler for this complaint.")
            self.infocomplaint_accusehandleID_input.clear()
            self.displayRelationships()
                    

    def deleteIdButtonClicked(self):
        if self.edit_mode:
            id = self.infocomplaint_accusehandleID_input.text()
            myTuple = (id, self.infocomplaint_complaintID_input.text())
            if self.infocomplaint_accusehandle_input.currentText() == "Accuses":
                if self.db.check_unique_accuse(myTuple): # ID must already be an accuser for this complaint
                    errorMessageBox(self, "Error", f"ID [{id}:{myTuple[1]}] is not an accuser for this complaint.")
                    return

                self.db.remove_accuse(myTuple)
                infoMessageBox(self, "Success", f"ID [{id}:{myTuple[1]}] has been removed as an accuser for this complaint.")
            elif self.infocomplaint_accusehandle_input.currentText() == "Handles":
                
                if self.db.check_unique_handle(myTuple): # ID must already be a handler for this complaint
                    errorMessageBox(self, "Error", f"ID [{id}:{myTuple[1]}] is not a handler for this complaint.")
                    return

                self.db.remove_handle(myTuple)
                infoMessageBox(self, "Success", f"ID [{id}:{myTuple[1]}] has been removed as a handler for this complaint.")
            self.infocomplaint_accusehandleID_input.clear()
            self.displayRelationships()


    def displayRelationships(self):
        self.displayAccuses()
        self.displayHandles()

    def displayAccuses(self):
        accuses = self.db.get_accuses_elements(self.infocomplaint_complaintID_input.text())
        self.infocomplaint_accuses_input.clear()
        for accused in accuses:
            print(accused)
            resident = self.db.get_element_by_id('residents', accused[0])
            self.infocomplaint_accuses_input.append(f"[{resident[0]}]  " + resident[1] + ' ' + resident[2])

    def displayHandles(self):
        handles = self.db.get_handles_elements(self.infocomplaint_complaintID_input.text())
        self.infocomplaint_handledby_input.clear()
        for handler in handles:
            official = self.db.get_element_by_id('barangay_officials', handler[0])
            self.infocomplaint_handledby_input.append(f"[{official[0]}]  " + official[1] + ' ' + official[2])