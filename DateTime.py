from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer, QDateTime
from ComplaSys_ui import Ui_MainWindow  # Replace with your actual filename if different
import sys

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Setup timer to update time
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)  # Every second

        # Initial update
        self.updateDateTime()

    def updateDateTime(self):
        current = QDateTime.currentDateTime()
        formatted = current.toString("yyyy-MM-dd hh:mm:ss")
        self.ui.labelDateTime.setText(formatted)  # Make sure you have a QLabel with this objectName

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
