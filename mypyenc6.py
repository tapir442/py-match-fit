#/bin/bash

import os
from pathlib import Path

uis = Path("ui")
for ui in uis.iterdir():
    os.system(f"pyuic6 -o {ui.stem}UI.py ui/{ui.name}")
