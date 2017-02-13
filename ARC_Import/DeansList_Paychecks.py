import os
os.chdir('C:\ARC_Integration\DeansList\Scripts')
import DeansList_Master as dl

behavior = dl.getAllBehavior()#sdt='2015-08-10')
homework = dl.getAllHomework()#sdt='2015-08-10')
att = dl.getAllAttendance()#sdt='2015-08-10')
classAtt = dl.getClassAttendance('KCP')#,sdt='2015-08-10')

px = []
px.extend(behavior)
px.extend(homework)
px.extend(att)
px.extend(classAtt)

pxMapped = dl.mapPaychecks(px)

dl.writeCSV(pxMapped,',','C:\ARC_Integration\DeansList\Data\DLPaychecksForARC')
