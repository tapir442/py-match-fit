import itertools
import datetime

class Scheduler:
    def __init__(self, teams: list, tournament_start: str = "08:00", game_duration: int = 90,
                 break_duration: int = 1
                 ):
        """
        >>> s = Scheduler(["team1", "team2", "team3", "team4"], game_duration=10, break_duration=2)
        >>> print(s.matches[1])
        ['team1', 'team2']
        >>> print(s.matches[2])
        ['team1', 'team3']
        >>> print(s.matches[3])
        ['team1', 'team4']
        >>> print(s.matches[4])
        ['team2', 'team3']
        >>> print(s.matches[5])
        ['team2', 'team4']
        >>> print(s.matches[6])
        ['team3', 'team4']
        >>> print(len(s.matches))
        6
        >>> s = Scheduler(["team8", "team9"])
        >>> print(s.matches[1])
        ['team8', 'team9']
        >>> print(len(s.matches))
        1
        >>> s = Scheduler(["team1", "team2", "team3", "team4"], game_duration=13, break_duration=2)
        >>> print(s.match_starts[0])
        (8, 0)
        >>> print(s.match_starts[1])
        (8, 15)
        >>> print(s.match_starts[2])
        (8, 30)
        >>> print(s.match_starts[3])
        (8, 45)
        >>> print(s.match_starts[4])
        (9, 0)
        >>> print(s.match_starts[5])
        (9, 15)
        """
        tournament_start = datetime.datetime.strptime(tournament_start, "%H:%M")
        game_duration    = datetime.timedelta(minutes = game_duration)
        break_duration   = datetime.timedelta(minutes = break_duration)
        self.matches = {}
        i = 0
        self.match_starts = [(tournament_start.hour, tournament_start.minute)]
        for match in itertools.combinations(teams, 2):
            i += 1
            self.matches[i] = list(match)
            tournament_start += game_duration + break_duration
            self.match_starts.append((tournament_start.hour, tournament_start.minute))
        del self.match_starts[-1]

    def switch_home_guest(self, i):
        """
        >>> s = Scheduler(["team1", "team2", "team3", "team4"])
        >>> s.switch_home_guest(5)
        >>> print(s.matches[1])
        ['team1', 'team2']
        >>> print(s.matches[2])
        ['team1', 'team3']
        >>> print(s.matches[3])
        ['team1', 'team4']
        >>> print(s.matches[4])
        ['team2', 'team3']
        >>> print(s.matches[5])
        ['team4', 'team2']
        >>> print(s.matches[6])
        ['team3', 'team4']
        """
        self.matches[i][0], self.matches[i][1]  = self.matches[i][1], self.matches[i][0]

    def switch_matches(self, i, j):
        """
        >>> s = Scheduler(["team1", "team2", "team3", "team4"])
        >>> s.switch_matches(3, 5)
        >>> print(s.matches[1])
        ['team1', 'team2']
        >>> print(s.matches[2])
        ['team1', 'team3']
        >>> print(s.matches[3])
        ['team2', 'team4']
        >>> print(s.matches[4])
        ['team2', 'team3']
        >>> print(s.matches[5])
        ['team1', 'team4']
        >>> print(s.matches[6])
        ['team3', 'team4']
        >>> #and now a combination
        >>> s = Scheduler(["team1", "team2", "team3", "team4"])
        >>> s.switch_matches(3, 5)
        >>> s.switch_home_guest(3)
        >>> print(s.matches[1])
        ['team1', 'team2']
        >>> print(s.matches[2])
        ['team1', 'team3']
        >>> print(s.matches[3])
        ['team4', 'team2']
        >>> print(s.matches[4])
        ['team2', 'team3']
        >>> print(s.matches[5])
        ['team1', 'team4']
        >>> print(s.matches[6])
        ['team3', 'team4']
        """
        h = self.matches[i]
        self.matches[i] = self.matches[j]
        self.matches[j] = h

    def print_single_match(self, i):
        s = f"Match {i}: {self.match_starts[i-1][0]:d}:" \
            f"{self.match_starts[i-1][1]:02d}, " \
            f"{self.matches[i][0]} : {self.matches[i][1]}"
        return s
