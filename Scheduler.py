import sys
from pprint import pprint
import random
import operator
import datetime
import itertools
import json


from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QTabWidget,QVBoxLayout, QGridLayout, QTableWidget, QLabel,  QTableWidgetItem, QComboBox, QTableView, QTableWidget, QInputDialog, QDialog,QRadioButton, QMessageBox, QLCDNumber, QLineEdit, QListWidget, QListWidgetItem
from PyQt6.QtGui import QIcon, QPixmap, QIntValidator, QValidator
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
        self.add_team.clicked.connect(self._add_team)
        self.create_schedule.clicked.connect(self._create_schedule)

        self.break_between_matches.setValidator(QIntValidator(0, 15))
        self.break_between_matches.setText("1")
        self.match_duration.setValidator(QIntValidator(1, 90))
        self.match_duration.setText("14")

        self.switch_matches.clicked.connect(self._switch_matches)
        self.switch_team_order.clicked.connect(self._switch_home_guest)

        self.number_of_match_to_switch.setText("1")
        self.home_team.setText("1")
        self.guest_team.setText("1")

        self.store_schedule.clicked.connect(self._store_schedule)

    def _store_schedule(self):
        json.dumps(self.schedule)

    def _switch_matches(self):
        if not 1 <= int(self.home_team.text()) <= self._no_matches():
            print("shit home")
            return
        if not 1 <= int(self.guest_team.text()) <= self._no_matches():
            print("shit guest")
            return

        self.schedule.switch_matches(int(self.home_team.text()),
                                     int(self.guest_team.text()))
        self._show_schedule()

    def _switch_home_guest(self):
        idx = int(self.number_of_match_to_switch.text())
        if not 1 <= idx <= self._no_matches():
            print("shit switch")
            return
        self.schedule.switch_home_guest(idx)
        self._show_schedule()

    def _no_matches(self):
        no_teams = len(self._actual_team_list())
        return int(round(no_teams*(no_teams-1)/2))

    def _add_team(self):
        txt = self.team.text()
        teams = self._actual_team_list()
        if txt and txt not in teams:
            self.team_list.addItem(QListWidgetItem(self.team.text()))
        self.team.setFocus()

    def _actual_team_list(self):
        return [str(self.team_list.item(i).text())
                for i in range(self.team_list.count())]

    def _create_schedule(self):
        teams = self._actual_team_list()
        start = self.tournamen_start_at.time()
        self.schedule = Scheduler(teams
                                  , f"{start.hour()}:{start.minute()}"
                                  , int(self.match_duration.text())
                                  , int(self.break_between_matches.text()))
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
