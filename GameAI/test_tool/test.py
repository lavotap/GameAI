#!/usr/bin/env python
#-*-coding:utf-8-*-

# 测试数据分析工具，生成excel数据格式以供分析数据，仅在test模式开启时有效

from pyExcelerator import *
import os
import re

# List out ./log/(log documents).
log_path=os.getcwd()+'/log/'

log_file=os.listdir(log_path)
sort_file=[]

if_conpred=re.compile("^Conpred_[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}:[0-9]{2}:[0-9]{2}[.]log$")
if_dispred=re.compile("^Dispred_[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}:[0-9]{2}:[0-9]{2}[.]log$")

num=0
ans=''
while not ans:
    ans=raw_input("Test of Con_pred or Dis_pred?[Con_pred] ")
    if ans=='':
        ans='C'
    else:
        if_ans=re.compile('^'+ans,re.IGNORECASE)
        if if_ans.match('Con_pred'):
            ans='C'
        elif if_ans.match('Dis_pred'):
            ans='D'
        else:
            print("Please input 'Con_pred' or 'Dis_pred'!")
            ans=''

for f in log_file:
    if (ans=='C' and if_conpred.match(f)):
        sort_file.append(f)
    elif (ans=='D' and if_dispred.match(f)):
        sort_file.append(f)

sort_file.sort()

ten_sort_file=sort_file[-10:]

print(log_path)
for f in ten_sort_file:
    print("\t["+str(num)+"] "+f)
    num+=1

# Choose a log document.
default_log_doc=ten_sort_file[-1]
log_doc=''
while not log_doc:
    log_doc=raw_input("Please choose a log document.{default:["+str(num-1)+"] "+default_log_doc+"} ")

    if log_doc=='':
        log_doc=default_log_doc

    else:
        # If input a number.
        can_int=True
        try:
            list_num=int(log_doc)
        except:
            can_int=False

        if can_int:
            if list_num<num:
                log_doc=ten_sort_file[list_num]
            else:
                print("Number is out of list!")
                log_doc=''
        else:
            if not log_doc in sort_file:
                print("Log document "+log_doc+" does not esist!")
                log_doc=''


# Open the log document.
open_doc=open(log_path+log_doc,'r')

# Write into an excel document.
TEST=re.compile("^TEST:\[(?P<Test_status>.{11})\]:Vector(?P<Test_vector>.*)[.]$")
STEP=re.compile("^STEP:\[number\]:(?P<Step>.*)[.]$")
RUDDER=re.compile("^BACKTRACK:<rudder>:Turn (?P<Rudder_direct>left|right|straight).*$")
ANGLE=re.compile("^ANGLE:<rudder>:Theoretic delta angle is (?P<T_angle>.*?); real delta angle is (?P<R_angle>.*?);.*$")

excel_doc=Workbook()
excel_sheet=excel_doc.add_sheet('test')

if ans=='C':
    excel_sheet.write(0,0,'x')
    excel_sheet.write(0,1,'y')
    excel_sheet.write(0,2,'status')
    excel_sheet.write(0,3,'direct')
    excel_sheet.write(0,4,'t_angle')
    excel_sheet.write(0,5,'r_angle')
elif ans=='D':
    excel_sheet.write(0,0,'x')
    excel_sheet.write(0,1,'y')
    excel_sheet.write(0,2,'status')

row_test=1
row_rudder=1
row_angle=1
aline=(open_doc.readline())[:-1]
while aline:
    test=TEST.match(aline)
    rudder=RUDDER.match(aline)
    angle=ANGLE.match(aline)
    if test:
        status=test.group('Test_status')
        vector=test.group('Test_vector')
        vector=eval(vector)
        excel_sheet.write(row_test,0,vector[0])
        excel_sheet.write(row_test,1,vector[1])
        excel_sheet.write(row_test,2,status)
        row_test+=1
    elif rudder:
        direct=rudder.group('Rudder_direct')
        excel_sheet.write(row_rudder,3,direct)
        row_rudder+=1
    elif angle:
        t_angle=angle.group('T_angle')
        r_angle=angle.group('R_angle')
        excel_sheet.write(row_angle,4,t_angle)
        excel_sheet.write(row_angle,5,r_angle)
        row_angle+=1

    aline=(open_doc.readline())[:-1]


excel_doc.save('./analyse/'+log_doc[:-4]+'.xls')
