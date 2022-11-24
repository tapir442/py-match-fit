import sys
from enum import Enum, auto


class Match_State (Enum):
    """
    """
    waiting  = auto()
    running  = auto()
    finished = auto()


class Bounded_Counter:
    def __init__(self, lower=0, upper=None, step=1):
        self.lower = lower
        self.upper = sys.maxsize
        self.value = lower
        self.step  = step

    def increment(self):
        self.value = min(self.upper, self.value + self.step)

    def decrement(self):
        self.value = max(self.lower, self.value - self.step)

    def __str__(self):
        return str(self.value)

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



class Team:
    """
    Team
    >>> team = Team("FC 1980 Wien")
    >>> from Match import Player
    >>> p = Player("Kurt", "Goalesel")
    >>> team.add_player(1, p)
    >>> print(team.name, [(_[0], _[1].surname) for _ in team.players.items()])
    FC 1980 Wien [('1', 'Goalesel')]
    >>> team.add_player(3, Player("Simon", "Libero"))
    >>> team.add_player(5, Player("Erich", "Ausputzer"))
    >>> print([_.surname for _ in team.players.values()])
    ['Goalesel', 'Libero', 'Ausputzer']
    >>> team.delete_player(3)
    >>> print([_.surname for _ in team.players.values()])
    ['Goalesel', 'Ausputzer']
    """
    pool = {}

    def __init__(self, name: str):
        self.name        = name
        self.players      = {}
        self.pool  [name] = self

    def add_player(self, number:any, player:Player) -> None:
        self.pool[self.name].players[str(number)] = player

    def delete_player(self, number: any) -> None:
        try:
            del self.players[str(number)]
        except KeyError:
            pass

    def scored(self, number: any) -> None:
        self.players[str(number)].scored()


class Match:
    """
    Match
    >>> teamh = Team("FC 1980 Wien")
    >>> from Match import Player
    >>> p = Player("Kurt", "Goalesel")
    >>> teamh.add_player(1, p)
    >>> teamh.add_player(3, Player("Simon", "Libero"))
    >>> teamh.add_player(5, Player("Erich", "Ausputzer"))
    >>> teamg = Team("All Stars")
    >>> teamg.add_player(1, Player("Olli", "Schiff"))
    >>> teamg.add_player("2b", Player("David", "Alaber"))
    >>> teamg.add_player(3, Player("Tschuck", "Norris"))
    >>> teamg.add_player(4, Player("Hansi", "Kranki"))
    >>> match = Match(teamh, teamg)
    >>> match.home_scored(3)
    >>> match.home_wins(), match.draw(), match.guest_wins(), match.running_score
    (True, False, False, (1, 0))
    >>> match.guest_scored(3)
    >>> match.home_wins(), match.draw(), match.guest_wins(), match.running_score
    (False, True, False, (1, 1))
    """
    def __init__(self, home: Team, guest: Team):
        self.home  = home
        self.guest = guest
        self.state = Match_State.waiting
        self.running_score = 0, 0

    def close(self):
        self.state = Match_State.finished

    def start(self):
        self.state = Match_State.running

    def home_scored(self, number: str):
        self.home.scored(number)
        self.running_score = self.score()

    def guest_scored(self, number: str):
        self.guest.scored(number)
        self.running_score = self.score()

    def score(self):
        return self.goals_home(), self.goals_guest()

    def draw(self):
        return self.running_score[0] == self.running_score[1]

    def home_wins(self):
        return self.running_score[0] > self.running_score[1]

    def guest_wins(self):
        return self.running_score[0] < self.running_score[1]

    def goals_home(self):
        s = 0
        for p in self.home.players.values():
            s += int(str(p.goals))
        return s

    def goals_guest(self):
        s = 0
        for p in self.guest.players.values():
            s += int(str(p.goals))
        return s