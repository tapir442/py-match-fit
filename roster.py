"""
"""

import sys
from functools import partial
import argparse
import pickle

import PyQt6

from PyQt6.QtCore import Qt, QTime

from PyQt6.QtWidgets import \
    QMainWindow, \
    QApplication, \
    QDialog, \
    QListWidgetItem, QTableWidgetItem, QPushButton, QErrorMessage

from Model import Tournament
# XXX should not be needed
from Match import Match
from mainWindowUI import Ui_MainWindow
from parameterUI import Ui_parameter
from team_membersUI import Ui_Dialog as team_member_dialog
from match_dialogUI import Ui_Match_Dialog

from TeamEditorUI import Ui_TeamAndScheduleEditor
from Scheduler_Model import Scheduler
import datetime

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        if len(sys.argv) == 1:
            self.tournament = Tournament()
        else:
            with open(sys.argv[1], "rb") as _:
                self.tournament = pickle.load(_)
        self.setupUi(self)
        # State tabula rasa
        self.tournament_parameters.setEnabled(True)
        if self.tournament.name:
            self.teams_and_schedule.setEnabled(True)
        else:
            self.teams_and_schedule.setEnabled(True)

        self.finish_tournament.setEnabled(True)

        self.setup_main_window()
        self.schedule = Scheduler([])

        self.setup_parameter_ui()
        self.tournament_parameters.clicked.connect(self._enter_parameters)
        self.teams_and_schedule.clicked.connect(self._enter_teams)
        self.logoLabel.setScaledContents(True)
        self.team_dialog = QDialog(self)
        self.team_dialog.ui = Ui_TeamAndScheduleEditor()
        self.member_dialog = QDialog(self)
        self.member_dialog.ui = team_member_dialog()
        self.matchPlan.itemClicked.connect(self._match_selected)
        self.setup_match()
        self.start_match.clicked.connect(self._start_match)

    def setup_main_window(self):
        top = 130
        for team in self.tournament.teams:
            pb = QPushButton(team, self.centralwidget)
            pb.move(9, top)
            top += 22
            pb.show()
            pb.clicked.connect(partial(self._enter_members, team))


    def setup_match(self):
        self.match_dialog = dialog = QDialog(self)
        dialog.ui = Ui_Match_Dialog()
        dialog.ui.setupUi(dialog)

    def _start_match(self, *args, **kw):
        dialog = self.match_dialog
        if self.tournament.match_idx == None:
            self.tournament.match_idx = 0
        else:
            self.tournament.match_idx += 1
        my_match = self.tournament.schedule[self.tournament.match_idx]
        print(my_match)
        import re
        mm = re.compile("^.*, (?P<home>.*) : (?P<guest>.*)$")
        mm = mm.match(my_match)
        dialog.ui.home_label.setText(mm.groupdict()["home"])
        dialog.ui.visiting_label.setText(mm.groupdict()["guest"])
        # XXX simplify
        TOP = 100
        INC = 14
        G   = 15
        top = TOP
        for player in self.tournament.teams[mm.groupdict()["home"]].players:
            player_data = self.tournament.teams[mm.groupdict()["home"]].players[player]
            v = "%s  %s  %s" % (player, player_data.name, player_data.surname)
            dialog.ui.home_team.addItem(v)
            button = QPushButton("+", dialog)
            button.setGeometry(48, top, G, G)
            button.clicked.connect(partial(self.click_plus, player))
            button = QPushButton("+", dialog)
            button.setGeometry(578, top, G, G)
            button.clicked.connect(partial(self.click_plus_guest, player))
            top += INC
        top = TOP
        for player in self.tournament.teams[mm.groupdict()["guest"]].players:
            player_data = self.tournament.teams[mm.groupdict()["guest"]].players[player]
            v = "%s  %s  %s" % (player, player_data.name, player_data.surname)
            dialog.ui.visiting_team.addItem(v)
            button = QPushButton("-", dialog)
            button.setGeometry(23, top, G, G)
            button.clicked.connect(partial(self.click_minus, player))
            button = QPushButton("-", dialog)
            button.setGeometry(600, top, G, G)
            button.clicked.connect(partial(self.click_minus_guest, player))
            top += INC
        self.running_match = Match(self.tournament.teams[mm.groupdict()["home"]],
                                   self.tournament.teams[mm.groupdict()["guest"]])
        self.running_match.start()
        ret = dialog.exec()
        self.running_match.close()
        from pprint import pprint
        pprint(self.running_match.__dict__)

    def click_plus(self, player):
        print("plus home", player)
        self.running_match.home_scored(player)

    def click_minus(self, player):
        print("minus home", player)

    def click_plus_guest(self, player):
        self.running_match.guest_scored(player)


    def click_minus_guest(self, player):
        print("plus gueat", player)


    def _match_selected(self, item):
        print(self.matchPlan.currentItem().text())
        print(dir(self.matchPlan.currentItem()))

    def setup_parameter_ui(self):
        self.parameters_dialog = dialog = QDialog(self)
        dialog.ui = Ui_parameter()
        dialog.ui.setupUi(dialog)
        dialog.ui.tournamentName.textChanged.connect(self._check_tournament_name)

    def _check_tournament_name(self, s):
        if s:
            return True
        msg = QErrorMessage()
        msg.showMessage("gib wos ein")
        msg.exec()
        self.parameters_dialog.ui.tournamentName.setFocus()
        return False

    def _enter_parameters(self, *args, **kw):
        dialog = self.parameters_dialog
        dialog.ui.match_duration.setValue(self.tournament.duration)
        dialog.ui.intermission.setValue(self.tournament.intermission)
        dialog.ui.tournamentName.setText(self.tournament.name)
        st = self.tournament.start_time
        if isinstance(st, datetime.time):
            t = QTime(st.hour, st.minute)
        else:
            t = eval(st)
        time = QTime(t.hour(), t.minute())
        dialog.ui.startTime.setTime(time)
        ret = dialog.exec()
        if not ret:
            return
        if not self._check_tournament_name(dialog.ui.tournamentName.text()):
            return
        self.tournament.duration     = dialog.ui.match_duration.value()
        self.tournament.intermission = dialog.ui.intermission.value()
        self.tournament.name         = dialog.ui.tournamentName.text()
        self.tournament.start_time   = str(dialog.ui.startTime.time())
        self.tournament.store()
        self.setWindowTitle(self.tournament.name)
        self.teams_and_schedule.setEnabled(True)

    def _enter_members(self, team, *args, **kw):
        dialog = self.member_dialog
        dialog.ui.setupUi(dialog)
        row = 0
        for player in self.tournament.teams[team].players:
            player_data = self.tournament.teams[team].players[player]
            dialog.ui.member_list.insertRow(row)
            dialog.ui.member_list.setItem(row, 0, QTableWidgetItem(player))
            dialog.ui.member_list.setItem(row, 1, QTableWidgetItem(player_data.name))
            dialog.ui.member_list.setItem(row, 2, QTableWidgetItem(player_data.surname))
        dialog.ui.add_player.clicked.connect(self._add_player)
        ret = dialog.exec()
        if not ret:
            return
        ml = dialog.ui.member_list
        for i in range(ml.rowCount()):
            d = [ml.item(i, j).text() for j in range(3)]
            self.tournament.add_player(team, *d)
        self.tournament.store()

    def _add_player(self, *args, **kw):
        ui = self.member_dialog.ui
        table = ui.member_list
        row = table.rowCount()
        table.insertRow(row)
        table.setItem(row, 1, QTableWidgetItem(
            ui.input_name.text().strip().title())
        )
        table.setItem(row, 2, QTableWidgetItem(ui.input_surname.text().strip().title()))
        table.setItem(row, 0, QTableWidgetItem(ui.input_id.text()))
        ui.input_surname.clear()
        ui.input_name.clear()
        ui.input_id.clear()
        ui.input_id.setFocus()
        self.tournament.store()

    def _enter_teams(self, *args, **kw):
        dialog = self.team_dialog
        dialog.ui.setupUi(dialog)
        for team in self.tournament.teams:
            dialog.ui.team_list.addItem(team)
        for match in self.tournament.schedule:
            dialog.ui.scheduleEditor.addItem(match)
        dialog.ui.addTeam.pressed.connect(self._add_team)
        dialog.ui.create_schedule_button.clicked.connect(self._create_schedule)
        dialog.show()
        ret = dialog.exec()
        if not ret:
            return
        for team in self._actual_team_list():
            self.tournament.add_team(team)
        for i in range(dialog.ui.scheduleEditor.count()):
            self.tournament.schedule.append(dialog.ui.scheduleEditor.item(i).text())
        self.tournament.show()
        top = 130
        for team in self.tournament.teams:
            pb = QPushButton(team, self.centralwidget)
            pb.move(9, top)
            top += 22
            pb.show()
            pb.clicked.connect(partial(self._enter_members, team))
        for match_no, match in self.schedule.matches.items():
            self.matchPlan.addItem(":".join(match))
        self.tournament.show()
        self.matchPlan.show()
        self.tournament.store()

    def _add_team(self):
        ui = self.team_dialog.ui
        txt = ui.team.text()
        teams = self._actual_team_list()
        if txt and txt not in teams:
            ui.team_list.addItem(QListWidgetItem(ui.team.text()))
        ui.team.clear()
        ui.team.setFocus()
        self.tournament.store()


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
        start = eval(self.tournament.start_time)
        self.schedule = Scheduler(teams
                                  , f"{start.hour()}:{start.minute()}"
                                  , int(self.tournament.duration)
                                  , int(self.tournament.intermission))
        self._show_schedule()
        breakpoint()
        self.tournament.store()

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

def main_GUI():
    roster = QApplication(sys.argv)
    gui    = Window()
    gui.show()
    return roster, gui


if __name__ == "__main__":
    app, ui = main_GUI()
    sys.exit(app.exec())
