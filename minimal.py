import sys
from pprint import pprint
import random
import datetime

import sys
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout, QGridLayout, QTableWidget, QLabel,  QTableWidgetItem, QComboBox, QTableView, QTableWidget, QInputDialog, QDialog,QRadioButton, QMessageBox, QLCDNumber
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
        self.setRowCount   (15)
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Spieler", "Team", "Tore"])


    def update (self, model, idx = 0) :
        if len (model.scorer ()) == 0 :
            for i in range (15) :
                self.setItem (i, 0,  QTableWidgetItem(""))
                self.setItem (i, 1,  QTableWidgetItem(""))
                self.setItem (i, 2,  QTableWidgetItem(""))
            return
        i = 0
        for x in model.scorer () :
            if i < 15 :
                self.setItem (i, 0,  QTableWidgetItem(" ".join (x[1:3])))
                self.setItem (i, 1,  QTableWidgetItem(x[-1]))
                self.setItem (i, 2,  QTableWidgetItem(str(x[0])))
            i += 1

class Tabelle (QTableWidget) :
    def __init__ (self, no_teams, parent = None) :
        super ().__init__()
        self.setRowCount (no_teams)
        self.setColumnCount(9)
        self.setWindowTitle ("Tabelle")
        self.setHorizontalHeaderLabels(["team", "#", "S",
                                        "U", "N"
                                        ,"Tore", "Erh.", "Diff", "Punkte"]
                                       )
        header = self.horizontalHeader ()
        for i in range (8) :
            header.setSectionResizeMode(i, PyQt5.QtWidgets.QHeaderView.ResizeToContents)


    def update (self, model, idx = 0) :
        mt = model.table ()
        for i, x in enumerate (mt) :
            y = [str(_) for _ in x]
            for j in range (len(y)) :
                self.setItem (i, j, QTableWidgetItem(y[j]))
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


        w        = QWidget ()
        w.layout = QGridLayout ()
        self.schedule_button = QPushButton ("Turnierplan")
        w.layout.addWidget (self.schedule_button, 1 ,1)
        self.schedule_button.clicked.connect(self.clickSchedule)

        self.result_home  = QLCDNumber (2, w)
        self.result_home.setDecMode ()
        w.layout.addWidget (self.result_home, 1 ,2)        
        self.result_guest = QLCDNumber (2, w)
        self.result_guest.setDecMode ()        
        w.layout.addWidget (self.result_guest, 1 ,3)
        w.show ()
        w.setLayout (w.layout)
        self.layout.addWidget (w, 1, 2)
                
#        match_button = QPushButton ("Start Match")
#        self.layout.addWidget (match_button)
#        match_button.clicked.connect(self.clickMatches)
        self.tournament = TournamentManager (self)
        self.layout.addWidget (self.tournament, 2,1)

        self.match = MatchManager \
            (self, Match ("1", "2"), self.tabs)
        self.layout.addWidget (self.match, 2,2)

        self.blitztabelle = Tabelle (len(sys.argv[1:]), self)
        self.layout.addWidget (self.blitztabelle, 3,1)

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

        self.installEventFilter(self)
        self.tabs.clicked.connect(self.onClicked)

    def set_tabs (self, team_list) :
        self.team_names      = team_list [:]
        for i in range (self.no_teams) :
            table = QTableWidget(20, 2, self.tabs)
            self._tabs.append (table)
            table.setHorizontalHeaderLabels(["Vorname", "Name"])
            table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
            table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
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
        super ().__init__ (20, 2)
        self.setWindowTitle ("Tournament Manager")
        self.parent = parent

    def start_match (self, idx) :
        self.match = MatchManager \
            (self, Match (self.parent.schedule [idx][0], self.parent.schedule [idx][1]), self.parent.tabs)


    def update (self, model, idx) :
        for i in range (len (model.schedule_table)) :
            self.setItem(i, 0, QTableWidgetItem (str(model.schedule_table[i].home())))
            self.setItem(i, 1, QTableWidgetItem (str(model.schedule_table[i].guest())))

class MatchManager (QWidget) :
    request = pyqtSignal (int, int)    
    def __init__ (self, parent, match, tabs) :
        super ().__init__(parent)
        self.parent = parent
        self.match  = match
        self.tabs   = tabs
        self.layout      = QGridLayout  ()
        self.mtable      = QTableWidget (20, 6)
        self.startbutton = QPushButton ("Start Match")
        self.stopbutton  = QPushButton ("Stop  Match")
        self.layout.addWidget (self.startbutton, 1, 1)
        self.layout.addWidget (self.mtable, 1, 2)
        self.layout.addWidget (self.stopbutton, 1, 3)
        self.setLayout(self.layout)

        
    def clear (self) :
        for i in range (20) :
            for j in range (6) :
                self.mtable.setItem (i, j,QTableWidgetItem( ""))

    def update (self, model, idx) :
        def cellClick (row, column) :
            self.request.emit(row, column)
        self.team1 = team1 = model.schedule_table [idx].home ()
        self.team2 = team2 = model.schedule_table [idx].guest()
        team1_index = [index for index in range(self.tabs.count())
                if team1._name == self.tabs.tabText(index)][0]
        team2_index = [index for index in range(self.tabs.count())
                if team2._name == self.tabs.tabText(index)][0]

        team1_widget = self.tabs.widget (team1_index)
        team2_widget = self.tabs.widget (team2_index)
        self.buttonlist = []
        self.mtable.setHorizontalHeaderLabels(["", "", team1._name, team2._name, "", ""])
        for i in range (team1_widget.rowCount ()) :
            e1 = team1_widget.item (i, 0).text () if team1_widget.item (i, 0) else ""
            e2 = team1_widget.item (i, 1).text () if team1_widget.item (i, 1) else ""
            if (e1 or e2) :
                column = 0
                btn = QPushButton ("-")                
                self.mtable.setCellWidget(i, column, btn)
                btn.clicked.connect(lambda *args, row=i, column=column: cellClick(row, column))

                column = 1
                btn = QPushButton ("+")
                self.mtable.setCellWidget(i, column, btn)
                btn.clicked.connect(
                    lambda *args, row=i, column=column: cellClick(row, column))
                
                self.mtable.setItem(i, 2, QTableWidgetItem ("%s" % (i+1)))
            else :
                self.mtable.setItem(i, 0, QTableWidgetItem (""))
                self.mtable.setItem(i, 1, QTableWidgetItem (""))
                self.mtable.setItem(i, 2, QTableWidgetItem (""))


        for i in range (team2_widget.rowCount ()) :
            e1 = team2_widget.item (i, 0).text () if team2_widget.item (i, 0) else ""
            e2 = team2_widget.item (i, 1).text () if team2_widget.item (i, 1) else ""
            if (e1 or e2) :
                column = 3
                self.mtable.setItem(i, column, QTableWidgetItem ("%s" % (i+1)))

                column = 4
                btn = QPushButton ("+")
                btn.clicked.connect(lambda *args, row=i, column=column: cellClick(row, column))
                self.mtable.setCellWidget(i, column, btn)

                column = 5
                btn = QPushButton ("-")
                btn.clicked.connect(lambda *args, row=i, column=column: cellClick(row, column))                
                self.mtable.setCellWidget(i, column, btn)                

#                self.mtable.setItem(i, 5, QTableWidgetItem (QPushButton ("-")))
            else :
                self.mtable.setItem(i, 3, QTableWidgetItem (""))
                self.mtable.setItem(i, 4, QTableWidgetItem (""))
                self.mtable.setItem(i, 5, QTableWidgetItem (""))


        header = self.mtable.horizontalHeader ()
        for i in range (6) :
            header.setSectionResizeMode(i, PyQt5.QtWidgets.QHeaderView.ResizeToContents)
        self.show()        
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
        self.title = '1980 Wien - Turniermanager'
        self.left = 0
        self.top = 0
        self.width  = 1720
        self.height = 1120
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
        self.view.table_widget.update       (self.model, row)
        self.view.table_widget.match.clear  ()
        self.view.table_widget.match.update (self.model, row)

    def change_model (self, *args, **kw) :
        print ("change :", args, kw)

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

    def stop_match (self, *args, **kw) :
        v = QMessageBox.question( self.view.table_widget.match
                                  , "Schluuspfiff ","Do ya realy wanna quit ?"
                                , QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                                )
        if v == QMessageBox.Yes :
            self.view.table_widget.match.clear ()
        
        
    def start_match_really (self, *args, **kw) :
        print ("Start really :", args, kw)


    def connect_signals (self) :
        self.view.table_widget.tournament.clicked.connect (self.start_match)
        self.view.table_widget.match.startbutton.clicked.connect (self.start_match_really)
        self.view.table_widget.match.stopbutton.clicked.connect (self.stop_match)

        self.view.table_widget.match.request.connect (self.goal)
        self.view.table_widget.t.close_button.clicked.connect (self.set_schedule)

#        self.view.table_widget.match.goal.goalShot.connect (self.goal)
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
            self.model.add_player (team, i + 1, e1, e2)

#    @pyqtSlot (int, int)
    def goal(self, row, column) :
#        if not self.view.table_widget.match.stopbutton.isChecked () :
#            return
        player_number, column = (row + 1, column)
        item = self.view.table_widget.match.mtable.rowAt (row)

        if column in (0,1) :
            team = self.model.schedule_table [self.model.running()].home()
        elif  column in (4,5) :
            team = self.model.schedule_table [self.model.running()].guest()
        else :
            return
        print ("team:", team._name, row, column)
        if column in (0,5) :
#            print ("Cancel ", team._name, player_number)
            self.model.cancel_goal (team._name, player_number)
        else :
#            print ("Goal ", team._name, player_number)            
            self.model.goal (team._name, player_number)
        self.view.table_widget.blitztabelle.update (self.model, 0)
        self.view.table_widget.torschuetzen.update (self.model, 0)
        idx = self.model.running ()
        match = model.schedule_table [idx]
        print ("====>", match._teams [2], match._teams [3])
        self.view.table_widget.result_home.display  (match._teams [2])
        self.view.table_widget.result_guest.display (match._teams [3])
        
if __name__ == "__main__" :
    model = Model()
    app   = QApplication(sys.argv)
    gui   = GUI()
    ctrl  = Controller(model, gui)
    sys.exit(app.exec_())


