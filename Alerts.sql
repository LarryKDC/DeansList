select 
student_number,
'Discipline' "Alert Type",
alert_discipline "Alert Text"
from PSSIS_Student_Alerts
where alert_discipline is not null
and (alert_disciplineexpires>=sysdate or alert_disciplineexpires='01-JAN-1900')

union all

select 
student_number,
'Guardian' "Alert Type",
alert_guardian "Alert Text"
from PSSIS_Student_Alerts
where alert_guardian is not null
and (alert_guardianexpires>=sysdate or alert_guardianexpires='01-JAN-1900')

union all

select 
student_number,
'Medical' "Alert Type",
alert_medical "Alert Text"
from PSSIS_Student_Alerts
where alert_medical is not null
and (alert_medicalexpires>=sysdate or alert_medicalexpires='01-JAN-1900' or alert_medicalexpires is null)

union all

select 
s.student_number,
'Special Education',--ps_customfields.getcf('Students',s.id,'sped_funding'),
Null
from students s
where s.enroll_status = 0
and ps_customfields.getcf('Students',s.id,'sped_funding') is not null
