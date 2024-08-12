import pandas as pd 
import streamlit as st 
import os
import numpy as np
import random
import time
from pathlib import Path
#from streamlit_gsheets import GSheetsConnection
from datetime import datetime

st.set_page_config(
    page_title = 'DAILY LINE LIST',
    page_icon =":bar_chart"
    )
cola, colb, colc = st.columns(3)
colb.subheader('DAILY LINE LISTS')
ex = r'ALL.xlsx'
df = pd.read_excel(ex)



today = datetime.now()
cola, colb, colc = st.columns(3)
todayd = today.strftime("%d-%m-%Y ")
#cola.write(f'**CURRENT DATE: {today}**')
cola.markdown(f"TODAY'S DATE: {todayd}")


current_time = time.localtime()
k = time.strftime("%V", current_time)
t = int(k) + 13
#cola,colb,colc = st.columns([1,2,1])
colb.write(f'**CURRENT WEEK IS: {k}**')
colc.write(f'**SURGE WEEK IS: {t}**')

t = int(k) + 13
df['DISTRICT'] = df['DISTRICT'].astype(str)
dist = df['DISTRICT'].unique()

st.write('**FILTER BY:**')

cola, colb, colc = st.columns(3)
df['FACILITY'] = df['FACILITY'].astype(str)
faca = df['FACILITY'].unique()

#THE TIMES
dy = today.strftime("%d")
day = int(dy)
tom = int(day+1)

wk = int(t)
nexw = int(wk+1)

m = today.strftime("%m")
mon = int(m)
nexm = int(mon+1)
lasm = int(mon-1)

a31 = [1,3,5,7,8,10,12]
a30 = [4,6,9,11]

if mon in a31:
    if day == 31:
        tom ==1
elif mon in a30:
    if day == 30:
        tom ==1
elif mon == 2:
    if day ==28:
        tom =1
else:
    pass

if mon ==12:
    nexm ==1
elif mon == 1:
    lasm = 12
else:
    pass



dis = cola.selectbox('**BY DISTRICT**', dist, index=None)

if not dis:
    df = df.copy()
else:
    df['DISTRICT'] = df['DISTRICT'].astype(str)
    df = df[df['DISTRICT']== dis].copy()
    df['FACILITY'] = df['FACILITY'].astype(str)
    faca = df['FACILITY'].unique()

fac = colb.selectbox('**BY FACILITY**', faca, index=None)

if not fac:
    df = df.copy()
else:
    df['FACILITY'] = df['FACILITY'].astype(str)
    df = df[df['FACILITY']==fac]

times = ['TODAY', 'TOMORROW', 'THIS WEEK', 'NEXT WEEK', 'LAST MONTH', 'THIS MONTH', 'NEXT MONTH']

tm = colc.selectbox('**BY TIME**', times, index=0)

if not tm:
    df = df.copy()
elif tm == 'TODAY':
    df[['Ryear', 'Rmonth', 'Rday']] = df[['Ryear', 'Rmonth', 'Rday']].apply(pd.to_numeric, errors='coerce')
    df =df[((df['Ryear']==2024) & (df['Rmonth']==mon) & (df['Rday'] == day))].copy()
elif tm == 'TOMORROW':
    df[['Ryear', 'Rmonth', 'Rday']] = df[['Ryear', 'Rmonth', 'Rday']].apply(pd.to_numeric, errors='coerce')
    df =df[((df['Ryear']==2024) & (df['Rmonth']==mon) & (df['Rday'] == tom))].copy()
elif tm == 'THIS WEEK':
    df['WEEK'] = pd.to_numeric(df['WEEK'], errors='coerce')
    df = df[df['WEEK']==wk]
elif tm == 'NEXT WEEK':
    df['WEEK'] = pd.to_numeric(df['WEEK'], errors='coerce')
    df = df[df['WEEK']==nexw]
elif tm == 'LAST MONTH':
    df['Rmonth'] = pd.to_numeric(df['Rmonth'], errors='coerce')
    df =df[df['Rmonth']==lasm].copy()  
elif tm == 'THIS MONTH':
    df['Rmonth'] = pd.to_numeric(df['Rmonth'], errors='coerce')
    df =df[df['Rmonth']==mon].copy() 
elif tm == 'NEXT MONTH':
    df['Rmonth'] = pd.to_numeric(df['Rmonth'], errors='coerce')
    df =df[df['Rmonth']==nexm].copy()  

if tm == 'LAST MONTH':
    st.write('**NOTE, LINE LISTS OF LAST MONTH MEAN THE CLIENTS DID NOT RECEIVE THESE SERVICES**')
else:
    pass

#######APPOINTMENT
appt = df.shape[0]
ap = df.shape[0]
if appt == 0:
    appt = 'NO'
cola, colb, colc = st.columns([2,2,1])


cola, colb = st.columns([1,1])

if tm == 'LAST MONTH':
    ten = 'were'
    tan = 'WHICH SERVICES THEY MIGHT HAVE MISSED'
elif tm == 'NEXT WEEK' or tm == 'TOMORROW' or tm == 'NEXT MONTH':
    ten = 'will be'
    tan = 'THAT THEY ALL ATTEND'
else:
    ten = 'are'
    tan = 'THAT THEY ALL ATTEND'
cola.markdown(f'**{tm}, {appt} clients {ten} on appointment**')
if appt =='NO':
    st.write(f'**NO LINELIST TO SHOW FOR {tm}**')
    st.stop()
else:
    pass
colb.markdown(f'**FOLLOW UP TO SEE {tan}**')


#####VL SECTION

df['VL STATUS'] = df['VL STATUS'].astype(str)

vl = df[df['VL STATUS']=='DUE'].copy()
vl = vl.shape[0]



#######2 MONTHS BLEEDING WINDOW

df['DIFF'] = pd.to_numeric(df['DIFF'], errors='coerce')

two = df[df['DIFF'].isin([1,2])].copy()

tw = two.shape[0]

########ADOLS
df['ADOL'] = df['ADOL'].astype(str)

adol = df[df['ADOL']=='REBLEED'].copy()
adv = adol.shape[0]


########PMTCT VL

df['3 MONTH'] = df['3 MONTH'].astype(str)

pm = df[df['3 MONTH']=='DUE'].copy()

prev = pm.shape[0]


########TPT
df['INITIATE_TPT?'] = df['INITIATE_TPT?'].astype(str)

tpt = df[df['INITIATE_TPT?']=='INITIATE'].copy()
tp = tpt.shape[0]


########TPT AFTER TB
df['REINITIATE TPT'] = df['REINITIATE TPT'].astype(str)

tba = df[df['REINITIATE TPT']=='REINITIATE TPT'].copy()
tpa = tba.shape[0]



########CERVICAL CANCER
df['CX_STATUS'] = df['CX_STATUS'].astype(str)
cx = df[df['CX_STATUS']=='SCREEN'].copy()
sc = cx.shape[0]


########CERVICAL CANCER RESCREENING

df['RESCREEN'] = df['RESCREEN'].astype(str)

resc = df[df['CX_STATUS']=='RESCREEN'].copy()
res = resc.shape[0]


########NON SUPPRESSORS
df['SUPPRESSION'] = df['SUPPRESSION'].astype(str)

ns = df[df['SUPPRESSION']=='NS'].copy()

hlv = ns.shape[0]


########LOW LEVEL VIREMIA
df['VIREMIA'] = df['VIREMIA'].astype(str)

vir = df[df['VIREMIA']=='LLV'].copy()
llv = vir.shape[0]


########NOT ON DTG
df['NOT'] = df['NOT'].astype(str)

dtg = df[df['NOT']=='NOT ON DTG'].copy()
dt = dtg.shape[0]



########PREGNANT
df['PT'] = df['PT'].astype(str)

pr = df[df['PT']=='YES'].copy()
preg = pr.shape[0]

  
if not dis:
    d = 'ALL'
else:
    d = dis

if not fac:
    f = 'ALL'
else:
    f = fac

cola, colb, colc = st.columns([1,2,1])
colb.write('**SUMMARY**')

cola, colb = st.columns(2)

with cola:
    st.write(f'**DISTRICT : {d}**')
    st.write(f'**FACILITY : {f}**')
    st.write(f'**PERIOD : {tm}**')
    st.write(f'**ON APPT : {ap}**')
    st.write(f'**DUE FOR VL : {vl}**')
    st.write(f'**DUE IN 2 MONTHS : {tw}**')
    st.write(f'**ADOLS FOR VL : {adv}**')
    st.write(f'**MOTHERS FOR VL : {prev}**')

with colb:
    st.write(f'**HLVs : {hlv}**')
    st.write(f'**LLVs : {llv}**')
    st.write(f'**FOR TPT : {tp}**')
    st.write(f'**TPT AFTER TB : {tpa}**')
    st.write(f'**CX CANCER : {sc}**')
    st.write(f'**CX RESCREEN : {res}**')
    st.write(f'**MOTHERS ON APPT : {preg}**')
    st.write(f'**NOT ON DTG : {dt}**')
    