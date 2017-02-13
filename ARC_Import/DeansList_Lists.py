# -*- coding: utf-8 -*-
"""
Created on Fri Oct 09 14:50:12 2015

@author: Larry.Jerome
"""

import os
os.chdir('"C:\ARC_Integration\DeansList\Scripts')
import DeansList_Master as dl


lists = dl.getAllSessionListsStudents()#sdt='2016-08-08')  # defaults to previous two week, reset sdt and edt to 'YYYY-MM-DD' if necessary to reset records
#deDupLists = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in lists)] #remove duplicates from lists records

dl.writeCSV(lists,',','C:\ARC_Integration\Deanslist\Data\DLListsForARC')
