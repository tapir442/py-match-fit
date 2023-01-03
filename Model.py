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


class Tournament:
    """
    Models a tournament
    """
    def __init__(self):
        self.name         = "No Tournament given"
        self.duration     = 14
        self.intermission = 1
        self.start_time   = "09:00"
        self.teams        = {}
        self.schedule     = []
        self.match_idx    = 0


    def show(self):
        print(self.teams)
        print(self.schedule)

    def add_player(self, team, number, name, surname):
        p = Match.Player(name.title(), surname.title())
        self.teams[team].add_player(number, p)

    def add_team(self, team):
        self.teams[team] = Match.Team(team)

    def store(self):
        import pickle
        with open("hansi.pickle", "wb") as f:
            pickle.dump(self, f)
        return
        d = {}
        print ("........")
        for a in self.__dict__:
            if a not in ["teams", "schedule"]:
                d[a] = getattr(self, a)
            elif a == "teams":
                d["teams"] = {}
                for t in self.teams:
                    d["teams"][t] = self.teams[t].tojson()
            elif a == "schedule":
                pass
        with open("hansi.txt", "w") as f:
            f.write(json.dumps(d, indent=4))

if __name__ == "__main__":
    t = Tournament_Machine()
    t.enter_params()
