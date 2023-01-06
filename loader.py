import pickle, sys

with open(sys.argv[1], "rb") as f:
    tournament = pickle.load(f)

import Match, Model
from pprint import pprint
pprint(tournament.__dict__)
breakpoint()

with open(sys.argv[1], "wb") as f:
    pickle.dump(tournament, f)
