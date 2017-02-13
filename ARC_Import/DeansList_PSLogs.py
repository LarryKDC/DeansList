# -*- coding: utf-8 -*-
"""
Created on Tue Oct 06 14:48:19 2015

@author: Larry.Jerome
"""

import os

os.chdir('C:\ARC_Integration\DeansList\Scripts')

import DeansList_Master as dl

####Create Comms file for PS logs import
comms = dl.getAllComms()
        
psComms = dl.mapComms(comms)

#errorFields = ['DLCallLogID','SchoolName']
try:
    dl.writeCSV(psComms['psData'],',','C:\ARC_Integration\DeansList\Data\DLCommsForPS')
except IndexError:
    print "No Comms"
    
try:
    dl.writeCSV(psComms['errors'],',','C:\ARC_Integration\DeansList\Data\DLCommsForPSErrors')
except IndexError:
    print "No Comms Errors"
