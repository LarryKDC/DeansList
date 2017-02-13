# -*- coding: utf-8 -*-
"""
Created on Fri Oct 09 13:58:33 2015

@author: Larry.Jerome
"""

import os
os.chdir('C:\ARC_Integration\DeansList\Scripts')
import DeansList_Master as dl
import datetime

#default date range is previous 14 days
attDaily = dl.getAllAttendance(sdt='2016-08-08')
attClass = dl.getClassAttendance('kcp',sdt='2016-08-08')

att = []
att.extend(attDaily)
att.extend(attClass)

dl.writeCSV(att,',','C:\ARC_Integration\DeansList\Data\DLAttendanceForARC')

