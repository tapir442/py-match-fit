""" Model.py """
import datetime
import functools
import pickle
from collections import namedtuple

import Match
from Scheduler_Model import Scheduler

team_result = namedtuple("team_result", ["team", "goals", "got", "points"])
scorer      = namedtuple("scorer", ["number", "name", "team", "goals"])

class Tournament:
    """
    Models a tournament
    """
    def __init__(self):
        self.name = ""
        self.duration = 10
        self.intermission = 2
        self.start_time = datetime.time(hour=9, minute=0)
        self.teams = {}
        self.match_idx = None
        self.clear_schedule()

    def show(self):
        print(self.teams)
        print(self.schedule)

    def add_player(self, team:str, number:str, name:str, surname:str) -> None:
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
            _.goals  = 0
            _.got    = 0
            _.diff   = 0

        for s in self.schedule.matches.values():
            winner = s.winner()
            if not winner:
                if s.draw():
                    s.home.points += 1
                    s.guest.points += 1
            else:
                winner.points += 3
            s.home.goals  += s.running_score[0].value
            s.home.got    += s.running_score[1].value
            s.home.diff   = s.home.goals - s.home.got
            s.guest.got   += s.running_score[0].value
            s.guest.goals += s.running_score[1].value
            s.guest.diff   = s.guest.goals - s.guest.got
        result = []
        for _ in self.teams.values():
            result.append(_)
        u = []

        def _cmp(s, o):
            if s.points < o.points:
                return -1
            if s.points > o.points:
                return 1
            w = None
            for match in self.schedule.matches.values():
                if match.home.name == s.name and match.guest.name == o.name:
                    w = match.winner()
                elif match.guest.name == s.name and match.home.name == o.name:
                    w = match.winner()
                else:
                    continue
            if w is not None:
                if w == o.name:
                    return -1
                if w == s.name:
                    return 1

            if s.diff < o.diff:
                return -1
            if s.diff > o.diff:
                return 1
            return 0
        for _ in sorted(result, key=functools.cmp_to_key(_cmp), reverse=True):
            u.append(team_result(team=_.name, goals = _.goals, got = _.got, points = _.points))
        return u

    def scorers(self):
        players = []
        for t in self.teams:
            for p in self.teams[t].players:
                _ = self.teams[t].players[p]
                _.number = p
                _.team   = t
                if _.goals.value:
                    players.append((_, t))
        p = sorted(players, key = lambda x: x[0].goals.value, reverse = True)
        players = []
        for _ in p:
            players.append(scorer(_[0].number,
                                  " ".join((_[0].name, _[0].surname)),
                                  _[0].team,
                                  _[0].goals.value))
        return players

    def create_schedule(self, *args, **kw):
        teams = self.teams.keys()
        start = self.start_time
        self.schedule = Scheduler(teams,
                                  f"{start.hour()}:{start.minute()}",
                                  int(self.duration),
                                  int(self.intermission))

    def store(self):
        with open("%s.pickle" % self.name, "wb") as f:
            pickle.dump(self, f)

if __name__ == "__main__":
    t = Tournament_Machine()
    t.enter_params()
