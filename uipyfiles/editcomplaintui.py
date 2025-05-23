# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editcomplaintui.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_editComplaintDialog(object):
    def setupUi(self, editComplaintDialog):
        editComplaintDialog.setObjectName("editComplaintDialog")
        editComplaintDialog.resize(458, 732)
        editComplaintDialog.setStyleSheet("background-color: rgb(0, 0, 25);")
        self.frame = QtWidgets.QFrame(editComplaintDialog)
        self.frame.setGeometry(QtCore.QRect(20, 20, 421, 691))
        self.frame.setStyleSheet("background-color: rgb(0, 0, 50);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(10, 10, 401, 631))
        self.frame_2.setStyleSheet("background-color: white;\n"
"border: 1px solid grey;\n"
"border-radius: 13px;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_resident_id = QtWidgets.QLabel(self.frame_2)
        self.label_resident_id.setGeometry(QtCore.QRect(21, 10, 124, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_resident_id.setFont(font)
        self.label_resident_id.setStyleSheet("border: 0px")
        self.label_resident_id.setObjectName("label_resident_id")
        self.editcomplaint_complaintID_input = QtWidgets.QLineEdit(self.frame_2)
        self.editcomplaint_complaintID_input.setGeometry(QtCore.QRect(21, 40, 361, 28))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.editcomplaint_complaintID_input.setFont(font)
        self.editcomplaint_complaintID_input.setStyleSheet("background-color: white;\n"
"border: 1px solid grey;\n"
"border-radius: 0px;")
        self.editcomplaint_complaintID_input.setObjectName("editcomplaint_complaintID_input")
        self.label_first_name = QtWidgets.QLabel(self.frame_2)
        self.label_first_name.setGeometry(QtCore.QRect(21, 70, 111, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_first_name.setFont(font)
        self.label_first_name.setStyleSheet("border: 0px")
        self.label_first_name.setObjectName("label_first_name")
        self.label_dob = QtWidgets.QLabel(self.frame_2)
        self.label_dob.setGeometry(QtCore.QRect(21, 350, 50, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_dob.setFont(font)
        self.label_dob.setStyleSheet("border: 0px")
        self.label_dob.setObjectName("label_dob")
        self.label_address = QtWidgets.QLabel(self.frame_2)
        self.label_address.setGeometry(QtCore.QRect(21, 410, 82, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_address.setFont(font)
        self.label_address.setStyleSheet("border: 0px")
        self.label_address.setObjectName("label_address")
        self.editcomplaint_category_input = QtWidgets.QComboBox(self.frame_2)
        self.editcomplaint_category_input.setGeometry(QtCore.QRect(21, 160, 361, 28))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.editcomplaint_category_input.setFont(font)
        self.editcomplaint_category_input.setStyleSheet("background-color: white;\n"
"border: 1px solid grey;\n"
"border-radius: 0px;")
        self.editcomplaint_category_input.setObjectName("editcomplaint_category_input")
        self.editcomplaint_category_input.addItem("")
        self.editcomplaint_category_input.addItem("")
        self.editcomplaint_category_input.addItem("")
        self.editcomplaint_category_input.addItem("")
        self.editcomplaint_category_input.addItem("")
        self.editcomplaint_category_input.addItem("")
        self.editcomplaint_category_input.addItem("")
        self.editcomplaint_category_input.addItem("")
        self.label_first_name_2 = QtWidgets.QLabel(self.frame_2)
        self.label_first_name_2.setGeometry(QtCore.QRect(21, 130, 87, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_first_name_2.setFont(font)
        self.label_first_name_2.setStyleSheet("border: 0px")
        self.label_first_name_2.setObjectName("label_first_name_2")
        self.label_first_name_3 = QtWidgets.QLabel(self.frame_2)
        self.label_first_name_3.setGeometry(QtCore.QRect(21, 560, 63, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_first_name_3.setFont(font)
        self.label_first_name_3.setStyleSheet("border: 0px")
        self.label_first_name_3.setObjectName("label_first_name_3")
        self.editcomplaint_status_input = QtWidgets.QComboBox(self.frame_2)
        self.editcomplaint_status_input.setGeometry(QtCore.QRect(20, 590, 361, 28))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.editcomplaint_status_input.setFont(font)
        self.editcomplaint_status_input.setStyleSheet("background-color: white;\n"
"border: 1px solid grey;\n"
"border-radius: 0px;")
        self.editcomplaint_status_input.setObjectName("editcomplaint_status_input")
        self.editcomplaint_status_input.addItem("")
        self.editcomplaint_status_input.addItem("")
        self.editcomplaint_status_input.addItem("")
        self.label_address_2 = QtWidgets.QLabel(self.frame_2)
        self.label_address_2.setGeometry(QtCore.QRect(21, 190, 107, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_address_2.setFont(font)
        self.label_address_2.setStyleSheet("border: 0px")
        self.label_address_2.setObjectName("label_address_2")
        self.editcomplaint_location_input = QtWidgets.QLineEdit(self.frame_2)
        self.editcomplaint_location_input.setGeometry(QtCore.QRect(21, 440, 361, 121))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.editcomplaint_location_input.setFont(font)
        self.editcomplaint_location_input.setStyleSheet("background-color: white;\n"
"border: 1px solid grey;\n"
"border-radius: 0px;")
        self.editcomplaint_location_input.setObjectName("editcomplaint_location_input")
        self.editcomplaint_description_input = QtWidgets.QLineEdit(self.frame_2)
        self.editcomplaint_description_input.setGeometry(QtCore.QRect(21, 220, 361, 131))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.editcomplaint_description_input.setFont(font)
        self.editcomplaint_description_input.setStyleSheet("background-color: white;\n"
"border: 1px solid grey;\n"
"border-radius: 0px;")
        self.editcomplaint_description_input.setObjectName("editcomplaint_description_input")
        self.editcomplaint_date_input = QtWidgets.QDateEdit(self.frame_2)
        self.editcomplaint_date_input.setGeometry(QtCore.QRect(21, 380, 361, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.editcomplaint_date_input.setFont(font)
        self.editcomplaint_date_input.setStyleSheet("background-color: white;\n"
"border: 1px solid grey;\n"
"border-radius: 0px;")
        self.editcomplaint_date_input.setCalendarPopup(True)
        self.editcomplaint_date_input.setObjectName("editcomplaint_date_input")
        self.editcomplaint_residentID_input = QtWidgets.QComboBox(self.frame_2)
        self.editcomplaint_residentID_input.setGeometry(QtCore.QRect(20, 100, 361, 28))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.editcomplaint_residentID_input.setFont(font)
        self.editcomplaint_residentID_input.setStyleSheet("background-color: white;\n"
"border: 1px solid grey;\n"
"border-radius: 0px;")
        self.editcomplaint_residentID_input.setObjectName("editcomplaint_residentID_input")
        self.editcomplaint_save_button = QtWidgets.QPushButton(self.frame)
        self.editcomplaint_save_button.setGeometry(QtCore.QRect(90, 650, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.editcomplaint_save_button.setFont(font)
        self.editcomplaint_save_button.setStyleSheet("background-color: white;\n"
"border-radius: 13px;")
        self.editcomplaint_save_button.setObjectName("editcomplaint_save_button")
        self.editcomplaint_cancel_button = QtWidgets.QPushButton(self.frame)
        self.editcomplaint_cancel_button.setGeometry(QtCore.QRect(240, 650, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.editcomplaint_cancel_button.setFont(font)
        self.editcomplaint_cancel_button.setStyleSheet("background-color: white;\n"
"border-radius: 13px;")
        self.editcomplaint_cancel_button.setObjectName("editcomplaint_cancel_button")

        self.retranslateUi(editComplaintDialog)
        QtCore.QMetaObject.connectSlotsByName(editComplaintDialog)

    def retranslateUi(self, editComplaintDialog):
        _translate = QtCore.QCoreApplication.translate
        editComplaintDialog.setWindowTitle(_translate("editComplaintDialog", "Edit Complaint"))
        self.label_resident_id.setText(_translate("editComplaintDialog", "Complaint ID:"))
        self.label_first_name.setText(_translate("editComplaintDialog", "Resident ID:"))
        self.label_dob.setText(_translate("editComplaintDialog", "Date:"))
        self.label_address.setText(_translate("editComplaintDialog", "Location:"))
        self.editcomplaint_category_input.setItemText(0, _translate("editComplaintDialog", "Domestic Issues"))
        self.editcomplaint_category_input.setItemText(1, _translate("editComplaintDialog", "Community Disputes"))
        self.editcomplaint_category_input.setItemText(2, _translate("editComplaintDialog", "Public Disturbance"))
        self.editcomplaint_category_input.setItemText(3, _translate("editComplaintDialog", "Business and Livelihood Issues"))
        self.editcomplaint_category_input.setItemText(4, _translate("editComplaintDialog", "Environmental Concerns"))
        self.editcomplaint_category_input.setItemText(5, _translate("editComplaintDialog", "Traffic and Road Issues"))
        self.editcomplaint_category_input.setItemText(6, _translate("editComplaintDialog", "Criminal Activities"))
        self.editcomplaint_category_input.setItemText(7, _translate("editComplaintDialog", "Barangay Ordinance Violations"))
        self.label_first_name_2.setText(_translate("editComplaintDialog", "Category:"))
        self.label_first_name_3.setText(_translate("editComplaintDialog", "Status:"))
        self.editcomplaint_status_input.setItemText(0, _translate("editComplaintDialog", "Pending"))
        self.editcomplaint_status_input.setItemText(1, _translate("editComplaintDialog", "Completed"))
        self.editcomplaint_status_input.setItemText(2, _translate("editComplaintDialog", "Cancelled"))
        self.label_address_2.setText(_translate("editComplaintDialog", "Description:"))
        self.editcomplaint_save_button.setText(_translate("editComplaintDialog", "Edit"))
        self.editcomplaint_cancel_button.setText(_translate("editComplaintDialog", "Cancel"))
