# -*- coding: utf-8 -*-
"""
Created on Fri Oct 09 15:52:01 2015

@author: Larry.Jerome
"""

import os
os.chdir('C:\ARC_Integration\DeansList\Scripts')
import DeansList_Master as dl

rosters = dl.getAllRosters()

dl.writeCSV(rosters,',','C:\ARC_Integration\DeansList\Data\DLRostersForARC')
