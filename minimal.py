import sys
from pprint import pprint
import random
import datetime

import sys
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout, QGridLayout, QTableWidget, QLabel,  QTableWidgetItem, QComboBox, QTableView, QTableWidget, QInputDialog, QDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtCore import QSize, Qt, QEvent, QObject, QAbstractTableModel

from model import Model, Match

class ClickableQTabWidget(QTabWidget):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit()

import operator
def fixtures(teams):
    if len(teams) % 2:
        teams.append('Day off')  # if team number is odd - use 'day off' as fake team
    rotation = list(teams)       # copy the list
    fixture = []
    for i in range(0, len(teams)-1):
        fixture.append(rotation)
        rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]
    return fixture
# end def fixtures

class Torschuetzen (QTableWidget) :
    def __init__ (self, parent = None) :
        super ().__init__ (parent)
        self.setWindowTitle ("Torschützen")
        self.parent = parent

    def update (self, model, idx = 0) :
        print ("tupdate")

class Tabelle (QTableWidget) :
    def __init__ (self, no_teams, parent = None) :
        super ().__init__()
        self.setRowCount (no_teams)
        self.setColumnCount(8)
        self.setWindowTitle ("Tabelle")
        self.setHorizontalHeaderLabels(["team", "#", "S",
                                        "U", "N"
                                        ,"Tore", "Diff", "Punkte"]
                                       )
        header = self.horizontalHeader ()
        for i in range (8) :
            header.setSectionResizeMode(i, PyQt5.QtWidgets.QHeaderView.ResizeToContents)


    def update (self, model, idx = 0) :
        mt = model.table ()
        for i, x in enumerate (mt) :
            self.setItem (i, 0, QTableWidgetItem(x[0]))
            self.setItem (i, 1, QTableWidgetItem(x[1]))
            self.setItem (i, 2, QTableWidgetItem(x[2]))
            self.setItem (i, 3, QTableWidgetItem(x[3]))
            self.setItem (i, 4, QTableWidgetItem(0))
            self.setItem (i, 5, QTableWidgetItem(0))
            self.setItem (i, 6, QTableWidgetItem(0))
            self.setItem (i, 7, QTableWidgetItem(0))
        self.show ()
class textView(QWidget):
    def __init__(self, parent = None):
        super().__init__()
#        self.theWindow = QWidget (parent)
        self.parent     = parent
        no_teams        = self.parent.no_teams
        games_per_round = self.parent.games_per_round
        no_rounds       = self.parent.no_rounds
        self.teams = []
        self.t = QTableWidget (games_per_round * no_rounds, 3, self)
        self.t.setWindowTitle ("Scheduler")
        self.layout=QVBoxLayout (self)
        self.layout.addWidget (self.t)
        self.close_button = QPushButton ("Close and validate")
        self.layout.addWidget (self.close_button)

    def setup (self) :
        self.tabs       = self.parent.tabs
        import datetime
        start_time      = 9
        start           = datetime.time (start_time)
        start           = datetime.datetime(2000, 1, 1, start_time, 0, 0)
        len_of_game     = 12
        len_of_break    = 3
        duration        = datetime.timedelta (hours = 0, minutes = len_of_game + len_of_break)
        teams           = self.parent.team_names
        self._cb_table  = []
        self.teams      = set ()
        for i in self.parent.schedule :
            self.teams.add (i[0])
            self.teams.add (i[1])
        for i in range (len (self.parent.schedule)) :
            self.t.setItem(i, 0, QTableWidgetItem (start.strftime ("%H:%M")))
            start = start + duration
            cb1  = QComboBox()
            anchor = self.parent.schedule [i][0]
            cb1.addItem (anchor, anchor)
            for team in self.teams:
                if team != anchor :
                    cb1.addItem (team, team)

            cb2 = QComboBox()
            anchor = self.parent.schedule [i][1]
            cb2.addItem (anchor, anchor)
            for team in self.teams:
                if team != anchor :
                    cb2.addItem (team, team)
            self._cb_table.append ((cb1, cb2))
            self.t.setCellWidget (i, 1,   cb1)
            self.t.setCellWidget (i, 2,   cb2)

class Team (object) :
    pool = {}
    def __init__ (self, name) :
        self._name        = name
        self.observers    = []
        self._players     = {}
        self.pool  [name] = self

    def set_name (self, name) :
        self._name = name

    def add_player (self, number, name, surname) :
        self._players [number] = [name, surname, 0]

    def delete_player (self, number) :
        try :
            del self._players [number]
        except KeyError :
            pass

    def goal (self, number) :
        self._players [number][2] += 1

    def cancel_goal (self, number) :
        if self._players [number][2] > 0 :
            self._players [number][2] -= 1

    def goals (self) :
        return sum ([self._players[p][2] for p in self._players])
# end class Team


class MyTableWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.layout    = QGridLayout()
        icon_label = QLabel (self)
        pixmap = QPixmap ('1980.jpeg')
        icon_label.setPixmap (pixmap)
        self.layout.addWidget (icon_label, 1,3)
#        icon_label.show ()
        self.tabs      = ClickableQTabWidget ()
        self.layout.addWidget (self.tabs, 1,1)
        self.tabs.resize (1000, 800)
        self._tabs = []
        self.setLayout(self.layout)


        schedule_button = QPushButton ("Turnierplan ändern")
        self.layout.addWidget (schedule_button, 1, 2)
        schedule_button.clicked.connect(self.clickSchedule)

#        match_button = QPushButton ("Start Match")
#        self.layout.addWidget (match_button)
#        match_button.clicked.connect(self.clickMatches)
        self.tournament = TournamentManager (self)
        self.layout.addWidget (self.tournament, 2,1)

        self.match = MatchManager \
            (self, Match ("1", "2"), self.tabs)
        self.layout.addWidget (self.match, 2,2)

#        self.scheduler = ScheduleViewer (self)
#        self.layout.addWidget (self.tournament, 2,1)
        self.blitztabelle = Tabelle (len(sys.argv[1:]), self)
        self.layout.addWidget (self.blitztabelle, 3,1)
#        self.blitztabelle.setRowCount(self.no_teams)

        self.torschuetzen = Torschuetzen (self)
        self.layout.addWidget (self.torschuetzen, 3, 2)

        self.no_teams = len(sys.argv[1:])
        self.games_per_round = int(self.no_teams//2)
        self.no_rounds       = self.no_teams if self.no_teams % 2 == 1 else self.no_teams - 1
        self.len_of_game     = 12
        self.len_of_break    = 3
        self.start_time      = 8
        self.start           = datetime.datetime(2000, 1, 1, self.start_time, 0, 0)
        self.duration        = datetime.timedelta (hours = 0, minutes = self.len_of_game + self.len_of_break)
        self.t = textView (self)
        from pprint import pprint

        self.installEventFilter(self)
        self.tabs.clicked.connect(self.onClicked)

    def set_tabs (self, team_list) :
        self.team_names      = team_list [:]
        for i in range (self.no_teams) :
            table = QTableWidget(20, 3, self.tabs)
            self._tabs.append (table)
            table.setHorizontalHeaderLabels(["Vorname", "Name", "Tore"])
            table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
            table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
            table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignRight)
            self.tabs.addTab (table, team_list [i])
        import itertools
        matches = fixtures (self.team_names)
        self.schedule = []
        for f in matches :
            n = len(f)
            v = [x for x in zip(f[:n//2], reversed (f[n//2:]))]
            self.schedule.append (v)
        r = []
        for x in self.schedule :
            for y in x :
                if (y[0] != "Day off") and (y[1] != "Day off") :
                    r.append (y)
        self.schedule = list(r)

    def onClicked(self):
        idx        = self.tabs.tabBar().currentIndex()
        dialog     = QInputDialog()
        result, ok = dialog.getText(self, 'Text Input Dialog', 'Enter your name:')
        if ok :
            self.tabs.tabBar().setTabText (idx, result)

    def update (self, model, idx = 0) :
        self.tournament.update   (model, idx)
        self.blitztabelle.update (model, idx)
        self.torschuetzen.update (model, idx)

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                print("Right button clicked")
        return False

    def change_name_of_team(self) :
        pass

    @pyqtSlot()
    def on_doubleclick(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
    def clickSchedule (self, *args, **kw) :
#        self.t.setup ()
        self.t.show ()

    def clickMatches (self, *args, **kw) :
        self.m = ScheduleViewer (self)
        self.m.show ()

class TournamentManager (QTableWidget):
    def __init__ (self, parent) :
        super ().__init__ (20, 3)
        self.setWindowTitle ("Tournament Manager")
        self.parent = parent

    def start_match (self, idx) :
        self.match = MatchManager \
            (self, Match (self.parent.schedule [idx][0], self.parent.schedule [idx][1]), self.parent.tabs)

    def update (self, model, idx) :
        for i in range (len (model.schedule_table)) :
            self.setItem(i, 0, QTableWidgetItem (str(model.schedule_table[i].home())))
            self.setItem(i, 1, QTableWidgetItem (str(model.schedule_table[i].guest())))

class MatchManager (QTableWidget) :
    def __init__ (self, parent, match, tabs) :
        super (MatchManager).__init__()
        self.parent = parent
        self.match  = match
        self.tabs   = tabs
        super().__init__ (20, 6)

    def update (self, model, idx) :
        self.team1 = team1 = model.schedule_table [idx].home ()
        self.team2 = team2 = model.schedule_table [idx].guest()
        team1_index = [index for index in range(self.tabs.count())
                if team1._name == self.tabs.tabText(index)][0]
        team2_index = [index for index in range(self.tabs.count())
                if team2._name == self.tabs.tabText(index)][0]

        team1_widget = self.tabs.widget (team1_index)
        team2_widget = self.tabs.widget (team2_index)
        self.setHorizontalHeaderLabels(["", "", team1._name, team2._name, "", ""])
        for i in range (team1_widget.rowCount ()) :
            e1 = team1_widget.item (i, 0).text () if team1_widget.item (i, 0) else ""
            e2 = team1_widget.item (i, 1).text () if team1_widget.item (i, 1) else ""
            if not (e1 or e2) :
                continue
            self.setItem(i, 0, QTableWidgetItem ("-"))
            self.setItem(i, 1, QTableWidgetItem ("+"))            
            self.setItem(i, 2, QTableWidgetItem ("%s" % (i+1)))

        for i in range (team2_widget.rowCount ()) :
            e1 = team2_widget.item (i, 0).text () if team2_widget.item (i, 0) else ""
            e2 = team2_widget.item (i, 1).text () if team2_widget.item (i, 1) else ""
            if not (e1 or e2) :
                continue
            self.setItem(i, 3, QTableWidgetItem ("%s" % (i+1)))
            self.setItem(i, 4, QTableWidgetItem ("+"))
            self.setItem(i, 5, QTableWidgetItem ("-"))

        header = self.horizontalHeader ()
        for i in range (6) :
            header.setSectionResizeMode(i, PyQt5.QtWidgets.QHeaderView.ResizeToContents)
    # end def __init__


class ScheduleViewer (QTableWidget) :
    def __init__ (self, parent = None) :
        super ().__init__ (len(parent.schedule), 4)
        self.parent = parent
        self.buttons = []
        for i in range (len(parent.schedule)) :
            self.setItem(i, 0, QTableWidgetItem (parent.schedule [i][0]))
            self.setItem(i, 1, QTableWidgetItem (parent.schedule [i][1]))
            self.buttons.append (QPushButton ("Start"))
            self.buttons[i].clicked.connect(self.notifyme)

#            if i > 0 :
#                self.buttons [i].setEnabled(False)
            self.setCellWidget(i,2, self.buttons [i])
#            stop  = QPushButton ("Stop")
#            stop.setEnabled(False)
#            self.setCellWidget(i,3, stop)
        self.match_index = 0

    def notifyme (self):
        heim      = self.parent.schedule [self.match_index][0]
        auswaerts = self.parent.schedule [self.match_index][1]

        match = MatchManager (self, Match (heim, auswaerts), self.parent.tabs)
        match.show ()

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 tabs - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width  = 1020
        self.height = 920
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyTableWidget()
        self.setCentralWidget(self.table_widget)
        self.show ()

class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view  = view
        self.model.register_observer(self)
        self.connect_signals ()
        self.init ()

    def init (self) :
        for i in sys.argv [1:] :
            self.model.init_team (i)
        self.view.table_widget.set_tabs ([x for x in self.model.teams.keys ()])
        self.view.table_widget.t.setup ()

    def start_match(self, idx) :
        """get the index of the clicked line"""
        row   = idx.row()
        model = idx.model()
        self.model.start_match (row)
        self.view.table_widget.update (self.model, row)
        self.view.table_widget.match.update (self.model, row)

    def set_schedule(self):
        result = None
        t = self.view.table_widget.t
        valtable = dict ((x, set()) for x in t.teams)
        for e in t._cb_table :
            valtable [e [0].currentText()].add (e[1].currentText ())
            valtable [e [1].currentText()].add (e[0].currentText ())

        # validation step
        all_teams = set (valtable.keys ())
        for team, opponents in valtable.items () :
            valid = all_teams - opponents == set ([team])
            if not valid :
                print ("%s has a problem: (%s)" % (team, opponents))
            else :
                result = [(e [0].currentText(), e[1].currentText ()) for e in t._cb_table]
                self.model.create_schedule (result)
                self.view.table_widget.tournament.update (self.model, 0)
                self.view.table_widget.match.update (self.model, 0)
                self.view.table_widget.blitztabelle.update (self.model, 0)
    # end def validate

    def connect_signals (self) :
        self.view.table_widget.tournament.clicked.connect (self.start_match)
        self.view.table_widget.t.close_button.clicked.connect (self.set_schedule)
        self.view.table_widget.match.clicked.connect (self.goal)
        self.view.table_widget.tabs.currentChanged.connect (self.players)


    def players (self, idx):
        res = []
        tab  = self.view.table_widget.tabs.widget (idx)
        team = self.view.table_widget.tabs.tabText(idx)
        for i in range (tab.rowCount ()) :
            e1 = tab.item (i, 0).text () if tab.item (i, 0) else ""
            e2 = tab.item (i, 1).text () if tab.item (i, 1) else ""
            if not (e1 or e2) :
                continue
            print (e1, e2)
            self.model.add_player (team, i + 1, e1, e2)
            
    def goal(self, idx) :
        player_number, column = (idx.row(), idx.column())
        item = self.view.table_widget.match.rowAt (idx.row())
#        pprint (item)
        if column in (0,1) :
            team = self.model.schedule_table [self.model.running()].home()
        else :
            team = self.model.schedule_table [self.model.running()].guest()
        print ("Team:::::", team)
        self.model.goal (team._name, player_number + 1)
        self.view.table_widget.blitztabelle.update (self.model, 0)
        
if __name__ == "__main__" :
    model = Model()
    app   = QApplication(sys.argv)
    gui   = GUI()
    ctrl  = Controller(model, gui)
    sys.exit(app.exec_())

#model.init_team ("Rapid")
#model.add_player ("Rapid", 1, "Funki", "Feurer")
#model.add_player ("Rapid", 2, "Hannes", "Pregesbauer")
#model.add_player ("Rapid", 4, "Egon", "Pajenk")
#model.add_player ("Rapid", 9, "Hans", "Krankl")
#model.add_player ("Rapid", 10, "Bjoern", "Bjeregaard")

#model.init_team  ("Austria")
#model.add_player ("Austria", 1, "Hannes", "Schreitl")
#model.add_player ("Austria", 2, "Robert", "Sara")
#model.add_player ("Austria", 4, "Josef", "Sara")
#model.add_player ("Austria", 8, "Herbert", "Prohaska")
#model.add_player ("Austria", 9, "Tibor", "Nylasi")

#model.init_team  ("Bayern")
#model.add_player ("Bayern", 1, "Olli",   "Kahn")
#model.add_player ("Bayern", 4, "David", "Alaba")
#model.add_player ("Bayern", 10, "Gerd", "Müller")
#model.add_player ("Bayern", 9, "Claudio", "Pizarro")
#model.add_player ("Bayern", 5, "Thomas", "Müller")

#model.init_team  ("Ajax")
#model.add_player ("Ajax", 1, "Peter", "Schmeichl")
#model.add_player ("Ajax", 9, "Marco", "van Basten")
#model.add_player ("Ajax", 10, "Ruud", "Gullit")
#model.add_player ("Ajax",  6, "Clarence", "Seedorf")

#model.create_schedule ()

#model.start_match ()

#model.goal ("Rapid", 4)
#model.goal ("Rapid", 4)
#model.goal ("Rapid", 4)
#model.goal ("Rapid", 4)
#model.goal ("Austria", 4)
#model.goal ("Austria", 8)
#model.goal ("Austria", 2)
#model.goal ("Austria", 2)
#model.goal ("Austria", 9)

#print ("=====================")
#model.close_match ()
#model.start_match ()
#model.goal ("Bayern", 9)
#model.goal ("Bayern", 9)
#model.goal ("Rapid", 9)
#print ("=====================")
#model.close_match ()
#model.start_match ()
#print ("=====================")
#model.close_match ()
#model.start_match ()
#print ("=====================")
#model.close_match ()
#model.start_match ()
#print ("=====================")
#model.close_match ()
#model.start_match ()
