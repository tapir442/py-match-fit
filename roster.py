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
    QListWidgetItem, QTableWidgetItem, QPushButton, QErrorMessage, \
    QAbstractItemView, QTableWidget

from PyQt6.QtGui import QPixmap, QColor


from Model import Tournament
# XXX should not be needed
from Match import Match
from mainWindowUI import Ui_MainWindow
from parameterUI import Ui_parameter
from team_membersUI import Ui_Dialog as team_member_dialog
from match_dialogUI import Ui_Match_Dialog

from TeamEditorUI import Ui_TeamAndScheduleEditor

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

        self.finish_tournament.setEnabled(False)

        self.setup_main_window()

        self.setup_parameter_ui()
        self.tournament_parameters.clicked.connect(self._enter_parameters)
        self.teams_and_schedule.clicked.connect(self._enter_teams)
        self.logoLabel.setScaledContents(True)
        self.team_dialog = QDialog(self)
        self.team_dialog.ui = Ui_TeamAndScheduleEditor()
        self.member_dialog = QDialog(self)
        self.member_dialog.ui = team_member_dialog()
#        self.matchPlan.itemClicked.connect(self._match_selected)
        self.setup_match()
        self.start_match.clicked.connect(self._start_match)

    def setup_main_window(self):
        self.finish_tournament.clicked.connect(self._ciao)
        self.setWindowTitle(self.tournament.name)
        p = self.logoLabel.setPixmap(QPixmap("1980.jpeg"))
        top = 130
        for team in self.tournament.teams:
            pb = QPushButton(team, self.centralwidget)
            pb.move(9, top)
            top += 22
            pb.show()
            pb.clicked.connect(partial(self._enter_members, team))
        self.setup_match_plan()
        self.show_table(self)

    def _ciao(self):
        self.tournament.store()
        sys.exit(0)

    def setup_match_plan(self) -> None:
        """
        Fills table with the match data
        """
        mp = self.matchPlan
        mp.setRowCount(len(self.tournament.schedule.matches))
        row = 0
        w   = QTableWidgetItem
        for match in self.tournament.schedule.matches.values():
            mp.setItem(row, 0, w(str(match.starts)))
            mp.setItem(row, 1, w(match.home.name))
            mp.setItem(row, 2, w(match.guest.name))
            mp.setItem(row, 3, w(":".join((
                                 str(match.running_score[0].value),
                                 str(match.running_score[1].value)))))
            row += 1
        mp.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        if self.tournament.match_idx is not None:
            i = self.tournament.match_idx
        else:
            i = 0
        if i < len(self.tournament.schedule.matches):
            for j in range(self.matchPlan.columnCount()):
                self.matchPlan.item(i, j).setBackground(
                    QColor(125,125,125))
        if self.tournament.match_idx == len(self.tournament.schedule.matches):
            self.start_match.setEnabled(False)
            self.finish_tournament.setEnabled(True)
        mp.show()

    def show_table(self, widget):
        r = self.tournament.standings()
        widget.tabelle.clear()
        widget.tabelle.setRowCount(len(self.tournament.teams))
        row = 0
        w = QTableWidgetItem
        t = widget.tabelle.setItem
        for _ in r:
            t(row, 0, w(_.team))
            t(row, 1, w(str(_.goals)))
            t(row, 2, w(str(_.got)))
            t(row, 3, w(str(_.goals - _.got)))
            t(row, 4, w(str(_.points)))
            row += 1
        widget.tabelle.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        widget.tabelle.show()
        r = self.tournament.scorers()
        widget.scorer.clear()
        widget.scorer.setRowCount(len(r))
        row = 0
        w = QTableWidgetItem
        t = widget.scorer.setItem
        for _ in r:
            t(row, 0, w(_.number))
            t(row, 1, w(_.name))
            t(row, 2, w(_.team))
            t(row, 3, w(str(_.goals)))
            row += 1
        widget.scorer.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        widget.scorer.show()

    def setup_match(self):
        self.match_dialog = dialog = QDialog(self)
        dialog.ui = Ui_Match_Dialog()
        dialog.ui.setupUi(dialog)

    def _start_match(self, *args, **kw):
        dialog = self.match_dialog
        if self.tournament.match_idx == None:
            self.tournament.match_idx = 1
        else:
            self.tournament.match_idx += 1
        my_match = self.tournament.schedule.matches[self.tournament.match_idx]
        home  = my_match.home
        guest = my_match.guest
        dialog.ui.home_label.setText(home.name)
        dialog.ui.visiting_label.setText(guest.name)
        dialog.ui.home_team.clear()
        dialog.ui.visiting_team.clear()
        dialog.ui.home_score.display("0")
        dialog.ui.visiting_score.display("0")
        # XXX simplify
        TOP = 100
        INC = 14
        G   = 15
        top = TOP
        buttons = []
        for player in self.tournament.teams[home.name].players:
            player_data = self.tournament.teams[home.name].players[player]
            v = "%s  %s  %s" % (player, player_data.name, player_data.surname)
            dialog.ui.home_team.addItem(v)
            button = QPushButton("+", dialog)
            buttons.append(button)
            button.setGeometry(48, top, G, G)
            button.clicked.connect(partial(self.click_plus, player))
            button = QPushButton("-", dialog)
            buttons.append(button)
            button.setGeometry(23, top, G, G)
            button.clicked.connect(partial(self.click_minus, player))
            top += INC
        top = TOP
        for player in self.tournament.teams[guest.name].players:
            player_data = self.tournament.teams[guest.name].players[player]
            v = "%s  %s  %s" % (player, player_data.name, player_data.surname)
            dialog.ui.visiting_team.addItem(v)
            button = QPushButton("+", dialog)
            buttons.append(button)
            button.setGeometry(578, top, G, G)
            button.clicked.connect(partial(self.click_plus_guest, player))
            button = QPushButton("-", dialog)
            buttons.append(button)
            button.setGeometry(600, top, G, G)
            button.clicked.connect(partial(self.click_minus_guest, player))
            top += INC
        self.running_match = my_match
        self.running_match.start()
        ret = dialog.exec()
        self.running_match.close()
        self.setup_match_plan()
        for b in buttons:
            b.deleteLater()
        self.show_table(self)

    def click_plus(self, player):
        self.running_match.home_scored(player)
        self.match_dialog.ui.home_score.display(str(self.running_match.running_score[0].value))
        self.live_table()

    def click_minus(self, player):
        self.running_match.home_cancelled(player)
        self.match_dialog.ui.home_score.display(str(self.running_match.running_score[0].value))
        self.live_table()

    def click_plus_guest(self, player):
        self.running_match.guest_scored(player)
        self.match_dialog.ui.visiting_score.display(str(self.running_match.running_score[1].value))
        self.live_table()

    def click_minus_guest(self, player):
        self.running_match.guest_cancelled(player)
        self.match_dialog.ui.visiting_score.display(str(self.running_match.running_score[1].value))
        self.live_table()

#    def _match_selected(self, item):
#        print(self.matchPlan.currentItem().text())
#        print(dir(self.matchPlan.currentItem()))

    def live_table(self):
        """
        displays the live table
        """
        self.show_table(self.match_dialog.ui)

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
        ui = dialog.ui
        t = self.tournament
        ui.match_duration.setValue(t.duration)
        ui.intermission.setValue(t.intermission)
        ui.tournamentName.setText(t.name)
        st = t.start_time
        # FixMe: datatype is totally unclear
        if isinstance(st, datetime.time):
            _time = QTime(st.hour, st.minute)
        else:
            try:
                time = eval(st)
            except TypeError:
                _time = st
        ui.startTime.setTime(_time)
        ret = dialog.exec()
        if not ret:
            return
        if not self._check_tournament_name(ui.tournamentName.text()):
            return
        t.duration     = ui.match_duration.value()
        t.intermission = ui.intermission.value()
        t.name         = ui.tournamentName.text()
        t.start_time   = ui.startTime.time()
        t.store()
        self.setWindowTitle(t.name)
        self.teams_and_schedule.setEnabled(True)

    def _enter_members(self, team:str) -> None:
        dialog = self.member_dialog
        ui     = dialog.ui
        ui.setupUi(dialog)
        row = 0
        _team = self.tournament.teams[team]
        s = ui.member_list.setItem
        for player in _team.players:
            player_data = _team.players[player]
            ui.member_list.insertRow(row)
            s(row, 0, QTableWidgetItem(player))
            s(row, 1, QTableWidgetItem(player_data.name))
            s(row, 2, QTableWidgetItem(player_data.surname))
        ui.add_player.clicked.connect(self._add_player)
        dialog.show()
        ret = dialog.exec()
        if not ret:
            return
        self.tournament.clear_players(team)
        ml = ui.member_list
        for i in range(ml.rowCount()):
            d = [ml.item(i, j).text() for j in range(3)]
            self.tournament.add_player(team, *d)
        self.tournament.store()

    def _add_player(self, *args, **kw) -> None:
        """
        Add a player to a team
        """
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

    def _enter_teams(self) -> None:
        """
        Input of all teams (at least their names), and creates a schedule
        """
        dialog = self.team_dialog
        ui = dialog.ui
        ui.setupUi(dialog)
        for team in self.tournament.teams:
            ui.team_list.addItem(team)
        self._show_schedule()
        ui.addTeam.pressed.connect(self._add_team)
        ui.create_schedule_button.clicked.connect(self._create_schedule)
        ui.switch1.setInputMask("00")
        ui.switch2.setInputMask("00")
        ui.switch_team_idx.setInputMask("00")
        ui.switch_matches.clicked.connect(partial(self._switch_matches, ui))
        ui.switch_teams.clicked.connect(partial(self._switch_home_guest, ui))
        dialog.show()
        ret = dialog.exec()
        if not ret:
            ui.scheduleEditor.clear()
            return
        ui.scheduleEditor.clear()
        self.tournament.show()
        top = 130
        for team in self.tournament.teams:
            pb = QPushButton(team, self.centralwidget)
            pb.move(9, top)
            top += 22
            pb.show()
            pb.clicked.connect(partial(self._enter_members, team))
        self.setup_match_plan()
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

    def _switch_matches(self, ui) -> None:
        """
        Editing the schedule: switch the schedule of two matches
        """
        no_matches = len(self.tournament.schedule.matches)
        # Fixme: code duplication
        try:
            i1 = int(ui.switch1.text())
        except ValueError:
            msg = QErrorMessage()
            msg.showMessage("enter a number for first match")
            msg.exec()
            return
        try:
            i2 = int(ui.switch2.text())
        except ValueError:
            msg = QErrorMessage()
            msg.showMessage("enter a number for second match")
            msg.exec()
            return

        if not 1 <= i1 <= no_matches:
            print("shit home")
            return
        if not 1 <= i2 <= no_matches:
            print("shit guest")
            return

        self.tournament.schedule.switch_matches(i1, i2)
        self._show_schedule()

    def _switch_home_guest(self, ui:Ui_TeamAndScheduleEditor) -> None:
        try:
            idx = int(ui.switch_team_idx.text())
        except ValueError:
            msg = QErrorMessage()
            msg.showMessage("enter a number for match")
            msg.exec()
            return
        no_matches = len(self.tournament.schedule.matches)
        if not 1 <= idx <= no_matches:
            print("shit switch")
            return
        self.tournament.schedule.switch_home_guest(idx)
        self._show_schedule()
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
        """
        creates a simple schedule for the tournament
        """
        ui = self.team_dialog.ui
        self.tournament.clear_teams()
        ui.scheduleEditor.clear()
        for team in self._actual_team_list():
            self.tournament.add_team(team)
        self.tournament.create_schedule()
        self.tournament.store()
        self._show_schedule()


    def _show_schedule(self) -> None:
        ui = self.team_dialog.ui
        mp = ui.scheduleEditor
        mp.setRowCount(len(self.tournament.schedule.matches))
        row = 0
        w   = QTableWidgetItem
        for match in self.tournament.schedule.matches.values():
            mp.setItem(row, 0, w(str(match.starts)))
            mp.setItem(row, 1, w(match.home.name))
            mp.setItem(row, 2, w(match.guest.name))
            mp.setItem(row, 3, w(":".join((
                                 str(match.running_score[0].value),
                                 str(match.running_score[1].value)))))
            row += 1
        mp.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        mp.show()


def main_GUI():
    roster = QApplication(sys.argv)
    gui    = Window()
    gui.show()
    return roster, gui


if __name__ == "__main__":
    app, ui = main_GUI()
    sys.exit(app.exec())
