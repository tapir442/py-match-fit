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

    def home (self) :
        return self._teams [0]

    def guest (self) :
        return self._teams [1]

    def goal (self, team, number) :
        if self._teams [0]._name == team :
            self._teams [2] += 1
        else :
            self._teams [3] += 1
        Team.pool [team].goal (number)

    def cancel_goal (self, team, number) :
        if self._teams [0]._name == team :
            if self._teams [2] > 0 :
                self._teams [2] -= 1
        else :
            if self._teams [3] > 0 :
                self._teams [3] -= 1
        Team.pool [team].cancel_goal (number)
        
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

    def __str__ (self) :
        return self._teams [0]._name +" "+ self._teams [1]._name

    def goals_home (self) :
        return self._teams [2]

    def goals_guest (self) :
        return self._teams [3]

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
        self.pool [self._name]._players [number] = [name, surname, 0]

    def delete_player (self, number) :
        try :
            del self._players [number]
        except KeyError :
            pass

    def goal (self, number) :
        try :
            self.pool [self._name]._players [number][2] += 1
        except KeyError :
            print ("Scheisse", self._name, number)

    def cancel_goal (self, number) :
        try :
            if self.pool [self._name]._players [number][2] > 0 :
                self.pool [self._name]._players [number][2] -= 1
        except KeyError:
            print ("Scheisse", self._name, number)
        
    def goals (self) :
        return sum ([self._players[p][2] for p in self._players])

    def __str__ (self) :
        return self._name

# end class Team


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

    def create_schedule (self, matches) :
        self.schedule_table = []
        for match in matches :
            self.schedule_table.append (Match (self.teams [match[0]], self.teams [match[1]]))

    def start_match (self, idx) :
        self._running = idx
        self.schedule_table [self._running].start ()

    def close_match (self) :
        self.schedule_table [self._running].close ()

    def register_observer(self, observer):
        self.observers.append(observer)

    def goal (self, team, number) :
        match = self.schedule_table [self._running]
        print ("Match for goal: ", self._running, match)
        print ("Team for goal:", team, "number:", number)
        match.goal (team, number)

    def cancel_goal (self, team, number) :
        match = self.schedule_table [self._running]        
        match.cancel_goal (team, number)
#       self.teams [team].cancel_goal (number)

    def running (self) :
        return self._running

    def table (self) :
        result     = []
        no_games_idx  = 0
        victories_idx = 1
        draw_idx      = 2
        lost_idx      = 3
        shot_idx      = 4
        got_idx       = 5
        diff_idx      = 6
        points_idx    = 7
        teams         = {}
        for match in self.schedule_table :
            if match._teams [0]._name not in teams :
                teams[match._teams [0]._name] = [0] * 8
            if match._teams [1]._name not in teams :
                teams[match._teams [1]._name] = [0] * 8
            if match._state == Match_State.waiting :
                # XXX
                continue
            
            teams[match._teams [0]._name][no_games_idx] += 1
            teams[match._teams [1]._name][no_games_idx] += 1

            teams[match._teams [0]._name][shot_idx] += match.goals_home  ()
            teams[match._teams [1]._name][shot_idx] += match.goals_guest ()

            teams[match._teams [1]._name][got_idx] += match.goals_home  ()
            teams[match._teams [0]._name][got_idx] += match.goals_guest ()

            teams[match._teams [0]._name][diff_idx] += match.goals_home  () -  match.goals_guest ()
            teams[match._teams [1]._name][diff_idx] += match.goals_guest () -  match.goals_home  ()

            if match.draw ():
                for i in range (2) :
                    teams[match._teams [i]._name][points_idx] += 1
                    teams[match._teams [i]._name][draw_idx]   += 1
            else :
                winner = match.winner ()
                loser  = match.loser ()
                teams[winner[0]._name][points_idx]    += 3
                teams[winner[0]._name][victories_idx] += 1
                teams[loser[0]._name][lost_idx]       += 1

        result = [ (x, *teams [x]) for x in teams ]
        result.sort (key = lambda x: (x [points_idx+1], x[diff_idx+1] ), reverse = True)
        return (x for x in result)

    def scorer (self) :
        scorers = []
        for team in self.teams :
            for player in self.teams[team]._players :
                _player = self.teams[team]._players [player]
                scorers.append ((_player [2], _player [0], _player [1], team))
        scorers.sort (reverse = True)
        return [x for x in scorers if x [0] > 0]
