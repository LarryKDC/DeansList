# -*- coding: utf-8 -*-
"""
Created on Fri Oct 09 15:10:41 2015

@author: Larry.Jerome
"""

import os
os.chdir('C:\Users\larry.jerome\Box Sync\Larry\Deanslist\Scripts\Python')
import DeansListMaster as dl

users = dl.getAllUsers()

errorFields = ['DLUserID','SchoolName']

dl.writeCSV(users,',','C:\Users\larry.jerome\Box Sync\Larry\Deanslist\Data\DLUsersForARC',errorFields)