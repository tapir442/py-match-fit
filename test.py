import sys

import random


import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout, QTableWidget, QLabel,  QTableWidgetItem, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QSize, Qt

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 tabs - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        self.show()

class MyTableWidget(QWidget):        
    def __init__(self):
        QWidget.__init__(self)
        self.layout    = QVBoxLayout()

        self.tabs      = QTabWidget ()
        self.tabs.resize (800, 600)        
        self._tabs = []        
        for i in range (int(sys.argv [1])) :
            w = QWidget()
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
        self.torschuetzen = QTableWidget (10, 4, self)    
        self.setLayout(self.layout)        

        schedule_button = QPushButton ("Create Schedule")
        self.layout.addWidget (schedule_button)
        schedule_button.clicked.connect(self.clickSchedule)

        match_button = QPushButton ("Start Match")
        self.layout.addWidget (match_button)
        match_button.clicked.connect(self.clickMatch)
        
        
    def magic(self):
        self.text.setText(random.choice(self.hello))

    def clickSchedule (self, *args, **kw) :
        self.t = textView ()
        self.t.show ()
        
    def clickMatch (self, *args, **kw) :
        self.m = MatchView ()
        self.m.show ()
        

        
class textView(QWidget):
    def __init__(self):
        super(textView, self).__init__()
        self.theWindow = QWidget ()

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
            cb1.addItem ("A-TEAM", "A-TEAM")
            cb1.addItem ("B-TEAM", "B-TEAM")
            cb1.addItem ("C-TEAM", "C-TEAM")
            cb1.addItem ("D-TEAM", "D-TEAM")
            cb1.addItem ("E-TEAM", "E-TEAM")

            cb2 = QComboBox()
            cb2.addItem ("A-TEAM", "A-TEAM")
            cb2.addItem ("B-TEAM", "B-TEAM")
            cb2.addItem ("C-TEAM", "C-TEAM")
            cb2.addItem ("D-TEAM", "D-TEAM")
            cb2.addItem ("E-TEAM", "E-TEAM")

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyTableWidget()
    widget.show()
    sys.exit(app.exec_())
		
def main():
   app = QApplication(sys.argv)
   ex = tabdemo()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()
