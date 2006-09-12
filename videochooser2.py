#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, math, random
import avg
import anim

Player = avg.Player()
Log = avg.Logger.get()
bDebug = not(os.getenv('AVG_DEPLOY'))
if (bDebug):
    Player.setResolution(0, 0, 900, 0) 
else:
    Player.setResolution(1, 0, 0, 0)
    Player.showCursor(0)
    Log.setFileDest("/var/log/cleuse.log")
Log.setCategories(Log.APP |
                  Log.WARNING | 
                  Log.PROFILE |
#                 Log.PROFILE_LATEFRAMES |
                  Log.CONFIG
#                 Log.MEMORY  |
#                 Log.BLTS    
#                  Log.EVENTS
                  )
Player.loadFile("videochooser2.avg")
anim.init(Player)
Player.setVBlankFramerate(1)
Player.play()
