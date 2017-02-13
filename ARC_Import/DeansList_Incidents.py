# -*- coding: utf-8 -*-
"""
Created on Wed Oct 07 12:37:25 2015

@author: Larry.Jerome
"""
import os
os.chdir('C:\ARC_Integration\DeansList\Scripts')
import DeansList_Master as dl
from datetime import datetime


####Create Incidents file for PS Logs import5
incidents = dl.getAllIncidents() #default date is current date - 14 days


#capture records
new_incidents = []

for incident in incidents:
    #if datetime.strptime(incident['CreateTS']['date'].split(' ')[0],'%Y-%m-%d') < datetime(2016,8,8):
    new_incidents.append(incident)
        
ARCIncidents = dl.mapIncidentsARC(new_incidents)

#errorFields = ['IncidentID','SchoolID']

try:
    dl.writeCSV(ARCIncidents['incidents'],',','C:\ARC_Integration\DeansList\Data\DLIncidentsForARC')
except IndexError:
    print 'No Incidents'

try:
    dl.writeCSV(ARCIncidents['penalties'],',','C:\ARC_Integration\DeansList\Data\DLPenaltiesForARC')
except IndexError:
    print 'No Penalties'

try:
    dl.writeCSV(ARCIncidents['errors'],',','C:\ARC_Integration\DeansList\Data\DLIncidentsErrors')
except IndexError:
    print 'No Errors'
