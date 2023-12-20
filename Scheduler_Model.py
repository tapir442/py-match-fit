""" Scheduler """

import itertools
import datetime

from Match import Match, Team

class Scheduler:
    """
    Scheduler implementation
    """
    def __init__(self, teams: list,
                 tournament_start: str = "08:00",
                 game_duration: int = 90,
                 break_duration: int = 1
                 ):
        """
        >>> s = Scheduler(["team1", "team2", "team3", "team4"], game_duration=10, break_duration=2)
        >>> print(s.matches[1])
        08:00, (team1, team2)
        >>> print(s.matches[2])
        08:12, (team1, team3)
        >>> print(s.matches[3])
        08:24, (team1, team4)
        >>> print(s.matches[4])
        08:36, (team2, team3)
        >>> print(s.matches[5])
        08:48, (team2, team4)
        >>> print(s.matches[6])
        09:00, (team3, team4)
        >>> print(len(s.matches))
        6
        >>> s = Scheduler(["team8", "team9"])
        >>> print(s.matches[1])
        08:00, (team8, team9)
        >>> print(len(s.matches))
        1
        >>> s = Scheduler(["team1", "team2", "team3", "team4"], game_duration=13
        ... , break_duration=2)
        >>> print(s.matches[1].starts)
        (8, 0)
        >>> print(s.matches[2].starts)
        (8, 15)
        >>> print(s.matches[3].starts)
        (8, 30)
        >>> print(s.matches[4].starts)
        (8, 45)
        >>> print(s.matches[5].starts)
        (9, 0)
        >>> print(s.matches[6].starts)
        (9, 15)
        """
        tournament_start = datetime.datetime.strptime(tournament_start, "%H:%M")
        game_duration    = datetime.timedelta(minutes=game_duration)
        break_duration   = datetime.timedelta(minutes=break_duration)
        self.matches = {}
        i = 0
#        i = 0
#        n = len(teams)
#        while i < n-1:
#            print('Runde ' + str(i+1) + ':')
#            print(teams[n-1], ':', teams[i])
#            j = 1
#            while j < n/2:
#                a = i-j
#                b = i+j
#                if a < 0:
#                    a = a + (n-1)
#                if b > n-2:
#                    b = b - (n-1)
#                print(teams[a], ':', teams[b])
#                j = j+1
#            i = i+1
        i = 0
        for match in itertools.combinations(teams, 2):
            i += 1
            # Fixme! no access to team should be used
            self.matches[i] = Match(Team.pool[match[0]],
                                    Team.pool[match[1]],
                                    (tournament_start.hour,
                                     tournament_start.minute))
            tournament_start += game_duration + break_duration

    def switch_home_guest(self, i:int) -> None:
        """
        >>> s = Scheduler(["team1", "team2", "team3", "team4"])
        >>> s.switch_home_guest(5)
        >>> print(s.matches[1])
        08:00, (team1, team2)
        >>> print(s.matches[2])
        09:31, (team1, team3)
        >>> print(s.matches[3])
        11:02, (team1, team4)
        >>> print(s.matches[4])
        12:33, (team2, team3)
        >>> print(s.matches[5])
        14:04, (team4, team2)
        >>> print(s.matches[6])
        15:35, (team3, team4)
        """
        self.matches[i].home, self.matches[i].guest = \
            self.matches[i].guest, self.matches[i].home

    def switch_matches(self, i:int, j:int) -> None:
        """
        >>> s = Scheduler(["team1", "team2", "team3", "team4"])
        >>> s.switch_matches(3, 5)
        >>> print(s.matches[1])
        08:00, (team1, team2)
        >>> print(s.matches[2])
        09:31, (team1, team3)
        >>> print(s.matches[3])
        11:02, (team2, team4)
        >>> print(s.matches[4])
        12:33, (team2, team3)
        >>> print(s.matches[5])
        14:04, (team1, team4)
        >>> print(s.matches[6])
        15:35, (team3, team4)
        >>> #and now a combination
        >>> s = Scheduler(["team1", "team2", "team3", "team4"])
        >>> s.switch_matches(3, 5)
        >>> s.switch_home_guest(3)
        >>> print(s.matches[1])
        08:00, (team1, team2)
        >>> print(s.matches[2])
        09:31, (team1, team3)
        >>> print(s.matches[3])
        11:02, (team4, team2)
        >>> print(s.matches[4])
        12:33, (team2, team3)
        >>> print(s.matches[5])
        14:04, (team1, team4)
        >>> print(s.matches[6])
        15:35, (team3, team4)
        """
        # XXX: assure that both matches are in the future
        self.matches[i].home, self.matches[i].guest, self.matches[j].home, self.matches[j].guest =\
            self.matches[j].home, self.matches[j].guest, self.matches[i].home, self.matches[i].guest
