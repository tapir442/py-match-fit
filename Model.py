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

import datetime
import pickle
import Match
from Scheduler_Model import Scheduler

class Tournament:
    """
    Models a tournament
    """
    def __init__(self):
        self.name = ""
        self.duration = 14
        self.intermission = 1
        self.start_time = datetime.time(hour=9, minute=0)
        self.teams = {}
        self.schedule = Scheduler([])
        self.match_idx = None

    def show(self):
        print(self.teams)
        print(self.schedule)

    def add_player(self, team, number, name, surname) -> None:
        """
        Adds a player to the tournament
        """
        self.teams[team].add_player(number,
                                    Match.Player(name.title(), surname.title())
                                    )
    def clear_teams(self):
        self.teams = {}

    def clear_players(self, team):
        self.teams[team].players = {}

    def add_team(self, team):
        self.teams[team] = Match.Team(team)

    def clear_schedule(self) -> None:
        self.schedule = Scheduler([])

    def standings(self):
        """
        compute the live table
        """
        for _ in self.teams.values():
            _.points = 0
        for s in self.schedule.matches.values():
            winner = s.winner()
            if not winner:
                if s.draw():
                    s.home.points += 1
                    s.guest.points += 1
            else:
                winner.points += 3
        result = []
        for _ in self.teams.values():
            result.append(_)
        u = []
        for _ in sorted(result, key=lambda x: x.points, reverse=True):
            u.append(f"{_.name}: {_.points}")
        return u

    def scorers(self):
        players = []
        for t in self.teams:
            for p in self.teams[t].players:
                _ = self.teams[t].players[p]
                if _.goals.value:
                    players.append((_, t))
        p = sorted(players, key = lambda x: x[0].goals.value, reverse = True)
        players = []
        for _ in p:
            players.append(f"{_[0].name} {_[0].surname}, ({_[1]}), {_[0].goals.value}")
        return players

    def create_schedule(self, *args, **kw):
        teams = self.teams.keys()
        start = self.start_time
        self.schedule = Scheduler(teams,
                                  f"{start.hour()}:{start.minute()}",
                                  int(self.duration),
                                  int(self.intermission))


if __name__ == "__main__":
    t = Tournament_Machine()
    t.enter_params()
