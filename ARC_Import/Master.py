# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 15:00:45 2016

@author: larry.jerome
"""

import requests
import pprint
import csv
import os
import datetime
import time
import copy



#os.chdir('C:\ARC_Integration\DeansList\Scripts')



schoolid={
            '82':'1000',
            '81':'1002',
            '85':'1001',
            '73':'1003',
            '77':'1004',
            '71':'1005',
            '72':'1006',
            '75':'1007',
            '76':'1008',
            '79':'1010',
            '70':'1009',
            '83':'1011',
            '74':'1012',
            '84':'1014',
            '78':'1013',
            '86':'2000',
            '80':'1100'
        }
        
schoolName={
            '82':'KEY',
            '81':'AIM',
            '85':'WILL',
            '73':'LEAP',
            '77':'Promise',
            '71':'Discover',
            '72':'Grow',
            '75':'Heights',
            '76':'Lead',
            '79':'Spring',
            '70':'Connect',
            '83':'NE',
            '74':'ATA',
            '84':'Valor',
            '78':'Quest',
            '86':'LC',
            '80':'KCP'
           }

schoolNameToID={
            'key':'82',
            'aim':'81',
            'will':'85',
            'leap':'73',
            'promise':'77',
            'discover':'71',
            'grow':'72',
            'heights':'75',
            'lead':'76',
            'spring':'79',
            'connect':'70',
            'ne':'83',
            'ata':'74',
            'valor':'84',
            'quest':'78',
            'lc':'86',
            'kcp':'80'
           }

unicodeErrors={ u'\u201c':'"',
                u'\u201d':'"',
                u'\u2019':"'",
                u'\uf0f0':' ',
                u'\u2013':'-',
                u'\u2026':"...",
                '\n':" ",
                '\n\n':" ",
                u'\xe1':"a",
                u'\xf3':'o',
                '\r':' ',
                '\t':' ',
                u'\u2022':'',
                u'\u2014':'--',
                u'\uf0a7':'',
                u'\uf04c':'',
                '\xa0':' ',
                '0xa0':' '
              }


incidentSubtypes={  'Academic Dishonesty':'ACADEMIC', #added to PS
                    'Alcohol Related (A)':'ALCOHOL',        #added to PS  
                    'Arson':'ARSON',                  #added to PS  
                    'Attendance Intervention':'ATT INTERVENTION', #added to PS
                    'Attendance/Skipping/Tardy':'SKIPPING', #added to PS
                    'Bullying':'BULLY',                 #added to PS
                    'Disruptive Behavior':'DB',         #added to PS
                    'Fighting':'FIGHT',                 #added to PS
                    'Flammables':'FLAMMABLES',          #added to PS
                    'Gambling':'GAMBLING',              #added to PS
                    'Illicit Drug Related (D)':'IDR',   #added to PS
                    'Improper Use of Technology':'TECHNOLOGY', #added to PS
                    'Insubordination':'INSUBORDINATION', #added to PS
                    'Sexual Misconduct or Harassment':'SEXUAL', #added to PS
                    'Theft':'THEFT',                        #added to PS
                    'Threatening Physical Harm':'THREAT', #added to PS
                    'Vandalism':'VANDALISM',        #added to PS
                    'Violent Incident (WITH physical injury) (VIOWINJ)':'VIOWINJ',   #added to PS
                    'Violent Incident (WITHOUT physical injury) (VIOWOINJ)':'VIOWOINJ', #added to PS
                    'Weapons Possession - Handguns (W-HANDGUNS)':'W-HANDGUNS',      #added to PS
                    'Weapons Possession - Non-firearm (W)':'W-NONGUN',       #added to PS
                    'Weapons Possession - Rifles / Shotgun (W-RIFLESHOTGUN)':'W-RIFLESHOTGUN',      #added to PS
                    'Weapons Possession - Use of more than one of the above (W-MULTIPLE)':'W-MULTIPLE',         #added to PS
                    'Weapons Possesssion - Any firearm that is not handgun, rifle, or shotgun (W-OTHER)':'W-OTHER',
                    'Weapons Possession (W)':'W-WEAPON'}

#these are the the log subtypes for Staff Contact, Student Contact, Parent Contact, and Third Party in PS                    
commSubtypes={	 'Academics':	'ACADEMICS'
            	,'Attendance':	'ATTENDANCE'
            	,'Discipline':	'DISCIPLINE'
            	,'Enrollment':	'ENROLLMENT'
            	,'Home Visit':	'HOME VISIT'
            	,'Medical':	'MEDICAL'
            	,'Other':	'OTHER'
            	,'Parent initiated':	'PARENT INITIATED'
            	,'Positive':	'POSITIVE'
            	,'Reminder':	'REMINDER'
            	,'Scheduling Meeting':	'SCHEDULING MEETING'
            	,'Truancy 5 absences':	'TRUANCY 5 ABSENCES'
            	,'Truancy 9 absences':	'TRUANCY 9 ABSENCES'
            	,'Truancy 10 absences':	'TRUANCY 10 ABSENCES'
            	,'Truancy 15 absences':	'TRUANCY 15 ABSENCES'
            	,'Truancy 20 absences':	'TRUANCY 20 ABSENCES'
            	,'Truancy 15 tardies':	'TRUANCY 15 TARDIES'
            	,'Truancy 27 tardies':	'TRUANCY 27 TARDIES'
            	,'Truancy 45 tardies':	'TRUANCY 45 TARDIES'
            	,'Truancy 60 tardies':	'TRUANCY 60 TARDIES'
            	,'Truancy Unenroll':	'TRUANCY UNENROLL'
            	,'Sensitive':	'SENSITIVE'
               ,'Crisis Management': 'CRISIS MANAGEMENT'
               ,'Sensitive Parent Comm': 'SENSITIVE - PARENT'
               ,None: "NONE"
             }



#create default variables for start and end date as two weeks ago and the current date in format 'YYYY-MM-DD'
default_sdt = (datetime.datetime.today() - datetime.timedelta(days = 14)).strftime('%Y-%m-%d')
default_edt = datetime.datetime.today().strftime('%Y-%m-%d')



def convertUnicode(value):
    for i in unicodeErrors.keys():
        try:
            value = value.replace(i,unicodeErrors[i])
            value = value.encode('ascii','ignore')
        except UnicodeDecodeError:
            next
##        except AttributeError: #raised when value is None
##            next
    return value


def getReferrals(school):
    url='https://kippdc.deanslistsoftware.com/api/v1/referrals?'
    school=school.lower()
    url+='apikey='+apiKeys[school]
    referrals=requests.get(url).json()
    return referrals['data']

def getAllReferrals():
    allReferrals=[]
    for school in apiKeys:
        referrals=getReferrals(school)
        allReferrals.extend(referrals)
    return allReferrals
    

def getLists(school):
    url='https://kippdc.deanslistsoftware.com/api/v1/lists?'
    school=school.lower()
    url+='apikey='+apiKeys[school]
    lists=requests.get(url).json()
    return lists['data']

    
def getSessionsList(school):
    listSessions = []
    for l in getLists(school):
        url='https://kippdc.deanslistsoftware.com/api/v1/lists/'+str(l['ListID'])+'?'
        school=school.lower()
        url+='apikey='+apiKeys[school]
        session=requests.get(url).json()
        for s in session['Sessions']:
            try:
                sessionDate = {'ListName':session['ListName'],'Session':s['ManifestID'],'ListID':session['ListID'],'Date':s['EndDate']}
            except TypeError:
                sessionDate = {'ListName':session['ListName'],'Session':s,'ListID':session['ListID'], 'Date':s}
            listSessions.append(sessionDate)
    return listSessions

def getSessionListsStudents(school, sdt = default_sdt, edt = default_edt):
    '''
    school: school name
    sdt: default to two weeks ago
    edt: default to today
    '''
    school=school.lower()
    consequences = []
    for session in getSessionsList(school):
        dateInt = int(''.join(session['Date'].split('-')))
        sdtInt = int(sdt.replace('-',''))
        edtInt = int(edt.replace('-',''))
        if sdtInt<=dateInt<=edtInt:         #only access lists for days prior to the current date
            url='https://kippdc.deanslistsoftware.com/api/v1/lists/'+str(session['ListID'])+'/'+str(session['Session'])+'?'
            url+='apikey='+apiKeys[school]
            students = requests.get(url).json()['Items']
            for student in students:
                if student['ID'] is not None:
                    incidentPenaltyID = student['ID']
                else:
                    incidentPenaltyID = -1*int((str(session['ListID'])+str(session['Session'])+str(student['StudentSchoolID'])).replace("-","")) #combine listid, session, and studentID to create a unique ID from the lists
                studentConsequence = {'IncidentID':-1
                                     ,'PenaltyID':session['ListID']
                                     ,'ListName':session['ListName']  #PenaltyName  
                                     ,'EndDate':session['Date']  #date of list
                                     ,'StartDate':None
                                     ,'StudentSchoolID':student['StudentSchoolID']
                                     ,'NumDays':None
                                     ,'NumPeriods':None
                                     ,'SchoolID':schoolNameToID[school]
                                     ,'IncidentPenaltyID':incidentPenaltyID} #create unique ID that is replicable
                consequences.append(studentConsequence)
            #IPID = -1000  #IncidentPenatlyID starting ID
#    for c in consequences:  #add InicidentPenaltyID to list value
#        IPID-=1
#        c['IncidentPenaltyID']=IPID
    return consequences
    
def getAllSessionListsStudents(sdt = default_sdt, edt = default_edt):
    '''
    sdt: default to two weeks ago
    edt: default to today
    '''
    allStudents=[]
    for school in apiKeys:
        students=getSessionListsStudents(school,sdt,edt)
        allStudents.extend(students)
    return allStudents

        
def getSuspensions(school):
    url='https://kippdc.deanslistsoftware.com/api/v1/suspensions?'
    school=school.lower()
    url+='apikey='+apiKeys[school]
    suspensions=requests.get(url).json()
    return suspensions['data']

def getAllSuspensions():
    allSuspensions=[]
    for school in apiKeys:
        suspensions=getSuspensions(school)
        allSuspensions.extend(suspensions)
    return allSuspensions
    
def getBehavior(school,sdt = default_sdt, edt = default_edt):
    '''
    sdt=Date(YYYY-MM-DD) -- two weeks ago
    edt=Date(YYYY-MM-DD) -- default is current date
    '''
    url='https://kippdc.deanslistsoftware.com/api/beta/export/get-behavior-data.php?'
    school=school.lower()
    url+='apikey='+apiKeys[school]
    url+='&sdt='+str(sdt)
    url+='&edt='+str(edt)
    behaviorData=requests.get(url).json()
    return behaviorData['data']

def getAllBehavior(sdt = default_sdt, edt = default_edt):
    '''
    sdt=Date(YYYY-MM-DD) -- two weeks ago
    edt=Date(YYYY-MM-DD) -- default is current date
    '''
    allBehaviorData=[]
    for school in apiKeys:
        behaviorData=getBehavior(school,sdt,edt)
        allBehaviorData.extend(behaviorData)
    return allBehaviorData

def getHomework(school,sdt = default_sdt, edt = default_edt):
    '''
    sdt=Date(YYYY-MM-DD) -- two weeks ago
    edt=Date(YYYY-MM-DD) -- default is current date
    '''
    url='https://kippdc.deanslistsoftware.com/api/beta/export/get-homework-data.php?'
    school=school.lower()
    url=url+'apikey='+apiKeys[school]
    url+='&sdt='+str(sdt)
    url+='&edt='+str(edt)
    homeworkData=requests.get(url).json()
    return homeworkData['data']
    
def getAllHomework(sdt = default_sdt, edt = default_edt):
    '''
    sdt=Date(YYYY-MM-DD) -- two weeks ago
    edt=Date(YYYY-MM-DD) -- default is current date
    '''
    allHomeworkData=[]
    for school in apiKeys:
        homeworkData=getHomework(school,sdt,edt)
        allHomeworkData.extend(homeworkData)
    return allHomeworkData
    
    
def getIncidents(school):
    url='https://kippdc.deanslistsoftware.com/api/v1/incidents?'
    school=school.lower()
    url=url+'apikey='+apiKeys[school]+'&cf=Y'
    incidentsData=requests.get(url).json()
    return incidentsData['data']
    
def getAllIncidents():
    allIncidentsData=[]
    for school in apiKeys:
        print school
        incidentsData=getIncidents(school)
        allIncidentsData.extend(incidentsData)
    return allIncidentsData
    
def getStudents(school):
    url='https://kippdc.deanslistsoftware.com/api/beta/export/get-students.php?'
    school=school.lower()
    url=url+'apikey='+apiKeys[school]
    studentData=requests.get(url).json()
    return studentData['data']
    
def getAllStudents():
    allStudentsData=[]
    for school in apiKeys:
        studentsData=getStudents(school)
        allStudentsData.extend(studentsData)
    return allStudentsData
    
def getUsers(school):
    url='https://kippdc.deanslistsoftware.com/api/beta/export/get-users.php?'
    school=school.lower()
    url=url+'apikey='+apiKeys[school]+'&show_inactive=Y'
    usersData=requests.get(url).json()
    return usersData['data']

def getAllUsers():
    allUsersData=[]
    for school in apiKeys:
        usersData=getUsers(school)
        allUsersData.extend(usersData)
    for user in allUsersData:
        user['LastName'].replace(u'\xf3','o')
    return allUsersData
    
def getComms(school):
    print 'retrieving %s comms data...' % (school)
    url='https://kippdc.deanslistsoftware.com/api/beta/export/get-comm-data.php?'
    school=school.lower()
    url=url+'apikey='+apiKeys[school]
    commData=requests.get(url).json()
    return commData['data']

def getAllComms():
    allCommData=[]
    for school in apiKeys:
        commData=getComms(school)
        allCommData.extend(commData)
    return allCommData
    
def getBankBook(school):
    url='https://kippdc.deanslistsoftware.com/api/beta/bank/get-bank-book.php?'
    school=school.lower()
    url=url+'apikey='+apiKeys[school]
    paychecksData=requests.get(url).json()
    return paychecksData['data']

def getAllBankBook():
    allPaychecksData=[]
    for school in apiKeys:
        paychecksData=getBankBook(school)
        allPaychecksData.extend(paychecksData)
    return allPaychecksData
    
def getRosters(school):
    url='https://kippdc.deanslistsoftware.com/api/beta/export/get-roster-assignments.php?'
    school=school.lower()
    url=url+'apikey='+apiKeys[school]+'&rt=ALL'
    url=url+'&show_inactive=Y'
    rosterData=requests.get(url).json()
    alertsRemoved = [r for r in rosterData['data'] if r['IntegrationID'] not in ['Guardian','Medical','Special Education','Discipline']]
    for row in alertsRemoved:    
        row['FirstName']=convertUnicode(copy.deepcopy(row['FirstName']))
        row['LastName']=convertUnicode(copy.deepcopy(row['LastName']))
        row['MiddleName']=convertUnicode(copy.deepcopy(row['MiddleName']))
        row['RosterName']=convertUnicode(copy.deepcopy(row['RosterName']))
    return alertsRemoved
    
def getAllRosters():
    allRosterData=[]
    for school in apiKeys:
        rosterData=getRosters(school)
        allRosterData.extend(rosterData)
    return allRosterData
    
def getAttendance(school,sdt = default_sdt, edt = default_edt):
    '''
    sdt=Date(YYYY-MM-DD) -- two weeks ago
    edt=Date(YYYY-MM-DD) -- default is current date
    '''
    url='https://kippdc.deanslistsoftware.com/api/v1/daily-attendance?'
    school=school.lower()
    url=url+'apikey='+apiKeys[school]
    url+='&sdt='+str(sdt)
    url+='&edt='+str(edt)
    attendanceData=requests.get(url).json()
    for row in attendanceData['data']:
        #run unicode conversion on staff and student name fields
        row['StaffFirstName'] = convertUnicode(copy.deepcopy(row['StaffFirstName']))
        row['StaffMiddleName'] = convertUnicode(copy.deepcopy(row['StaffMiddleName']))
        row['StaffLastName'] = convertUnicode(copy.deepcopy(row['StaffLastName']))
        row['StudentFirstName'] = convertUnicode(copy.deepcopy(row['StudentFirstName']))
        row['StudentMiddleName'] = convertUnicode(copy.deepcopy(row['StudentMiddleName']))
        row['StudentLastName'] = convertUnicode(copy.deepcopy(row['StudentLastName']))
        if row['Behavior'] not in ['Present','Tardy','No Attendance Taken']:
            row['AttendanceCode'] = row['Behavior'].split(' ')[0].replace('"',"")
        elif row['Behavior'] == 'Present':
            row['AttendanceCode'] = None
        elif row['Behavior'] == 'Tardy':
            row['AttendanceCode'] = 'T'
        elif row['Behavior'] == 'No Attendance Taken':
            row['AttendanceCode'] = 'NA'
        else:
            row['AttendanceCode'] = '-----'
    return attendanceData['data']
    
def getAllAttendance(sdt = default_sdt, edt = default_edt):
    '''
    sdt=Date(YYYY-MM-DD) -- two weeks ago
    edt=Date(YYYY-MM-DD) -- default is current date
    '''
    allAttendanceData=[]
    for school in apiKeys:
        attendanceData=getAttendance(school,sdt,edt)
        allAttendanceData.extend(attendanceData)
    return allAttendanceData

def getClassAttendance(school,sdt = default_sdt, edt = default_edt):
    '''
    sdt=Date(YYYY-MM-DD) -- two weeks ago
    edt=Date(YYYY-MM-DD) -- default is current date
    '''
    url='https://kippdc.deanslistsoftware.com/api/v1/class-attendance?'
    school=school.lower()
    url=url+'apikey='+apiKeys[school]
    url+='&sdt='+str(sdt)
    url+='&edt='+str(edt)
    attendanceData=requests.get(url).json()
    for row in attendanceData['data']:
        #run unicode conversion on staff and student name fields
        row['StaffFirstName']=convertUnicode(copy.deepcopy(row['StaffFirstName']))
        row['StaffMiddleName']=convertUnicode(copy.deepcopy(row['StaffMiddleName']))
        row['StaffLastName']=convertUnicode(copy.deepcopy(row['StaffLastName']))
        row['StudentFirstName']=convertUnicode(copy.deepcopy(row['StudentFirstName']))
        row['StudentMiddleName']=convertUnicode(copy.deepcopy(row['StudentMiddleName']))
        row['StudentLastName']=convertUnicode(copy.deepcopy(row['StudentLastName']))
        row['AttendanceCode'] = None
    return attendanceData['data']
    
def getAllClassAttendance(sdt = default_sdt, edt = default_edt):
    '''
    sdt=Date(YYYY-MM-DD) -- two weeks ago
    edt=Date(YYYY-MM-DD) -- default is current date
    '''
    allAttendanceData=[]
    for school in apiKeys:
        attendanceData=getClassAttendance(school,sdt,edt)
        allAttendanceData.extend(attendanceData)
    return allAttendanceData

def mapIncidents(incidents):
    psData=[]
    errors=[]
    for incident in incidents:    
        if incident['Status'] == 'Resolved':# and incident['Infraction'] != 'Attendance Intervion': #logtypeid = 508
            customFields = {cf['FieldName']:cf['NumValue'] for cf in incident['Custom_Fields']}
            psRecord={}
            
            try:
                #print incidents.index(incident)
                psRecord['ID']=incident['IncidentID']
                psRecord['Student_Number']=int(incident['StudentSchoolID'])
                psRecord['SchoolID']=int(schoolid[incident['SchoolID']])
                if incident['Infraction'] == 'Attendance Intervention':
                    psRecord['LogTypeID']=508
                else:
                    psRecord['LogTypeID']=-100000
                psRecord['Category']=11
                try:                
                    psRecord['Subtype']=incidentSubtypes[incident['Infraction']] #subtype is varchar(20)
                except KeyError: #raised when incident infraction is not in the subtype list above. err
                    errors.append({'ID':incident['IncidentID'],'School':schoolName[incident['SchoolID']],'ErrorField':'Infraction', 'Error':'KeyError: Infraction: %s not a possible subtype' % (incident['Infraction'])}) 
                    psRecord['Subtype'] = None
                if incident['Infraction']=='Illicit Drug Related (D)':# or customFields['Drug Related']=='Y':
                    psRecord['Discipline_DrugRelatedFlag']=1
                else:
                    psRecord['Discipline_DrugRelatedFlag']=0
                if incident['Infraction']=='Alcohol Related (A)':
                    psRecord['Discipline_AlcoholRelatedFlag']=1
                else:
                    psRecord['Discipline_AlcoholRelatedFlag']=0
                try:        
                    if 'Weapons' in incident['Infraction'].split():
                        psRecord['Discipline_WeaponRelatedFlag']=1
                    else:
                        psRecord['Discipline_WeaponRelatedFlag']=0
                except AttributeError: #raised when Infraction is None because it cannot split NoneType to search for the word 'Weapons'
                    #add if custom_field['weapon related']  ==  Y then discipline_weaponrelatedflag = 1                    
                    psRecord['Discipline_WeaponRelatedFlag']=0
                psRecord['Discipline_PoliceInvolvedFlag']=0 #not sure this should always be zero
                psRecord['Discipline_IncidentDate']=time.strftime('%m/%d/%Y',time.strptime(incident['IssueTS']['date'].split(" ")[0],'%Y-%m-%d')) #IssueTS is the date of the incident 
                psRecord['Discipline_IncidentLocDetail']=incident['Location']
                psRecord['Discipline_ActionDate']=None
                psRecord['Discipline_ActionTakenEndDate']=None
                penaltyString = None #define penalty string 
                if len(incident['Penalties'])>0:   
                    penaltyString=incident['Penalties'][0]['PenaltyName']
                    if incident['Penalties'][0]['StartDate']!=None:
                        psRecord['Discipline_ActionDate']=time.strftime('%m/%d/%Y',time.strptime(incident['Penalties'][0]['StartDate'],'%Y-%m-%d'))
                    if incident['Penalties'][0]['EndDate']!=None:
                        psRecord['Discipline_ActionTakenEndDate']=time.strftime('%m/%d/%Y',time.strptime(incident['Penalties'][0]['EndDate'],'%Y-%m-%d'))
                    psRecord['Discipline_DurationAssigned']=incident['Penalties'][0]['NumDays']
                    if len(incident['Penalties'])>1:
                        for penalty in incident['Penalties'][1:]:
                            penaltyString+='; '
                            penaltyString+=penalty['PenaltyName']
                    for penalty in incident['Penalties']:
                        if penalty['PenaltyName']=='Police Referral':
                            psRecord['Discipline_PoliceInvolvedFlag']=1
                            
                #Clean up entry fields
                entryFields = ['ReportedDetails','AdminSummary','Context','AddlReqs','FamilyMeetingNotes']
                for field in entryFields:
                    
                    try:
                        incident[field]=str(convertUnicode(copy.deepcopy(incident[field])))
                    except AttributeError: #raised when field is None
                        incident[field] = None
                    except UnicodeEncodeError: #raised when unicode value cannot be converted
                        errors.append({'ID':incident['IncidentID'],
                                       'School':schoolName[incident['SchoolID']],
                                       'ErrorField':field, 
                                       'Error':'UnicodeEncodeError'}) 
                        incident[field]='N/A'
                    
                psRecord['Entry']=  'CONSEQUENCE: '              +str(penaltyString)              +' ***** '+\
                                    'REPORTED DETAILS: '         +'('+str(incident['CreateLast'])+', '+str(incident['CreateFirst'])+') '\
                                                                 +str(incident['ReportedDetails'])+' ***** '+\
                                    'ADMIN SUMMARY: '            +str(incident['AdminSummary'])   +' ***** '+\
                                    'CONTEXT NOTES: '            +str(incident['Context'])        +' ***** '+\
                                    'ADDITIONAL REQUIREMENTS: '  +str(incident['AddlReqs'])       +' ***** '+\
                                    'FAMILY MEETING NOTES: '     +str(incident['FamilyMeetingNotes'])
                
                psRecord['Discipline_Reporter']=str(incident['CreateLast'])+", "+str(incident['CreateFirst']) #does this need to be staff ID?
                psRecord['Entry_Date']=time.strftime('%m/%d/%Y',time.strptime(incident['IssueTS']['date'].split(" ")[0],'%Y-%m-%d'))  #set this to CreateTS because that is when the record was created in DL
                psRecord['Entry_Time']=incident['IssueTS']['date'].split(" ")[1]   #set this to CreateTS because that is when the record was created in DL
                psRecord['Entry_Author']=str(incident['UpdateLast'])+", "+str(incident['UpdateFirst']) #does this need to be staffID? 
                psData.append(psRecord)
            except TypeError:
                psRecord={}
                psRecord['School']=schoolName[incident['SchoolID']]
                psRecord['ID']=incident['IncidentID']
                psRecord['Error']='TypeError'
                psRecord['ErrorField'] = None
                errors.append(psRecord)
            except UnicodeEncodeError:
                psRecord={}
                psRecord['School']=schoolName[incident['SchoolID']]
                psRecord['ID']=incident['IncidentID']
                psRecord['Error']='UnicodeError'
                psRecord['ErrorField'] = None
                errors.append(psRecord)
    data={'psData':psData,'errors':errors}
    return data


    
    
def mapIncidentsARC(incidents):
    incidentList=[]
    penalties=[]
    errors = []
    
    #list of headers in the custom_DLIncidents_raw table    
    fields = [  'Actions',  'AddlReqs', 'AdminSummary', 'Alcohol Related','Category', 'CategoryID', 'CloseTS', 'Context',
                'CreateBy', 'CreateFirst', 'CreateLast', 'CreateMiddle','CreateTS', 'CreateTitle', 'Drug Related', 'FamilyMeetingNotes',
                'FollowupNotes', 'GradeLevelShort', 'HomeroomName', 'IncidentID','Infraction', 'InfractionTypeID', 'Injury Type', 'IsReferral', 'IssueTS',
                'Location', 'LocationID', 'Police Involved','ReportedDetails', 'ReturnDate', 'ReturnPeriod','ReviewTS',
                'SchoolID', 'SendAlert', 'Status','StatusID', 'StudentFirst', 'StudentID', 'StudentLast',
                'StudentMiddle', 'StudentSchoolID', 'UpdateFirst', 'UpdateLast','UpdateMiddle', 'UpdateTS', 'Weapon Related']#, 'Hearing']    
    #list of fields from about that contain dates
    dateFields = ['CloseTS','CreateTS','IssueTS','ReturnDate','UpdateTS','ReviewTS']
    #list of headers that are in custom_DLPenalties_raw table
    penaltyFields = ['StartDate', 'SchoolID', 'EndDate', 'NumPeriods', 'PenaltyID', 'IncidentID', 'PenaltyName','IncidentPenaltyID', 'NumDays']
    for incident in incidents:
        record = {}
        #create a dictionary of custom field names and values        
        customFields = {cf['FieldName']:cf['StringValue'] for cf in incident['Custom_Fields']}
        
        #loop through fields in field list (theses are the columns in custom_DLIncidents_raw)
        for field in fields:
            if field == 'Actions':
                record[field] = None
            elif field in customFields.keys():
                try:
                    record[field] = customFields[field]
                except KeyError: #raises error if field does not exist in API
                    errors.append({'ID':incident['IncidentID'],'School':incident['SchoolID'],'ErrorField':field, 'Error':'KeyError'}) 
                    record[field] =  'N/A'
            elif field in dateFields: #catch all the timestamp fields and get only the date
                try:
                    record[field] = incident[field]['date'].split(' ')[0] #only take the date from the datetime field
                except TypeError: #raises error if there is no value in the date field
                    record[field] = None
                except KeyError: #raises error if field does not exist in API
                    errors.append({'ID':incident['IncidentID'],'School':incident['SchoolID'],'ErrorField':field, 'Error':'KeyError'}) 
                    record[field] =  None
            else:
                try:    
                    record[field] = str(convertUnicode(copy.deepcopy(incident[field])))
                except UnicodeEncodeError: #raises error if unicode value in text field and not converted with convertUnicode(...)
                    errors.append({'ID':incident['IncidentID'],'School':incident['SchoolID'],'ErrorField':field,'Error':'UnicodeEncodeError'}) 
                    record[field] = 'N/A'
                except AttributeError: #raises error if value in API is none
                    errors.append({'ID':incident['IncidentID'],'School':incident['SchoolID'],'ErrorField':field,'Error':'AttributeError'})                    
                    record[field] = incident[field]
                except KeyError: #raises keyerror if field does not exist in API
                    errors.append({'ID':incident['IncidentID'],'School':incident['SchoolID'],'ErrorField':field,'Error':'KeyError'}) 
                    next
        #extract homeroom name from HomeroomName value
        try:
            start=record['HomeroomName'].find('(')+1
            end=record['HomeroomName'].find(')')
            record['HomeroomName']=record['HomeroomName'][start:end]
        except AttributeError:
            record['HomeroomName']=None #last record with incident ID -1 has no homeroom values
        #add the link record
        try:
            record['Link']='https://kippdc.deanslistsoftware.com/incidents/'+str(incident['IncidentID'])
        except KeyError:
            errors.append({'ID':incident['IncidentID'],'School':incident['SchoolID'],'ErrorField':'Link'})
            record['Link'] = 'N/A'
        #append mapped incident record to the list of incidents
        incidentList.append(record)     
        #add penalties to penalties list
        if len(incident['Penalties'])>0:
            for p in incident['Penalties']:
                p['StudentSchoolID']=incident['StudentSchoolID']
        penalties.extend(copy.deepcopy(incident['Penalties'])) #make a deep copy so the print key is not removed from the original 
    #loop through penalties and delete to remove the print T/F field -- corresponds to 'Show on Incident Letter' checkbox in DL  
    for p in penalties: #if field is not in table field list about, remove it from the dictionary
        for field in p.keys():
            if field not in penaltyFields:
                del p[field]
    #add a record with incidentid = -1 to join on the penalties tabl, because list records. have an incidentid of -1      
    incidentList.append({'IncidentID':-1})
    #create a dictionary that contains each of the three lists that is returned by this function        
    data = {'incidents':incidentList, 'errors':errors, 'penalties':penalties}
    return data
                    
        
        
def mapComms(commsData):
    print "mapping comms data..."
    psData=[]
    errors=[]
    users={}
    for user in getAllUsers(): #fill dictionary users with userID : username key/value pairs
        
        try: #do unicode conversions on user last name
            user['LastName'] = str(convertUnicode(copy.deepcopy(user['LastName'])))
        except AttributeError: #raised when value is none -- this should never happen
            user['LastName'] = None
            errors.append({'ID':user['DLUserID'],
                           'School':schoolName[user['DLSchoolID']],
                           'ErrorField':'LastName', 
                           'Error':'AttributeError'})
        except UnicodeEncodeError: #raised when unicode value cannot be converted
            user['LastName'] = None
            errors.append({'ID':user['DLUserID'],
                           'School':schoolName[user['DLSchoolID']],
                           'ErrorField':'LastName', 
                           'Error':'UnicodeEncodeError'})
        
        try: #do unicode conversions on user first name
            user['FirstName'] = str(convertUnicode(copy.deepcopy(user['FirstName'])))
        except AttributeError: #raised when value is none -- this should never happen
            user['FirstName'] = None
            errors.append({'ID':user['DLUserID'],
                           'School':schoolName[user['DLSchoolID']],
                           'ErrorField':'FirstName', 
                           'Error':'AttributeError'})
        except UnicodeEncodeError: #raised when unicode value cannot be converted
            user['FirstName'] = None
            errors.append({'ID':user['DLCallLogID'],
                           'School':schoolName[user['DLSchoolID']],
                           'ErrorField':'FirstName', 
                           'Error':'UnicodeEncodeError'})
        users[user['DLUserID']]=str(user['LastName'])+', '+str(user['FirstName']) #add user to users dictionary userID : username
    for comm in commsData:      
        
        psRecord={}  #create empty dictionary to store the record

        psRecord['Entry_Author']=users[comm['DLUserID']]  #get entry auther for the users list created above
        psRecord['Entry_Date']=time.strftime('%m/%d/%Y',time.strptime(comm['CallDateTime'].split()[0],'%Y-%m-%d')) #get the date of the communication and convert it to mm/dd/yyyy format
        psRecord['Entry_Time']=comm['CallDateTime'].split()[1]  #get the time for the communication
        psRecord['Category']=10     #####'DL Communication category in powerschool.log table
        
        #Clean up entry fields
        entryFields = ['CallTopic','Reason','PersonContacted','Response','FollowupRequest','FollowupResponse']  #all fields that take free form text
        for field in entryFields:
            try:
                comm[field]=str(convertUnicode(copy.deepcopy(comm[field])))
            except AttributeError: #raised when field is None
                comm[field] = None
            except UnicodeEncodeError: #raised when unicode value cannot be converted
                errors.append({'ID':comm['DLCallLogID'],
                               'School':schoolName[comm['DLSchoolID']],
                               'ErrorField':field, 
                               'Error':'UnicodeEncodeError'}) 
                comm[field]='N/A'           
                
        #create the entry
        if comm['CallType'] == 'P':  #call type is phone call
            psRecord['Entry'] = str(comm['PersonContacted'])+' ('+str(comm['CommWith'])+': '+str(comm['Relationship'])+')'+' ***** '+\
                                str(comm['CallType'])+' - '+str(comm['CallStatus'])+' - '+str(comm['PhoneNumber'])+' ***** '+\
                                'CALL TOPIC: '+str(comm['CallTopic'])+' ***** '+\
                                'RESPONSE: '+str(comm['Response'])+' ***** '+\
                                'FOLLOWUP REQUEST: '+str(comm['FollowupRequest'])+' ***** '+\
                                'FOLLOWUP RESPONSE: '+str(comm['FollowupResponse'])
        elif comm['CallType'] == 'E': #call type is email
            psRecord['Entry'] = str(comm['PersonContacted'])+' ('+str(comm['CommWith'])+': '+str(comm['Relationship'])+')'+' ***** '+\
                                str(comm['CallType'])+' - '+str(comm['CallStatus'])+' - '+str(comm['Email'])+' ***** '+\
                                'CALL TOPIC: '+str(comm['CallTopic'])+' ***** '+\
                                'RESPONSE: '+str(comm['Response'])+' ***** '+\
                                'FOLLOWUP REQUEST: '+str(comm['FollowupRequest'])+' ***** '+\
                                'FOLLOWUP RESPONSE: '+str(comm['FollowupResponse'])
        elif comm['CallType'] == 'IP': #call type is in person
            psRecord['Entry'] =  str(comm['PersonContacted'])+' ('+str(comm['CommWith'])+': '+str(comm['Relationship'])+')'+' ***** '+\
                                str(comm['CallType'])+' ***** '+\
                                'CALL TOPIC: '+str(comm['CallTopic'])+' ***** '+\
                                'RESPONSE: '+str(comm['Response'])+' ***** '+\
                                'FOLLOWUP REQUEST: '+str(comm['FollowupRequest'])+' ***** '+\
                                'FOLLOWUP RESPONSE: '+str(comm['FollowupResponse'])
        elif comm['CallType'] == '': #call type is none (comms with students (STU) or other staff member (ED)) 
            psRecord['Entry'] =  str(comm['PersonContacted'])+' ('+str(comm['CommWith'])+': '+str(comm['Relationship'])+')'+' ***** '+\
                                str(comm['CallType'])+' ***** '+\
                                'CALL TOPIC: '+str(comm['CallTopic'])+' ***** '+\
                                'RESPONSE: '+str(comm['Response'])+' ***** '+\
                                'FOLLOWUP REQUEST: '+str(comm['FollowupRequest'])+' ***** '+\
                                'FOLLOWUP RESPONSE: '+str(comm['FollowupResponse'])
        elif comm['CallType']=='3P':
            psRecord['Entry'] = str(comm['PersonContacted'])+' ('+str(comm['CommWith'])+' -- '+str(comm['ThirdParty'])+': '+str(comm['Relationship'])+')'+' ..... '+\
                                str(comm['CallType'])+' ..... '+\
                                'CALL TOPIC: '+str(comm['CallTopic'])+' ..... '+\
                                'RESPONSE/FOLLOWUP: '+str(comm['Response'])+' ..... '+\
                                'FOLLOWUP REQUEST: '+str(comm['FollowupRequest'])+' ***** '+\
                                'FOLLOWUP RESPONSE: '+str(comm['FollowupResponse'])
                                
        psRecord['SchoolID']=int(schoolid[comm['DLSchoolID']]) #set Powerschool schoolID
        
        #set the logtypeID -- should 
        if comm['CommWith']=='REL' or comm['CommWith']=='P': #########################add subtypes
            psRecord['LogTypeID']=507  #Parent Contact
        elif comm['CommWith']=='ED':
            psRecord['LogTypeID']=6145 #Staff Contact
        elif comm['CommWith']=='STU':
            psRecord['LogTypeID']=6143 #Student Contact
        elif comm['CommWith'] == '3P':
                psRecord['LogTypeID'] = 6982 #Third Party
        try:
            psRecord['Subtype']=commSubtypes[comm['Reason']]
        except KeyError:
            psRecord['Subtype']=None
            errors.append({'ID':comm['DLCallLogID'],
               'School':schoolName[user['DLSchoolID']],
               'ErrorField':'Reason', 
               'Error':'KeyError'})
               
        psRecord['Student_Number']=int(comm['StudentSchoolID']) #set the student number
        
        psRecord['ID']=comm['DLCallLogID'] #set log id to DLCallLogID
        
        psData.append(psRecord)
        
        data={'psData':psData,'errors':errors}
    return data


    
    
def mapCommsARC(comms):
    commsList = []
    errors = []
    #list of headers from custom_DLComms_raw table
    commsFields = ['CallDateTime',	'CallStatus','CallTopic','CallType','CommWith','DLCallLogID'
                  ,'DLSchoolID',	'DLStudentID','DLUserID','Email','FollowupBy','FollowupCloseTS'
                  ,'FollowupID','FollowupInitTS','FollowupOutstanding','FollowupRequest'
                  ,'FollowupResponse','PersonContacted','PhoneNumber','Reason','Relationship'
                  ,'Response','SchoolName','SecondaryStudentID','StudentSchoolID','UserSchoolID']
    for comm in comms:
        record = {}
        for field in commsFields:
            try:
                record[field] = str(convertUnicode(copy.deepcopy(comm[field]))) #used deepcopy because it was returning original string without making the unicode replacement
            except UnicodeEncodeError: #raises error if field value can't be converted to string
                errors.append({'ID':comm['DLCallLogID'],'School':comm['DLSchoolID'],'ErrorField':field,'Error':'UnicodeEncodeError'})
                record[field] == None
            except UnicodeDecodeError: #'ascii' codec can't decode byte 0xa0 in position 0: ordinal not in range(128) --- Investigate this!
                errors.append({'ID':comm['DLCallLogID'],'School':comm['DLSchoolID'],'ErrorField':field,'Error':'UnicodeDecodeError'})
                record[field]=copy.deepcopy(comm[field].decode("ascii",'ignore'))
            except AttributeError: #raises error if field value is None
                record[field] = None
            except KeyError: #raises error if field does not exist in API
                errors.append({'ID':comm['DLCallLogID'],'School':comm['DLSchoolID'],'ErrorField':field, 'Error':'KeyError'}) 
                record[field] =  None
            #create record link
            record['Link']='https://kippdc.deanslistsoftware.com/comm/edit-comm.php?id='+str(comm['DLCallLogID'])
        #append mapped record to commsList
        commsList.append(record)
    #create dictionary to be returned
    data = {'comms':commsList, 'errors':errors}
    return data
    
        
def mapPaychecks(data):
    psData=[]
    rostersByStudent={}
    rosters=getAllRosters()
    #create where student ID is the key and a dictionary of rosters is the value.
    #SecondaryIntegrationID is equal to PS SectionID
    for roster in rosters:
        if roster['StudentSchoolID'] in rostersByStudent.keys():
            rostersByStudent[roster['StudentSchoolID']][roster['RosterName']]=roster['SecondaryIntegrationID'] #adds key/value pair to student dictionary
        else:
            rostersByStudent[roster['StudentSchoolID']]={roster['RosterName']:roster['SecondaryIntegrationID']} #creates the first key/value pair in the student dictionary
    
    for behavior in data:
        if behavior['DLSchoolID'] in ['80','81','82','83','84','85','75']: #[AIM,KEY,NE,Valor,WILL,Heights] All use Paychecks. Will need to be updated each year if new schools use Paychecks
            psRecord={}
            psRecord['Student_Number']=behavior['StudentSchoolID']
            psRecord['FullName']=str(behavior['StudentLastName'])+', '+str(behavior['StudentFirstName'])
            psRecord['LastName']=behavior['StudentLastName']
            psRecord['FirstName']=behavior['StudentFirstName']
            psRecord['Schoolid']=int(schoolid[behavior['DLSchoolID']])
            psRecord['SchoolName']=schoolName[behavior['DLSchoolID']]
            psRecord['StaffFullName']=str(behavior['StaffLastName'])+', '+str(behavior['StaffFirstName'])
            try:
                psRecord['SectionID']=rostersByStudent[behavior['StudentSchoolID']][behavior['Roster']] #uses the studentID (student_number) roster name attached to the px to get the sectionID (secondaryIntegrationID)
            except KeyError: #raised when roster in behavior id none
                psRecord['SectionID']=99999
            except AttributeError:  #unclear why this is here but not hurting anything
                psRecord['SectionID']=None
            except TypeError:       #unclear why this is here but not hurting anything
                psRecord['SectionID']=None
            psRecord['BehaviorCategory']=behavior['BehaviorCategory']
            psRecord['Behavior']=behavior['Behavior']
            psRecord['PointValue']=int(behavior['PointValue'])
            psRecord['BehaviorDate']=behavior['BehaviorDate']
            psRecord['SourceSystem']='DeansList'
            psRecord['Roster']=behavior['Roster']
            psData.append(psRecord)
    return psData




def writeCSV(data,delimiter,filename):
    '''
    write list of dictionaries to csv
    errorFields = list of fields to go in error csv
    '''
    #print "writing CSV..."
    toCSV=data
    keys=sorted(toCSV[0].keys())
    with open(filename+'.txt','wb') as output_file:
        dict_writer = csv.DictWriter(output_file,keys,delimiter=delimiter,quoting=csv.QUOTE_ALL)
        dict_writer.writeheader()
        #dict_writer.writerows(toCSV)
        for row in toCSV:
            dict_writer.writerow(row)


