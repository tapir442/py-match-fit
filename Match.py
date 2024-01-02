"""
Match data containers
"""
import sys
from enum import Enum, auto
import json
import datetime
import functools

class Match_State (Enum):
    """
    """
    waiting  = auto()
    running  = auto()
    finished = auto()

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if "tojson" in dir(o):
            return o.tojson()
        return json.JSONEncoder.default(self, o)

@functools.total_ordering
class Bounded_Counter:
    def __init__(self, lower:int=0, upper:int=sys.maxsize, step:int=1):
        self.lower = lower
        self.upper = upper
        self.value = lower
        self.step  = step

    def increment(self, step:int=0):
        self.value = min(self.upper, self.value + (self.step if not step else step))

    def decrement(self, step:int=0):
        self.value = max(self.lower, self.value - (self.step if not step else step))

    def __str__(self):
        return str(self.value)

    def tojson(self):
        return json.dumps(self.__dict__, indent=4, cls=CustomEncoder)

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value


class Player:
    """
    >>> p = Player("Kurt", "Goalkeeper")
    >>> print(p.name, p.surname, p.suspended, p.goals, p.assists, p.yellow_cards, p.red_cards)
    Kurt Goalkeeper False 0 0 0 0
    >>> p.scored()
    >>> print(p.name, p.surname, p.suspended, p.goals, p.assists, p.yellow_cards, p.red_cards)
    Kurt Goalkeeper False 1 0 0 0
    >>> p.scored()
    >>> print(p.name, p.surname, p.suspended, p.goals, p.assists, p.yellow_cards, p.red_cards)
    Kurt Goalkeeper False 2 0 0 0
    >>> p.goal_was_cancelled()
    >>> print(p.name, p.surname, p.suspended, p.goals, p.assists, p.yellow_cards, p.red_cards)
    Kurt Goalkeeper False 1 0 0 0
    >>> p.had_assist()
    >>> print(p.name, p.surname, p.suspended, p.goals, p.assists, p.yellow_cards, p.red_cards)
    Kurt Goalkeeper False 1 1 0 0
    >>> p.goal_was_cancelled()
    >>> print(p.name, p.surname, p.suspended, p.goals, p.assists, p.yellow_cards, p.red_cards)
    Kurt Goalkeeper False 0 1 0 0
    >>> p.goal_was_cancelled()
    >>> print(p.name, p.surname, p.suspended, p.goals, p.assists, p.yellow_cards, p.red_cards)
    Kurt Goalkeeper False 0 1 0 0
    >>> from pprint import pprint
    >>> pprint(p.tojson())
    {'assists': '1',
     'goals': '0',
     'name': 'Kurt',
     'red_cards': '0',
     'surname': 'Goalkeeper',
     'suspended': 'False',
     'yellow_cards': '0'}
    """
    def __init__(self, name: str, surname: str):
        self.name         = name
        self.surname      = surname
        self.suspended    = False
        # football specific, should not be there in generic version
        self.goals        = Bounded_Counter()
        self.assists      = Bounded_Counter()
        self.yellow_cards = Bounded_Counter()
        self.red_cards    = Bounded_Counter()

    def scored(self):
        self.goals.increment()

    def cancelled(self):
        self.goals.decrement()

    def goal_was_cancelled(self):
        self.goals.decrement()

    def got_yellow_card(self):
        self.yellow_cards.increment()

    def yellow_card_was_cancelled(self):
        self.yellow_cards.decrement()

    def got_red_card(self):
        self.red_cards.increment()

    def red_card_was_cancelled(self):
        self.red_cards.decrement()

    def will_be_suspendded(self):
        self.suspended = True

    def suspension_over(self):
        self.suspended = False

    def had_assist(self):
        self.assists.increment()

    def no_assist(self):
        self.assists.decrement()

    def tojson(self):
        d = {}
        for k, v in self.__dict__.items():
            d [k] = str(v)
        return d

class Team:
    """
    Team
    >>> team = Team("FC 1980 Wien")
    >>> from Match import Player
    >>> p = Player("Kurt", "Goalesel")
    >>> team.add_player("1", p)
    >>> print(team.name, [(_[0], _[1].surname) for _ in team.players.items()])
    FC 1980 Wien [('1', 'Goalesel')]
    >>> team.add_player("3", Player("Simon", "Libero"))
    >>> team.add_player("5", Player("Erich", "Ausputzer"))
    >>> print([_.surname for _ in team.players.values()])
    ['Goalesel', 'Libero', 'Ausputzer']
    >>> team.delete_player("3")
    >>> print([_.surname for _ in team.players.values()])
    ['Goalesel', 'Ausputzer']
    >>> from pprint import pprint
    >>> pprint(team.tojson())
    ('{"name": "FC 1980 Wien", "players": {"1": {"name": "Kurt", "surname": '
     '"Goalesel", "suspended": "False", "goals": "0", "assists": "0", '
     '"yellow_cards": "0", "red_cards": "0"}, "5": {"name": "Erich", "surname": '
     '"Ausputzer", "suspended": "False", "goals": "0", "assists": "0", '
     '"yellow_cards": "0", "red_cards": "0"}}}')
    """
    pool = {}

    def __init__(self, name: str):
        self.name = name
        self.players = {}
        self.pool  [name] = self
        self.points = 0
        self.og = 0

    def add_player(self, number:str, player:Player) -> None:
        self.players[number] = player

    def delete_player(self, number: str) -> None:
        try:
            del self.players[number]
        except KeyError:
            pass

    def scored(self, number: str) -> None:
        self.players[number].scored()

    def scored_og(self) -> None:
        self.og += 1

    def cancelled_og(self, running_score):
        if self.og > 0:
            self.og -= 1
            running_score.decrement()

    def cancelled(self, number: str) -> None:
        self.players[number].cancelled()

    def __hash__(self):
        return hash(self.name)

    def tojson(self):
        """
        Serialize
        """
        d = {}
        for k in self.__dict__:
            if k == "name":
                d[k] = self.__dict__[k]
            if k == "pool":
                continue
            if k == "players":
                d["players"] = {}
                for playerid in self.players:
                    d["players"][playerid] = self.players[playerid].tojson()
            if k == "og":
                d["og"] = self.og.tojson()
        return json.dumps(d)

class Match:
    """
    Match
    >>> teamh = Team("FC 1980 Wien")
    >>> from Match import Player
    >>> p = Player("Kurt", "Goalesel")
    >>> teamh.add_player("1", p)
    >>> teamh.add_player("3", Player("Simon", "Libero"))
    >>> teamh.add_player("5", Player("Erich", "Ausputzer"))
    >>> teamg = Team("All Stars")
    >>> teamg.add_player("1", Player("Olli", "Schiff"))
    >>> teamg.add_player("2b", Player("David", "Alaber"))
    >>> teamg.add_player("3", Player("Tschuck", "Norris"))
    >>> teamg.add_player("4", Player("Hansi", "Kranki"))
    >>> from datetime import time
    >>> match = Match(teamh, teamg, starts=time(9, 0))
    >>> match.home_scored("3")
    >>> match.home_wins(), match.draw(), match.guest_wins(), match.running_score
    (True, False, False, (1, 0))
    >>> match.guest_scored("3")
    >>> match.home_wins(), match.draw(), match.guest_wins(), match.running_score
    (False, True, False, (1, 1))
    """
    HOME=0
    GUEST=1
    def __init__(self, home: Team, guest: Team, starts: datetime.date):
        self.home  = home
        self.guest = guest
        self.state = Match_State.waiting
        self.starts = starts
        self.running_score = [Bounded_Counter(), Bounded_Counter()]

    def close(self):
        self.state = Match_State.finished

    def start(self):
        self.state = Match_State.running
        self.running_score = [Bounded_Counter(), Bounded_Counter()]

    def home_scored(self, number: str):
        self.home.scored(number)
        self.running_score[self.HOME].increment()

    def guest_scored(self, number: str):
        self.guest.scored(number)
        self.running_score[self.GUEST].increment()

    def home_cancelled(self, number: str):
        v = self.home.players[number].goals.value
        self.home.cancelled(number)
        if v != self.home.players[number].goals.value:
            self.running_score[self.HOME].decrement()

    def guest_cancelled(self, number: str):
        v = self.guest.players[number].goals.value
        self.guest.cancelled(number)
        if v != self.guest.players[number].goals.value:
            self.running_score[self.GUEST].decrement()

    def og_home(self):
        self.home.scored_og()
        self.running_score[self.HOME].increment()

    def og_guest(self):
        self.guest.scored_og()
        self.running_score[self.GUEST].increment()

    def og_cancel_home(self):
        self.home.cancelled_og(self.running_score[self.HOME])

    def og_cancel_guest(self):
        self.guest.cancelled_og(self.running_score[self.GUEST])

    def score(self):
        return self.goals_home(), self.goals_guest()

    def draw(self):
        if self.state == Match_State.waiting:
            return None
        return self.running_score[self.HOME] == self.running_score[self.GUEST]

    def home_wins(self):
        return self.running_score[self.HOME] > self.running_score[self.GUEST]

    def guest_wins(self):
        return self.running_score[self.HOME] < self.running_score[self.GUEST]

    @staticmethod
    def _goals(o):
        return o.og + [int(str(p.goals)) for p in o.players.values()]

    def goals_home(self):
        return self._goals(self.home)

    def goals_guest(self):
        return self._goals(self.guest)

    def winner(self):
        """
        returns winner of a match
        """
        if self.state == Match_State.waiting:
            return None
        if self.home_wins():
            return self.home
        if self.guest_wins():
            return self.guest
        return ""

    def __str__(self):
        return f"{self.starts[self.HOME]:02d}:{self.starts[self.GUEST]:02d}, ({self.home}, {self.guest})"
