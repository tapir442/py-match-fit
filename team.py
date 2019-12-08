class Team:
    def __init__ (self, name) :
        self._name    = name
        self._members = {}
    # end def __init__

    def add_member (self, number, name, surname) :
        assert 1 <= number <= 25
        self._members [number] = [name, surname, 0]
    # end def add_member

    def del_member (self, number) :
        try :
            del self._members [number]
        except KeyError :
            pass
    # end def del_member

    def goal (self, number) :
        assert number in self._members
        self._members [number][2] += 1
    # end def shot

    def cancel_goal (self, number) :
        assert number in self._members
        if self._members [number][2] > 0 :
            self._members [number][2] -= 1
    # end def cancel_goal

    def goalgetters (self) :
        def getKey (x) :
            return x[2]
        _goalgetters = [x for x in self._members.values ()]
        _goalgetters.sort (key = getKey, reverse=True)
        return _goalgetters
    # end def goalgetters

    def team (self) :
        for k in sorted (self._members) :
            print (self._members [k])
# end class Team

if __name__ == "__main__" :
    team = Team ("1980")
    team.add_member (1, "Hansi", "Goalesel")
    team.add_member (2, "2", "2N")
    team.add_member (3, "3", "3N")
    team.goal (2)
    team.goal (2)
    team.goal (3)
    team.team ()
    print (team.goalgetters())
    
