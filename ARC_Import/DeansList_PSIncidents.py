# -*- coding: utf-8 -*-
"""
Created on Fri Oct 09 14:29:45 2015

@author: Larry.Jerome
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 07 12:37:25 2015

@author: Larry.Jerome
"""
import os
os.chdir('C:\ARC_Integration\DeansList\Scripts')
import DeansList_Master as dl


####Create Incidents file for PS Logs import
incidents = dl.getAllIncidents()
        
psIncidents = dl.mapIncidents(incidents)


try:
    dl.writeCSV(psIncidents['psData'],',','C:\ARC_Integration\DeansList\Data\DLIncidentsForPS')
except IndexError:
    print "No Incidents"
    
try:        
    dl.writeCSV(psIncidents['errors'],',','C:\ARC_Integration\DeansList\Data\DLIncidentsForPS_Errors')
except IndexError:
    print "No Errors"
