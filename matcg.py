class Match :
    def __init__ (self, team1, team2) :
        self._team1 = team1
        self._team2 = team2
    # end def __init__

    def goal_team1 (self, number) :
        self._team1.goal (number)

    def goal_team2 (self, number) :
        self._team2.goal (number)



    
