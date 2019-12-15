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
                scorers.append ((_player [2], _player [0], _player [1], team))
        scorers.sort (reverse = True)
        return [x for x in scorers if x [0] > 0]

class GUI(object):
    def __init__(self):
        pass

    def show(self, data):
        from pprint import pprint
        for x in data.table  ():
            pprint (x)
        for x in data.scorer ():
            pprint (x)

class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view  = view
        self.model.register_observer(self)

    def update(self):
        self.view.show(self.model)



model = Model()
gui = GUI()
ctrl = Controller(model, gui)

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

