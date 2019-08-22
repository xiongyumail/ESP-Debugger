#!/usr/bin/env python3
import sys
from pcbnew import *

filename=sys.argv[1]

pcb = LoadBoard(filename)
for module in pcb.GetModules():
    print("* Module: %s"%module.GetReference())
    module.Value().SetVisible(False)      # set Value as Hidden
    module.Reference().SetVisible(False)   # set Reference as Hidden

pcb.Save("mod_"+filename)
