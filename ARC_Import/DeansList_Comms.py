# -*- coding: utf-8 -*-
"""
Created on Wed Oct 07 12:29:24 2015

@author: Larry.Jerome
"""

import os
os.chdir('C:\ARC_Integration\DeansList\Scripts')

import DeansList_Master as dl  #DeansList_Master is the master module that contains all the function for access the DL API

####Create Comms file for PS logs import
comms = dl.getAllComms() #this function gets all the communication records as dictionaries from all schools in DL and puts them into a single list

commsForARC = dl.mapCommsARC(comms) #this function transkforms them into a list of lists and selects fields to be loaded into ARC

try: #store the list of records as a CSV so they can be loaded into the database
    dl.writeCSV(commsForARC['comms'],',','C:\ARC_Integration\DeansList\Data\DLCommsForARC')
except IndexError: #if an indexError occurs it means no records came through the API
    print 'No Communications - Uh Oh!'

try: #create a CSV that logs errors in the transformation of the list of commumications into the CSV in the previous step
    dl.writeCSV(commsForARC['errors'],',','C:\ARC_Integration\DeansList\Data\DLCommsErrors')
except IndexError: #an IndexError indicates that there were no errors in the transformation
    print 'No Errors'
