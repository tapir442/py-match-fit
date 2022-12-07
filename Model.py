from enum import Enum, auto

from statemachine import StateMachine, State

class Tournament_Machine(StateMachine):
    tabula_rasa    = State("tabula_rasa", initial=True)
    params         = State("params")
#    parameters_set = State("parameters_set")
#    teams_set      = State("teams_set")
 #   scheduled      = State("scheduled")
#    match_ready    = State("match_ready")
#    match_running  = State("match_running")
#    match_finished = State("match_finished")
#    finished       = State("finished")

    enter_params   = tabula_rasa.to(params)

    def on_enter_params(self, disable=None, enable=None, *args, **kw):
        print(locals())
        print("on_enter_params")


import itertools
import datetime
import json

import Match

from PyQt6.QtCore import QSize, Qt, QEvent, QObject, QAbstractTableModel, QAbstractListModel

class Tournament:
    def __init__(self):
        self.StateMachine = Tournament_Machine()
        self.name         = "No Tournament given"
        self.duration     = 14
        self.intermission = 1
        self.start_time   = "09:00"
        # XXX
        self.teams        = [Match.Team("hansi")]
        self.schedule     = []

    def show(self):
        print(self.teams)
        print(self.schedule)

    def add_player(self, team, number, name, surname):
        p = Match.Player(name, surname)
        # XXX not nice
        for t in self.teams:
            if t.name == team:
                t.add_player(number, p)


if __name__ == "__main__":
    t = Tournament_Machine()
    print(t.current_state)
    t.enter_params()
