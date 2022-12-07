import sys
from enum import Enum, auto


from PyQt6.QtGui import QIcon, QPixmap, QValidator, QStandardItemModel, QStandardItem
from PyQt6.QtCore import QSize, Qt, QEvent, QObject, QAbstractTableModel, QStringListModel, QRect
from PyQt6.QtWidgets import QMainWindow, QApplication,QDialog,  QListWidget, \
    QListWidgetItem,QTableWidgetItem, QLabel

import PyQt6

from Model import Tournament
from mainWindowUI import Ui_MainWindow
from parameterUI import Ui_parameter
from team_membersUI import Ui_Dialog as team_member_dialog

from TeamEditorUI import Ui_TeamAndScheduleEditor
from Scheduler_Model import Scheduler


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tournament = Tournament()
        self.setupUi(self)
        # State tabula rasa
        self.tournament_parameters.setEnabled(True)
        self.teams_and_schedule.setEnabled(False)
        self.finish_tournament.setEnabled(True)

        self.tournament_parameters.clicked.connect(self._enter_parameters)
        self.teams_and_schedule.clicked.connect(self._enter_teams)
        self.Roaster.clicked.connect(self._enter_members)

    def _enter_parameters(self, *args, **kw):
        dialog = QDialog(self)
        dialog.ui = Ui_parameter()
        dialog.ui.setupUi(dialog)
        ret = dialog.exec()
        if not ret:
            return
        self.tournament.duration     = dialog.ui.match_duration.value()
        self.tournament.intermission = dialog.ui.intermission.value()
        self.tournament.name         = dialog.ui.tournamentName.text()
        self.tournament.start_time   = dialog.ui.startTime.time()
        self.setWindowTitle(self.tournament.name)
        self.teams_and_schedule.setEnabled(True)

    def _enter_members(self, *args, **kw):
        dialog = self.member_dialog = QDialog(self)
        dialog.ui = team_member_dialog()
        dialog.ui.setupUi(dialog)
        dialog.ui.add_player.clicked.connect(self._add_player)
        ret = dialog.exec()
        if not ret:
            return
        ml = dialog.ui.member_list
        for i in range(ml.rowCount()):
            d = [ml.item(i, j).text() for j in range(3)]
            self.tournament.add_player("hansi", *d)

    def _add_player(self, *args, **kw):
        ui = self.member_dialog.ui
        table = ui.member_list
        row = table.rowCount()
        table.insertRow(row)
        table.setItem(row, 1, QTableWidgetItem(
            ui.input_name.text().strip())
        )
        table.setItem(row, 2, QTableWidgetItem(ui.input_surname.text().strip()))
        table.setItem(row, 0, QTableWidgetItem(ui.input_id.text()))
        ui.input_surname.clear()
        ui.input_name.clear()
        ui.input_id.clear()
        ui.input_id.setFocus()

    def _enter_teams(self, *args, **kw):
        self.team_dialog = dialog = QDialog(self)
        dialog.ui = Ui_TeamAndScheduleEditor()
        dialog.ui.setupUi(dialog)
        dialog.ui.addTeam.pressed.connect(self._add_team)
        dialog.ui.create_schedule_button.clicked.connect(self._create_schedule)
        dialog.show()
        ret = dialog.exec()
        if not ret:
            return
        self.tournament.teams = self._actual_team_list()[:]
        self.tournament.show()
        top  = 180
        for team in self.tournament.teams:
            label = QLabel(team)
            label.setGeometry(QRect(9, top, 163, 17))
            self.centralwidget.addWidget(label)
            top += 22

    def _add_team(self):
        ui  = self.team_dialog.ui
        txt = ui.team.text()
        teams = self._actual_team_list()
        if txt and txt not in teams:
            ui.team_list.addItem(QListWidgetItem(ui.team.text()))
        ui.team.clear()
        ui.team.setFocus()



#    def rowCount(self, index):
#        return len(self.todos)
#
#    def connectSignalsSlots(self):
#        self.add_team.clicked.connect(self._add_team)
#        self.create_schedule.clicked.connect(self._create_schedule)
#
#        self.break_between_matches.setValidator(QIntValidator(0, 15))
#        self.break_between_matches.setText("1")
#        self.match_duration.setValidator(QIntValidator(1, 90))
#        self.match_duration.setText("14")
#
#        self.switch_matches.clicked.connect(self._switch_matches)
#        self.switch_team_order.clicked.connect(self._switch_home_guest)
#
#        self.number_of_match_to_switch.setText("1")
#        self.home_team.setText("1")
#        self.guest_team.setText("1")
#
#        self.store_schedule.clicked.connect(self._store_schedule)
#
#    def _store_schedule(self):
#        self.schedule.store_on_disk()
#
#    def _switch_matches(self):
#        if not 1 <= int(self.home_team.text()) <= self._no_matches():
 #           print("shit home")
 #           return
 #       if not 1 <= int(self.guest_team.text()) <= self._no_matches():
#            print("shit guest")
#            return
#
#        self.schedule.switch_matches(int(self.home_team.text()),
#                                     int(self.guest_team.text()))
#        self._show_schedule()
#
#    def _switch_home_guest(self):
#        idx = int(self.number_of_match_to_switch.text())
#        if not 1 <= idx <= self._no_matches():
#            print("shit switch")
#            return
#        self.schedule.switch_home_guest(idx)
#        self._show_schedule()
#
#    def _no_matches(self):
#        no_teams = len(self._actual_team_list())
#        return int(round(no_teams*(no_teams-1)/2))
#
#    def _add_team(self):
#        txt = self.team.text()
#        teams = self._actual_team_list()
#        if txt and txt not in teams:
#            self.team_list.addItem(QListWidgetItem(self.team.text()))
#        self.team.setFocus()
#
    def _actual_team_list(self):
        ui = self.team_dialog.ui
        return [str(ui.team_list.item(i).text())
                for i in range(ui.team_list.count())]
#
    def _create_schedule(self):
        ui = self.team_dialog.ui
        ui.create_schedule_button.clicked.connect(self._create_schedule)
        teams = self._actual_team_list()
        start = self.tournament.start_time
        self.schedule = Scheduler([])
        self.schedule = Scheduler(teams
                                  , f"{start.hour()}:{start.minute()}"
                                  , int(self.tournament.duration)
                                  , int(self.tournament.intermission))
        self._show_schedule()

    def _show_schedule(self):
        ui = self.team_dialog.ui
        for i in self.schedule.matches:
            ui.scheduleEditor.addItem(QListWidgetItem(self.schedule.print_single_match(i)))
#
#    def about(self):
#        QMessageBox.about(
#            self,
#            "Tournament Director - Schedule Editor",
#            "<p>A sample text editor app built with:</p>"
#            "<p>- PyQt</p>"
#            "<p>- Qt Designer</p>"
#            "<p>- Python</p>",
#        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
