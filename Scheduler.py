import sys
from pprint import pprint
import random
import operator
import datetime
import itertools

from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QTabWidget,QVBoxLayout, QGridLayout, QTableWidget, QLabel,  QTableWidgetItem, QComboBox, QTableView, QTableWidget, QInputDialog, QDialog,QRadioButton, QMessageBox, QLCDNumber, QLineEdit, QListWidget, QListWidgetItem
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import pyqtSlot, pyqtSignal
from PyQt6.QtCore import QSize, Qt, QEvent, QObject, QAbstractTableModel


from PyQt6.uic import loadUi

from SchedulerUI import Ui_MainWindow
from Scheduler_Model import Scheduler

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        print("SignalSlots")
        self.add_team.clicked.connect(self._add_team)
        self.create_schedule.clicked.connect(self._create_schedule)
#        self.action_Exit.triggered.connect(self.close)
#        self.action_Find_Replace.triggered.connect(self.findAndReplace)
#        self.action_About.triggered.connect(self.about)

    def _add_team(self):
        txt = self.team.text()
        teams = self._actual_team_list()
        if txt and txt not in teams:
            self.team_list.addItem(QListWidgetItem(self.team.text()))
        self.team.setFocus()

    def findAndReplace(self):
        print ("findAndReplace")
        dialog = FindReplaceDialog(self)
        dialog.exec()

    def _actual_team_list(self):
        return [str(self.team_list.item(i).text())
                for i in range(self.team_list.count())]

    def _create_schedule(self):
        teams = self._actual_team_list()
        self.schedule = Scheduler(teams)
        self._show_schedule()

    def _show_schedule(self):
        self.show_schedule.clear()
        for i in self.schedule.matches:
            self.show_schedule.addItem(QListWidgetItem(self.schedule.print_single_match(i)))

    def about(self):
        QMessageBox.about(
            self,
            "Tournament Director - Schedule Editor",
            "<p>A sample text editor app built with:</p>"
            "<p>- PyQt</p>"
            "<p>- Qt Designer</p>"
            "<p>- Python</p>",
        )


class FindReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/Scheduler.ui", self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
