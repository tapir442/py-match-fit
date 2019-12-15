import sys

import random


import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout, QTableWidget, QLabel,  QTableWidgetItem, QComboBox, QTableView, QTableWidget, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtCore import QSize, Qt, QEvent, QObject


class ClickableQTabWidget(QTabWidget):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit()    


class textView(QWidget):
    def __init__(self, tabs):
        super(textView, self).__init__()
        self.theWindow = QWidget ()
        self.tabs = tabs

        teams = []
        for idx in range (int(sys.argv[1])) :
            teams.append (self.tabs.tabBar().tabText (idx))
        
        no_teams        = int(sys.argv[1])
        games_per_round = int(no_teams//2)
        no_rounds       = no_teams if no_teams % 2 == 1 else no_teams - 1
        self.t = t = QTableWidget (games_per_round * no_rounds, 3, self.theWindow)
        self.theWindow.layout=QVBoxLayout (self)
        self.theWindow.layout.addWidget (t)
        import datetime
        start_time      = 8
        start           = datetime.time (start_time)
        start           = datetime.datetime(2000, 1, 1, 8, 0, 0)
        len_of_game     = 12
        len_of_break    = 3
        duration        = datetime.timedelta (hours = 0, minutes = len_of_game + len_of_break)
        self._cb_table  = []
        for i in range (games_per_round * no_rounds) :
            t.setItem(i, 0, QTableWidgetItem (start.strftime ("%H:%M")))
            start = start + duration
            cb1  = QComboBox()
            for team in teams :
                cb1.addItem (team, team)

            cb2 = QComboBox()
            for team in teams :
                cb2.addItem (team, team)                


            self._cb_table.append ((cb1, cb2))
            
            
            t.setCellWidget (i, 1,   cb1)
            t.setCellWidget (i, 2,   cb2)

        self.close_button = QPushButton ("Close and validate")
        self.theWindow.layout.addWidget (self.close_button)
        self.close_button.clicked.connect(self.validate)

    def validate (self) :
        valtable = {"A-TEAM" : set (),
                    "B-TEAM" : set (),
                    "C-TEAM" : set (),
                    "D-TEAM" : set (),
                    "E-TEAM" : set (),
                    }
        for e in self._cb_table :
            valtable [e [0].currentText()].add (e[1].currentText ())
            valtable [e [1].currentText()].add (e[0].currentText ())
            
        # validation step
        all_teams = set (valtable.keys ())
        for team, opponents in valtable.items () :
            print (team, opponents)
            valid = all_teams - opponents == set ([team])
            if not valid :
                print ("%s has a problem: (%s)" % (team, opponents))

        
        
class MatchView (QWidget) :
    def __init__ (self)  :
        super(MatchView, self).__init__()
        self.theWindow = QWidget ()  
        t = QTableWidget (12, 6, self.theWindow)
        self.theWindow.layout=QVBoxLayout (self)
        self.theWindow.layout.addWidget (t)

    def handleEvents (self, event) :
        print (event)

    def event (self, event):
        print (event)


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
        self.layout    = QVBoxLayout()
        self.tabs      = ClickableQTabWidget ()
        self.tabs.resize (800, 600)        
        self._tabs = []        
        for i in range (int(sys.argv [1])) :
            w     = QWidget()
            table = QTableWidget(20, 3, w)
            self._tabs.append (table)            
            table.setHorizontalHeaderLabels(["Vorname", "Name", "Tore"])            
            table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
            table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
            table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignRight) 
            self.tabs.addTab (w, "Team %s" % (i+1))
            w.layout = QVBoxLayout(self)
            w.layout.addWidget (table)
            w.setLayout (w.layout)            
        self.layout.addWidget (self.tabs)
        self.setLayout(self.layout)        

        schedule_button = QPushButton ("Create Schedule")
        self.layout.addWidget (schedule_button)
        schedule_button.clicked.connect(self.clickSchedule)

        match_button = QPushButton ("Start Match")
        self.layout.addWidget (match_button)
        match_button.clicked.connect(self.clickMatch)

        self.blitztabelle = QTableWidget (self)
        self.layout.addWidget (self.blitztabelle)
        self.blitztabelle.setRowCount(int(sys.argv[1]))
        self.blitztabelle.setColumnCount(8)
        
        self.blitztabelle.setHorizontalHeaderLabels(["team", "Spiele", "Siege",
                                                                  "Unentschieden", "Niederlagen"
                                                                  ,"Tore", "Differenz", "Punkte"]
                                                   )
        
        self.torschuetzen = QTableWidget (self)
        self.layout.addWidget (self.torschuetzen)
        self.installEventFilter(self)

        self.tabs.clicked.connect(self.onClicked)

    def onClicked(self):
        from pprint import pprint
        pprint (dir(self.tabs.tabBar()))
        idx        = self.tabs.tabBar().currentIndex()
        dialog     = QInputDialog()
        result, ok = dialog.getText(self, 'Text Input Dialog', 'Enter your name:')
        if ok :
            self.tabs.tabBar().setTabText (idx, result)

        
    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                print("Right button clicked")
        return False        

    def change_name_of_team(self) :
        pass

    @pyqtSlot()
    def on_doubleclick(self):
        print("A"*99)        
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())        
    def clickSchedule (self, *args, **kw) :
        self.t = textView (self.tabs)
        self.t.show ()
        
    def clickMatch (self, *args, **kw) :
        self.m = MatchView ()
        self.m.show ()


from enum import Enum, auto
class Match_State (Enum):
    waiting  = auto()
    running  = auto()
    finished = auto()

class Match (object) :    
    def __init__ (self, team1, team2) :
        self._teams  = [team1, team2, 0, 0]
        self._state  = Match_State.waiting
        
    def close (self) :
        self._state    = Match_State.finished 

    def start (self) :
        self._state    = Match_State.running
        
    def goal (self, team, number) :
        if self._teams [0]._name == team :
            self._teams [2] += 1
        else :
            self._teams [3] += 1
        Team.pool [team].goal (number)

    def draw (self) :
        return self._teams [2] == self._teams [3]


    def winner(self):
        """Returns the winning team"""
        if self._teams [2] >= self._teams [3]:
            return (self._teams [0], self._teams [2])
        return (self._teams [1], self._teams [3])

    def loser(self):
        """Returns the losing team"""
        if self._teams [2] >= self._teams [3]:
            return (self._teams [1], self._teams [3])
        return (self._teams [0], self._teams [2])
    
    
class Model(object):
    def __init__(self):
        self.observers      = []
        self.teams          = {}
        self.schedule_table = []
        self._running       = -1
    def init_team (self, name) :
        self.teams [name] = Team (name)

    def add_player (self, team, number, name, surname) :
        self.teams [team].add_player (number, name, surname)

    def create_schedule (self) :
        self.schedule_table = [ Match (self.teams ["Rapid"], self.teams ["Austria"])
                              , Match (self.teams ["Bayern"], self.teams ["Ajax"])
                              , Match (self.teams ["Austria"], self.teams ["Bayern"])
                              , Match (self.teams ["Rapid"], self.teams ["Ajax"])
                              , Match (self.teams ["Austria"], self.teams ["Ajax"])
                              , Match (self.teams ["Rapid"], self.teams ["Bayern"])  
           ]

    def start_match (self) :
        self._running += 1
        self.schedule_table [self._running].start ()
        self.notify ()
        
    def close_match (self) :
        self.schedule_table [self._running].close ()
        
    def register_observer(self, observer):
        self.observers.append(observer)

    def notify(self):
        [observer.update() for observer in self.observers]

    def goal (self, team, number) :
        match = self.schedule_table [self._running]
        match.goal (team, number)
        self.notify ()

    def cancel_goal (self, team, number) :
        self.teams [team].cancel_goal (number)
        self.notify ()

    def table (self) :
        result     = []
        shot_idx   = 0
        got_idx    = 1
        points_idx = 2
        teams      = {}
        for i in self.schedule_table :
            if i._teams [0]._name not in teams :
                teams[i._teams [0]._name] = [0, 0, 0]
            if i._teams [1]._name not in teams :
                teams[i._teams [1]._name] = [0, 0, 0]
            if i._state == Match_State.waiting :
                continue

            if i.draw ():
                teams[i._teams [0]._name][points_idx] += 1
                teams[i._teams [1]._name][points_idx] += 1
                teams[i._teams [0]._name][shot_idx]   += i._teams [2]
                teams[i._teams [1]._name][shot_idx]   += i._teams [2]
                teams[i._teams [0]._name][got_idx]    += i._teams [3]
                teams[i._teams [1]._name][got_idx]    += i._teams [3]
            else :
                winner = i.winner ()
                loser  = i.loser ()
                teams[winner[0]._name][points_idx] += 3
                teams[winner[0]._name][shot_idx]   += winner[1]
                teams[winner[0]._name][got_idx]    += loser [1]
                teams[loser [0]._name][shot_idx]   += loser [1]
                teams[loser [0]._name][got_idx]    += winner[1]
        result = [ (x, *teams [x]) for x in teams ]
        result.sort (key = lambda x: (x [points_idx+1], x[shot_idx+1] - x[got_idx+1], x[shot_idx+1]), reverse = True)
        return (x for x in result)

    def scorer (self) :
        scorers = []
        for team in self.teams :
            for player in self.teams[team]._players :
                _player = self.teams[team]._players [player]
                scorers.append ((_player [2], _playeter [0], _player [1], team))
        scorers.sort (reverse = True)
        return [x for x in scorers if x [0] > 0]

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
        
#    def show(self):
#        from pprint import pprint
#        for x in data.table  ():
#            self.table_widget.torschuetzen = QTableWidget (10, 4, self)                
#        for x in data.scorer ():
#            pass

class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view  = view
        self.model.register_observer(self)

    def update(self):
        print ("A"*99)
        self.view.show(self.model)

if __name__ == "__main__" :
    model = Model()
    app = QApplication(sys.argv)    
    gui = GUI()
    ctrl = Controller(model, gui)
    sys.exit(app.exec_())

model.init_team ("Rapid")
model.add_player ("Rapid", 1, "Funki", "Feurer")
model.add_player ("Rapid", 2, "Hannes", "Pregesbauer")
model.add_player ("Rapid", 4, "Egon", "Pajenk")
model.add_player ("Rapid", 9, "Hans", "Krankl")
model.add_player ("Rapid", 10, "Bjoern", "Bjeregaard")

model.init_team  ("Austria")
model.add_player ("Austria", 1, "Hannes", "Schreitl")
model.add_player ("Austria", 2, "Robert", "Sara")
model.add_player ("Austria", 4, "Josef", "Sara")
model.add_player ("Austria", 8, "Herbert", "Prohaska")
model.add_player ("Austria", 9, "Tibor", "Nylasi")

model.init_team  ("Bayern")
model.add_player ("Bayern", 1, "Olli",   "Kahn")
model.add_player ("Bayern", 4, "David", "Alaba")
model.add_player ("Bayern", 10, "Gerd", "Müller")
model.add_player ("Bayern", 9, "Claudio", "Pizarro")
model.add_player ("Bayern", 5, "Thomas", "Müller")

model.init_team  ("Ajax")
model.add_player ("Ajax", 1, "Peter", "Schmeichl")
model.add_player ("Ajax", 9, "Marco", "van Basten")
model.add_player ("Ajax", 10, "Ruud", "Gullit")
model.add_player ("Ajax",  6, "Clarence", "Seedorf")
                  
model.create_schedule ()

model.start_match ()

model.goal ("Rapid", 4)
model.goal ("Rapid", 4)
model.goal ("Rapid", 4)
model.goal ("Rapid", 4)
model.goal ("Austria", 4)
model.goal ("Austria", 8)
model.goal ("Austria", 2)
model.goal ("Austria", 2)
model.goal ("Austria", 9)

print ("=====================")
model.close_match ()
model.start_match ()
model.goal ("Bayern", 9)
model.goal ("Bayern", 9)
model.goal ("Rapid", 9)
print ("=====================")
model.close_match ()
model.start_match ()
print ("=====================")
model.close_match ()
model.start_match ()
print ("=====================")
model.close_match ()
model.start_match ()
print ("=====================")
model.close_match ()
model.start_match ()

