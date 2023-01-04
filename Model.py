#from enum import Enum, auto

#from statemachine import StateMachine, State

#class Tournament_Machine(StateMachine):
#    tabula_rasa    = State("tabula_rasa", initial=True)
#    params         = State("params")
#    parameters_set = State("parameters_set")
#    teams_set      = State("teams_set")
#    scheduled      = State("scheduled")
#    match_ready    = State("match_ready")
#    match_running  = State("match_running")
#    match_finished = State("match_finished")
#    finished       = State("finished")

#    enter_params   = tabula_rasa.to(params)

#    def on_enter_params(self, disable=None, enable=None, *args, **kw):
#        print(locals())
#        print("on_enter_params")


import json
import Match
import pickle
import datetime

class Tournament:
    """
    Models a tournament
    """
    def __init__(self):
        self.name         = "No Tournament given"
        self.duration     = 14
        self.intermission = 1
        self.start_time   = datetime.time(hour=9, minute=0)
        self.teams        = {}
        self.schedule     = []
        self.match_idx    = None

    def show(self):
        print(self.teams)
        print(self.schedule)

    def add_player(self, team, number, name, surname):
        p = Match.Player(name.title(), surname.title())
        self.teams[team].add_player(number, p)

    def add_team(self, team):
        self.teams[team] = Match.Team(team)

    def store(self):
        with open("hansi.pickle", "wb") as f:
            pickle.dump(self, f)

    def standings(self):
        eligible_matches = [_ for _ in self.schedule]




if __name__ == "__main__":
    t = Tournament_Machine()
    t.enter_params()
