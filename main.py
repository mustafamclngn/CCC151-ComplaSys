import sys

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5 import QtCore

from database.database import Database, printTime, warnMessageBox, infoMessageBox, errorMessageBox
from resource import resource_qrc

from uipyfiles.inforesidentui import Ui_infoResidentDialog
from uipyfiles.infocomplaintui import Ui_infoComplaintDialog
from uipyfiles.infoofficialui import Ui_infoOfficialDialog
from uipyfiles.mainui import Ui_MainWindow
from uipyfiles.addcomplaintui import Ui_addComplaintDialog
from uipyfiles.addresidentui import Ui_addResidentDialog
from uipyfiles.addofficialui import Ui_addOfficialDialog

from functions.classcomplaint import AddComplaintDialog
from functions.classofficial import AddOfficialDialog
from functions.classresident import AddResidentDialog
from functions.inforesidentdialog import InfoResidentDialog
from functions.infocomplaintdialog import InfoComplaintDialog
from functions.infoofficialdialog import InfoOfficialDialog
from datetime import datetime

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
            
class MainClass(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # setup and layout
        if self.chart_frame.layout() is None:
            self.chart_frame.setLayout(QVBoxLayout())

        # combo box from month choice
        self.monthFilterBox = QComboBox(self.chart_frame)
        self.monthFilterBox.addItem("All Months")
        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        self.monthFilterBox.addItems(months)
        self.chart_frame.layout().addWidget(self.monthFilterBox)

        # connect choice to chart
        self.monthFilterBox.currentIndexChanged.connect(self.plot_complaint_pie_chart)

        #Font
        font_id = QFontDatabase.addApplicationFont("resource/Gilroy-Medium.ttf")
        if font_id == -1:
            print("Failed to load font.")
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            custom_font = QFont(font_family, 12)
            app.setFont(custom_font)

        #Automatic on dashboard button when load
        QTimer.singleShot(0, self.homeBtn.click)
        self.homeBtn.clicked.connect(self.show_home)
        self.resBtn.clicked.connect(self.show_residents)
        self.compBtn.clicked.connect(self.show_complaints)
        self.offiBtn.clicked.connect(self.show_officials)
        self.exBtn.clicked.connect(self.show_exit_message)

        #add dialogs (to be changed)
        self.addResBtn.clicked.connect(self.add_residents)
        self.addCompBtn.clicked.connect(self.add_complaints)
        self.addOffiBtn.clicked.connect(self.add_officials)
        
        #Datettime
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)
        self.updateDateTime()
        
        #Refresh Button
        self.refreshResBtn.clicked.connect(self.load_residents)
        self.refreshResBtn_2.clicked.connect(self.load_residents)
        self.refreshOffiBtn.clicked.connect(self.load_officials)
        self.refreshOffiBtn_2.clicked.connect(self.load_officials)
        self.refreshCompBtn.clicked.connect(self.load_complaints)
        self.refreshCompBtn_2.clicked.connect(self.load_complaints)

        self.db = Database()
        self.resident_table.itemClicked.connect(self.on_resident_item_clicked)
        self.official_table.itemClicked.connect(self.on_official_item_clicked)
        self.complaint_table.itemClicked.connect(self.on_complaint_item_clicked)
        self.pendingComp_table.itemClicked.connect(self.onDashboardBtnClicked)
        self.sortCases_box.currentIndexChanged.connect(self.updateDashboardCases)

        #Pagination States
        self.res_page = 1
        self.comp_page = 1
        self.offi_page = 1
        self.rows_per_page = 15 

        #Pagination Buttons
        # Residents pagination
        self.backResBtn.clicked.connect(lambda: self.prev_page('res_page', self.load_residents))
        self.nextResBtn.clicked.connect(lambda: self.next_page('res_page', self.load_residents))

        # Complaints pagination
        self.backCompBtn.clicked.connect(lambda: self.prev_page('comp_page', self.load_complaints))
        self.nextCompBtn.clicked.connect(lambda: self.next_page('comp_page', self.load_complaints))

        # Officials pagination
        self.backOffiBtn.clicked.connect(lambda: self.prev_page('offi_page', self.load_officials))
        self.nextOffiBtn.clicked.connect(lambda: self.next_page('offi_page', self.load_officials))

        #Search buttons for RESIDENT, OFFICIALS, COMPLAINTS
        #Residents Search
        self.searchResBtn.clicked.connect(
        lambda: self.universal_search(
            "residents",
            self.searchRes_line,
            self.resident_table
        )
    )   
        #Complaints Search
        self.searchCompBtn.clicked.connect(
        lambda: self.universal_search(
            "complaints",
            self.searchComp_line,
            self.complaint_table
        )
    )
        #Officials Search
        self.searchOffiBtn.clicked.connect(
        lambda: self.universal_search(
            "barangay_officials",
            self.searchOffi_line,
            self.official_table
        )
    )
        
        # Table Header Sort
        self.resSort = 'ASC'
        self.comSort = 'ASC'
        self.offSort = 'ASC'
        self.resident_table.horizontalHeader().sectionClicked.connect(self.on_resident_header_clicked)
        self.complaint_table.horizontalHeader().sectionClicked.connect(self.on_complaint_header_clicked)
        self.official_table.horizontalHeader().sectionClicked.connect(self.on_barangay_official_header_clicked)

        self.refreshCasesBtn.clicked.connect(self.refreshCasBtnClicked)


    def onDashboardBtnClicked(self, item):
        row = item.row()
        col = item.column()
        value = item.text()
        row_values = self.db.get_element_by_id("complaints", self.pendingComp_table.item(row, 0).text())
        dialog = InfoComplaintDialog(row_values, self.db)
        dialog.exec_()
        self.showDashboardTable()

    def showDashboardTable(self):
        # Load the overall counts
        self.overallRes_line.setText(str(self.db.count_elements("residents")))
        self.overallOffi_line.setText(str(self.db.count_elements("barangay_officials")))
        self.updateDashboardCases()

        # Set up the pending complaints table
        self.pendingComp_table.setRowCount(0)
        pending_cases = self.db.get_pending_complaints()
        for row_num, row_data in enumerate(pending_cases):
            self.pendingComp_table.insertRow(row_num)
            self.pendingComp_table.setItem(row_num, 0, QTableWidgetItem(str(row_data[0]))) # ComplaintID
            self.pendingComp_table.setItem(row_num, 1, QTableWidgetItem(str(row_data[4]))) # Category
            self.pendingComp_table.setItem(row_num, 2, QTableWidgetItem(str(row_data[1]))) # DateTime
            self.pendingComp_table.setItem(row_num, 3, QTableWidgetItem(str(row_data[6]))) # Location
            self.pendingComp_table.setItem(row_num, 4, QTableWidgetItem(str(row_data[5]))) # Status

    def refreshCasBtnClicked(self):
        self.sortCases_box.setCurrentIndex(0)  # Reset to "All Months"

    def updateDashboardCases(self):
        month = self.sortCases_box.currentIndex()
        # Create a datetime object for the first day of the selected month in the current year
        now = datetime.now()
        year = now.year
        # If month is 0 ("All Months"), use January as default for the date, but let your count_complaints_status handle "all months"
        r = self.db.count_complaints_status()
        result = []
        if month > 0:
            dt = datetime(year, month, 1)
            r = self.db.count_complaints_status(dt)
        for i in r:
            result.append(str(i).replace(",", "").replace("(", "").replace(")", ""))

        self.overallComp_line.setText(result[0])
        self.overallpendComp_line.setText(result[2])
        self.overallcompComp_line.setText(result[1])

    def on_resident_header_clicked(self, logicalIndex):
        headers = ['resident_id', 'first_name', 'last_name', 'age', 'sex', 'contact']
        headers_names = ['RESIDENTID', 'FIRSTNAME', 'LASTNAME', 'AGE', 'SEX', 'CONTACT']
        if self.resSort == 'ASC':
            self.resSort = 'DESC'
        else:
            self.resSort = 'ASC'
        self.load_residents(page=self.res_page, column=headers[logicalIndex], order=self.resSort)
        self.sortRes_box.setCurrentText(headers_names[logicalIndex])
        self.resSortCurrentSetting = [headers[logicalIndex], self.resSort]  # Update current sorting settings

    def on_complaint_header_clicked(self, logicalIndex):
        headers = ['complaint_id', 'resident_id', 'complaint_category', 'date_time', 'complaint_status']
        headers_names = ['COMPLAINTID', 'RESIDENTID', 'CATEGORY', 'DATETIME', 'STATUS', 'LOCATION']
        if self.comSort == 'ASC':
            self.comSort = 'DESC'
        else:
            self.comSort = 'ASC'
        self.load_complaints(page=self.comp_page, column=headers[logicalIndex], order=self.comSort)
        self.sortComp_box.setCurrentText(headers_names[logicalIndex])
        self.comSortCurrentSetting = [headers[logicalIndex], self.comSort]

    def on_barangay_official_header_clicked(self, logicalIndex):
        headers = ['barangay_official_id', 'position', 'first_name', 'last_name', 'contact']
        headers_names = ['OFFICIALID', 'POSITION', 'FIRSTNAME', 'LASTNAME', 'CONTACT']
        if self.offSort == 'ASC':
            self.offSort = 'DESC'
        else:
            self.offSort = 'ASC'
        self.load_officials(page=self.offi_page, column=headers[logicalIndex], order=self.offSort)
        self.sortOff_box.setCurrentText(headers_names[logicalIndex])
        self.offSortCurrentSetting = [headers[logicalIndex], self.offSort]

    def plot_complaint_pie_chart(self):
        # layout chart in chart_frame
        layout = self.chart_frame.layout()

        # clear widget every change
        self.monthFilterBox.setParent(None)  # remove combo box temp
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget:
                layout.removeWidget(widget)
                widget.deleteLater()

        # chart label
        label = QLabel("Overall Complaints")
        label.setStyleSheet("font-size: 24px; border: 0px;")
        label.setAlignment(QtCore.Qt.AlignLeft)
        layout.addWidget(label)

        # get data
        month_index = self.monthFilterBox.currentIndex()
        cursor = self.db.cursor

        if month_index == 0:
            cursor.execute("SELECT complaint_status FROM complaints")
        else:
            cursor.execute("""
                SELECT complaint_status FROM complaints
                WHERE MONTH(STR_TO_DATE(date_time, '%Y-%m-%d')) = %s
            """, (month_index,))

        results = cursor.fetchall()

        # count cases
        completed = sum(1 for r in results if r[0] == "Completed")
        pending = sum(1 for r in results if r[0] == "Pending")
        cancelled = sum(1 for r in results if r[0] == "Cancelled")
        total = completed + pending + cancelled

        # create chart
        fig = Figure(figsize=(10, 9), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_position([0.1, 0.2, 0.8, 0.7])

        # chart data
        if total == 0:
            wedges, texts = ax.pie(
                [1],
                labels=[""],
                colors=["#D3D3D3"],
                startangle=90,
                wedgeprops=dict(width=0.5)
            )
            legend_labels = ["No Complaints: 0"]
        else:
            wedges, texts = ax.pie(
                [completed, pending, cancelled],
                labels=["", "", ""],
                colors=["#94FF94", "#FFD994", "#FFB3B3"],
                startangle=90,
                wedgeprops=dict(width=0.5)
            )
            legend_labels = [
                f"Completed: {completed}",
                f"Pending:   {pending}",
                f"Cancelled: {cancelled}"
            ]

        ax.axis("equal")
        ax.legend(
            wedges, legend_labels,
            title="",
            loc='center',
            bbox_to_anchor=(0.5, -0.2),
            frameon=False
        )

        # layout shi idk
        fig.tight_layout(rect=[0, 0.15, 1, 0.95])
        
        # widgets in correct order
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        layout.addWidget(self.monthFilterBox)


    def updateDateTime(self):
        current = QDateTime.currentDateTime()
        formatted = current.toString("ddd, MMM d, h:mm AP")
        self.labelDateTime1.setText(formatted)

#add dialogs
    def add_residents(self):
        dialog = AddResidentDialog(self, db=self.db)
        dialog.exec_()
        self.load_residents()
        
    def add_complaints(self):
        dialog = AddComplaintDialog(self, db=self.db)
        dialog.exec_()
        self.load_complaints()

    def add_officials(self):
        dialog = AddOfficialDialog(self, db=self.db)
        dialog.exec_()
        self.load_officials()

    def show_exit_message(self):
        reply = QMessageBox.question(self, 'Exit', 'Are you sure you want to exit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
            
    def show_home(self):
        self.stackedWidget.setCurrentIndex(0)
        self.overallRes_line.setText(str(self.db.count_elements("residents")))
        self.overallOffi_line.setText(str(self.db.count_elements("barangay_officials")))
        self.updateDashboardCases()
        self.plot_complaint_pie_chart()
        self.showDashboardTable()

    def show_residents(self):
        self.stackedWidget.setCurrentIndex(1)
        self.load_residents()

    def show_complaints(self):
        self.stackedWidget.setCurrentIndex(2)
        self.load_complaints()

    def show_officials(self):
        self.stackedWidget.setCurrentIndex(3)
        self.load_officials()

    def edit_resident(self):
        selected = self.resident_table.currentRow()
        if selected < 0:
            warnMessageBox(self, "Edit Resident", "Please select a resident to edit.")
            return
        resident_id = self.resident_table.item(selected, 0).text()
        db = self.db
        data = db.get_element_by_id("residents", resident_id)
        if not data:
            warnMessageBox(self, "Edit Resident", "Resident not found.")
            return
        dialog = AddResidentDialog(self)
        # Pre-fill dialog fields
        dialog.addresident_residentID_input.setText(str(data[0]))
        dialog.addresident_firstname_input.setText(str(data[1]))
        dialog.addresident_lastname_input.setText(str(data[2]))
        dialog.addresident_age_input.setText(str(data[3]))
        dialog.addresident_dob_input.setDate(QtCore.QDate.fromString(str(data[4]), "yyyy-MM-dd"))
        dialog.addresident_photo_label.setText(str(data[5]))
        dialog.addresident_address_input.setPlainText(str(data[6]))
        dialog.addresident_contact_input.setText(str(data[7]))
        dialog.addresident_sex_input.setCurrentText(str(data[8]))
        # Disable editing of resident_id
        dialog.addresident_residentID_input.setEnabled(False)
        if dialog.exec_() == QDialog.Accepted:
            # Update the record
            updated = (
                resident_id,
                dialog.addresident_firstname_input.text(),
                dialog.addresident_lastname_input.text(),
                dialog.addresident_dob_input.date().toString("yyyy-MM-dd"),
                dialog.addresident_photo_label.text(),
                dialog.addresident_address_input.toPlainText(),
                dialog.addresident_contact_input.text(),
                dialog.addresident_sex_input.currentText()
            )
            db.update_resident(resident_id, updated)
            self.load_residents()

    def delete_resident(self):
        selected = self.resident_table.currentRow()
        if selected < 0:
            warnMessageBox(self, "Delete Resident", "Please select a resident to delete.")
            return
        resident_id = self.resident_table.item(selected, 0).text()
        reply = QMessageBox.question(self, "Delete Resident", f"Delete resident {resident_id}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.remove_resident(resident_id)
            self.load_residents()

    def load_residents(self, page=None, column="last_name", order='ASC'):
        if page is not None:
            self.res_page = max(1, page)
        else:
            self.res_page = max(1, self.res_page)
        db = self.db
        self.resident_table.setRowCount(0)
        results = db.get_elements(
            table="residents",
            column=column,
            page=self.res_page,
            order=order,
            limit=self.rows_per_page
        )
        for row_num, row_data in enumerate(results):
            self.db.update_resident_age(row_data[0], self.db.calculate_age(row_data[4]), False)  # Update age based on birth date
            self.resident_table.insertRow(row_num)
            self.resident_table.setItem(row_num, 0, QTableWidgetItem(str(row_data[0])))  # ResidentID
            self.resident_table.setItem(row_num, 1, QTableWidgetItem(str(row_data[1])))  # FirstName
            self.resident_table.setItem(row_num, 2, QTableWidgetItem(str(row_data[2])))  # LastName
            self.resident_table.setItem(row_num, 3, QTableWidgetItem(str(row_data[3])))  # Age
            self.resident_table.setItem(row_num, 4, QTableWidgetItem(str(row_data[8])))  # Sex
            self.resident_table.setItem(row_num, 5, QTableWidgetItem(str(row_data[7])))  # Contact
            self.resident_table.setItem(row_num, 6, QTableWidgetItem(str(row_data[4])))  # Birthdate
            self.resident_table.setItem(row_num, 7, QTableWidgetItem(str(row_data[6])))  # Address
            self.resident_table.setItem(row_num, 8, QTableWidgetItem(str(row_data[5])))  # Credentials (photo_cred)
        self.ResPage_line.setText(str(self.res_page))

    def on_resident_item_clicked(self, item):
        row = item.row()
        col = item.column()
        value = item.text()
        row_values = [self.resident_table.item(row, c).text() for c in range(self.resident_table.columnCount())]
        dialog = InfoResidentDialog(self.db.get_element_by_id("residents", row_values[0]), self.db)
        dialog.display_info()
        dialog.exec_() 
        self.load_residents()

    def edit_official(self):
        selected = self.official_table.currentRow()
        if selected < 0:
            warnMessageBox(self, "Edit Official", "Please select an official to edit.")
            return
        official_id = self.official_table.item(selected, 0).text()
        db = self.db 
        data = db.get_element_by_id("barangay_officials", official_id)
        if not data:
            warnMessageBox(self, "Edit Official", "Official not found.")
            return
        dialog = AddOfficialDialog(self)
        # Pre-fill dialog fields
        dialog.addofficial_officialID_input.setText(str(data[0]))
        dialog.addofficial_firstname_input.setText(str(data[1]))
        dialog.addofficial_lastname_input.setText(str(data[2]))
        dialog.addofficial_contact_input.setText(str(data[3]))
        dialog.addofficial_position_input.setCurrentText(str(data[4]))
        # Disable editing of official_id
        dialog.addofficial_officialID_input.setEnabled(False)
        if dialog.exec_() == QDialog.Accepted:
            updated = (
                official_id,
                dialog.addofficial_firstname_input.text(),
                dialog.addofficial_lastname_input.text(),
                dialog.addofficial_contact_input.text(),
                dialog.addofficial_position_input.currentText()
            )
            db.update_barangay_official(official_id, updated)
            self.load_officials()

    def delete_official(self):
        selected = self.official_table.currentRow()
        if selected < 0:
            warnMessageBox(self, "Delete Official", "Please select an official to delete.")
            return
        official_id = self.official_table.item(selected, 0).text()
        reply = QMessageBox.question(self, "Delete Official", f"Delete official {official_id}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.remove_official(official_id)
            self.load_officials()

    def load_officials(self, page=None, column='last_name', order='ASC'):
        if page is not None:
            self.offi_page = max(1, page)
        else:
            self.offi_page = max(1, self.offi_page)
        db = self.db 
        self.official_table.setRowCount(0)
        results = db.get_elements(
            table="barangay_officials",
            column=column,
            order=order,
            page=self.offi_page,
            limit=self.rows_per_page
        )
        for row_num, row_data in enumerate(results):
            self.official_table.insertRow(row_num)
            self.official_table.setItem(row_num, 0, QTableWidgetItem(str(row_data[0])))  # OFFICIALID
            self.official_table.setItem(row_num, 1, QTableWidgetItem(str(row_data[4])))  # POSITION
            self.official_table.setItem(row_num, 2, QTableWidgetItem(str(row_data[1])))  # FIRSTNAME
            self.official_table.setItem(row_num, 3, QTableWidgetItem(str(row_data[2])))  # LASTNAME
            self.official_table.setItem(row_num, 4, QTableWidgetItem(str(row_data[3])))  # CONTACT
        self.OffiPage_line.setText(str(self.offi_page))

    def on_official_item_clicked(self, item):
        row = item.row()
        col = item.column()
        value = item.text()
        row_values = [self.official_table.item(row, c).text() for c in range(self.official_table.columnCount())]
        dialog = InfoOfficialDialog(self.db.get_barangay_official(row_values[0]), self.db)
        dialog.display_info()
        dialog.exec_()
        self.load_officials()

    def edit_complaint(self):
        selected = self.complaint_table.currentRow()
        if selected < 0:
            warnMessageBox(self, "Edit Complaint", "Please select a complaint to edit.")
            return
        complaint_id = self.complaint_table.item(selected, 0).text()
        db = self.db
        db.cursor.execute("SELECT * FROM Complaint WHERE complaint_id = %s", (complaint_id,))
        data = db.cursor.fetchone()
        if not data:
            warnMessageBox(self, "Edit Complaint", "Complaint not found.")
            return
        dialog = AddComplaintDialog(self)
        # Pre-fill dialog fields
        dialog.addcomplaint_complaintID_input.setText(str(data[0]))
        dialog.addcomplaint_date_input.setDate(QtCore.QDate.fromString(str(data[1]), "yyyy-MM-dd"))
        dialog.addcomplaint_description_input.setText(str(data[2]))
        dialog.addcomplaint_residentID_input.setCurrentText(str(data[3]))
        dialog.addcomplaint_category_input.setCurrentText(str(data[4]))
        dialog.addcomplaint_status_input.setCurrentText(str(data[5]))
        dialog.addcomplaint_location_input.setText(str(data[6]))
        # Disable editing of complaint_id
        dialog.addcomplaint_complaintID_input.setEnabled(False)
        if dialog.exec_() == QDialog.Accepted:
            updated = (
                complaint_id,
                dialog.addcomplaint_date_input.date().toString("yyyy-MM-dd"),
                dialog.addcomplaint_description_input.text(),
                dialog.addcomplaint_residentID_input.currentText(),
                dialog.addcomplaint_category_input.currentText(),
                dialog.addcomplaint_status_input.currentText(),
                dialog.addcomplaint_location_input.text()
            )
            db.update_complaint(complaint_id, updated)

    def delete_complaint(self):
        selected = self.complaint_table.currentRow()
        if selected < 0:
            warnMessageBox(self, "Delete Complaint", "Please select a complaint to delete.")
            return
        complaint_id = self.complaint_table.item(selected, 0).text()
        reply = QMessageBox.question(self, "Delete Complaint", f"Delete complaint {complaint_id}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.remove_complaint(complaint_id)
            self.load_complaints()

    def load_complaints(self, page=None, column="date_time", order='ASC'):
        if page is not None:
            self.comp_page = max(1, page)
        else:
            self.comp_page = max(1, self.comp_page)
        db = self.db  # Create a new Database instance
        self.complaint_table.setRowCount(0)
        results = db.get_elements(
            table="complaints",
            column=column,
            order=order,
            page=self.comp_page,
            limit=self.rows_per_page
        )
        for row_num, row_data in enumerate(results):
            self.complaint_table.insertRow(row_num)
            self.complaint_table.setItem(row_num, 0, QTableWidgetItem(str(row_data[0])))  # ComplaintID
            self.complaint_table.setItem(row_num, 1, QTableWidgetItem(str(row_data[3])))  # ResidentID
            self.complaint_table.setItem(row_num, 2, QTableWidgetItem(str(row_data[4])))  # Category
            self.complaint_table.setItem(row_num, 3, QTableWidgetItem(str(row_data[1])))  # DateTime
            self.complaint_table.setItem(row_num, 4, QTableWidgetItem(str(row_data[5])))  # Status
            self.complaint_table.setItem(row_num, 5, QTableWidgetItem(str(row_data[6])))  # Location
            self.complaint_table.setItem(row_num, 6, QTableWidgetItem(str(row_data[2])))  # Description
        self.CompPage_line.setText(str(self.comp_page))
        
    def on_complaint_item_clicked(self, item):
        row = item.row()
        col = item.column()
        value = item.text()
        row_values = self.db.get_element_by_id("complaints", self.complaint_table.item(row, 0).text())
        dialog = InfoComplaintDialog(row_values, self.db)
        dialog.exec_()
        self.load_complaints()

    def universal_search(self, table, searchbar, tablewidget):
        query = searchbar.text().strip()
        tablewidget.setRowCount(0)
        results = self.db.universal_search(table,query)
        for row_num, row_data in enumerate(results):
            tablewidget.insertRow(row_num,)
            for col_num, value in enumerate(row_data):
                tablewidget.setItem(row_num, col_num, QTableWidgetItem(str(value)))
    
    def next_page(self, page_attr, load_func):
        setattr(self, page_attr, getattr(self, page_attr) + 1)
        load_func()

    def prev_page(self, page_attr, load_func):
        if getattr(self, page_attr) > 1:
            setattr(self, page_attr, getattr(self, page_attr) - 1)
            load_func()
        else:
            setattr(self, page_attr, 1)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainClass()
    main.show()
    exit_code = app.exec_()
    main.db.close_connection()
    print("Application closed and database connection closed.")
    sys.exit(exit_code)
