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
st.write('')
st.divider()
#######APPOINTMENT
appt = df.shape[0]
if appt == 0:
    appt = 'NO'
cola, colb, colc = st.columns([2,2,1])
colb.write('**APPOINTMENT**')

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


with st.expander(f"**CLIK TO VIEW {tm}'s APPT**"):
        apptdf = df[['FACILITY','ART', 'RETURN DATE', 'VL STATUS', 'CX_STATUS', 'RESCREEN', 'SUPPRESSION', 'NOT', 'INITIATE_TPT?']].copy()
        apptdf = apptdf.set_index('FACILITY')
        st.write (apptdf)

st.divider()

#####VL SECTION
cola, colb, colc = st.columns([2,2,1])
colb.write('**VL SECTION**')

df['VL STATUS'] = df['VL STATUS'].astype(str)

vl = df[df['VL STATUS']=='DUE'].copy()

vl = vl[['FACILITY', 'ART','RETURN DATE', 'VL DATE', 'VL STATUS']].copy()
vl = vl.set_index('FACILITY')
a = vl.shape[0]

if a == 1:
    statement = 'ONE CLIEN IS DUE FOR VL'
elif a >1:
    statement = f'{a} ARE DUE FOR VL'
else:
    statement = f'NO ONE IS DUE FOR VL'


#######2 MONTHS BLEEDING WINDOW

df['DIFF'] = pd.to_numeric(df['DIFF'], errors='coerce')

two = df[df['DIFF'].isin([1,2])].copy()

two = two[['FACILITY','ART', 'RETURN DATE','VL DATE']].copy()
two = two.set_index('FACILITY')
b = two.shape[0]

if b == 1:
    statement2 = f'ONE CLIENT  ON APPT {tm} IS DUE FOR VL IN TWO MONTHS, BLEED THEM'
elif b >1:
    statement2 = f'{b} CLIENTS ON APPT {tm} ARE DUE FOR VL IN TWO MONTHS, BLEED THEM'
else:
    statement2 = f'NO CLIENT ON APPT {tm} IS DUE FOR VL IN TWO MONTHS'

#cola, colb = st.columns([1,2])


if a ==0:
    st.write(f'**{statement2}**')
    pass
else:
    st.write(f'**{statement}**')
    with st.expander(f'**CLICK TO VIEW CLIENTS ON APPT {tm} THAT ARE DUE FOR VL**'):
        st.write(vl)

cola, colb, colc = st.columns([2,2,1])
colb.write('**2 month bleeding window**')
st.write('')

if b ==0:
    st.write(f'**{statement2}**')
    pass
else:
    st.write(f'**{statement2}**')
    with st.expander(f'**CLICK TO VIEW CLIENTS ON APPT {tm} THAT ARE DUE FOR VL IN TWO MONTHS**'):
        st.write(two)

st.write('')

########ADOLS
cola, colb, colc = st.columns([2,2,1])
colb.write('**6 month VL for adolscents and children**')
st.write('')
df['ADOL'] = df['ADOL'].astype(str)

adol = df[df['ADOL']=='REBLEED'].copy()

adol = adol[['FACILITY','ART', 'AG','RETURN DATE','VL DATE']].copy()
adol = adol.set_index('FACILITY')
b = adol.shape[0]

if b == 1:
    statement2 = f'ONE ADOLSCENT ON APPT {tm} IS DUE FOR THEIR 6 MONTHS VL, BLEED THEM'
elif b >1:
    statement2 = f'{b}  ADOLSCENTS ON APPT {tm} ARE DUE FOR THEIR 6 MONTHS VL, BLEED THEM'
else:
    statement2 = f'NO ADOLSCENT ON APPT {tm} IS DUE FOR THEIR 6 MONTHS VL'

if b ==0:
    st.write(f'**{statement2}**')
    pass
else:
    st.write(f'**{statement2}**')
    with st.expander(f'**CLICK TO VIEW ADOLSCENTS ON APPT {tm} THAT ARE DUE FOR THEIR 6 MONTHS VL**'):
        st.write(adol)

st.write('')

########PMTCT VL
cola, colb, colc = st.columns([2,2,1])
colb.write('**3 Months VL for pregnant mothers**')
st.write('')
df['3 MONTH'] = df['3 MONTH'].astype(str)

pm = df[df['3 MONTH']=='DUE'].copy()

pm = pm[['FACILITY','ART', 'PT','RETURN DATE','VL DATE']].copy()
pm = pm.set_index('FACILITY')
b = pm.shape[0]

if b == 1:
    statement2 = f'ONE MOTHER ON APPT {tm} IS DUE FOR THEIR 3 MONTHS VL, BLEED HER'
elif b >1:
    statement2 = f'{b}  MOTHER ON APPT {tm} ARE DUE FOR THEIR 3 MONTHS VL, BLEED THEM'
else:
    statement2 = f'NO MOTHER ON APPT {tm} IS DUE FOR HER 3 MONTHS VL'

if b ==0:
    st.write(f'**{statement2}**')
    pass
else:
    st.write(f'**{statement2}**')
    with st.expander(f'**CLICK TO VIEW MOTHERS ON APPT {tm} THAT ARE DUE FOR THEIR 3 MONTHS VL**'):
        st.write(pm)

st.divider()

st.write('')

########TPT
cola, colb, colc = st.columns([2,2,1])
colb.write('**TPT SECTION**')
st.write('')
df['INITIATE_TPT?'] = df['INITIATE_TPT?'].astype(str)

tpt = df[df['INITIATE_TPT?']=='INITIATE'].copy()

tpt = tpt[['FACILITY','ART', 'AG','ART START DATE','RETURN DATE','TPT']].copy()
tpt = tpt.set_index('FACILITY')
b = tpt.shape[0]

if b == 1:
    statement2 = f'ONE CLIENT ON APPT {tm} IS ELLIGIBLE FOR TPT'
elif b >1:
    statement2 = f'{b} CLIENTS ON APPT {tm} ARE ELLIGIBLE FOR TPT'
else:
    statement2 = f'NO CLIENT ON APPT {tm} IS ELLIGIBLE FOR TPT'

if b ==0:
    st.write(f'**{statement2}**')
    pass
else:
    st.write(f'**{statement2}**')
    with st.expander(f'**CLICK TO VIEW CLIENTS ON APPT {tm} THAT ARE ELLIGIBLE FOR TPT**'):
        st.write(tpt)

########TPT AFTER TB
cola, colb, colc = st.columns([2,2,1])
colb.write('**TPT AFTER TB**')
st.write('')
df['REINITIATE TPT'] = df['REINITIATE TPT'].astype(str)

tba = df[df['REINITIATE TPT']=='REINITIATE TPT'].copy()

tba = tba[['FACILITY','ART', 'TB', 'TBD','RETURN DATE','REINITIATE TPT']].copy()
tba = tba.set_index('FACILITY')
b = tba.shape[0]

if b == 1:
    statement2 = f'ONE CLIENT ON APPT {tm} FOR TPT AFTER TB'
elif b >1:
    statement2 = f'{b} CLIENTS ON APPT {tm} FOR TPT AFTER TB'
else:
    statement2 = f'NO CLIENT ON APPT {tm} FOR TPT AFTER TB'

if b ==0:
    st.write(f'**{statement2}**')
    pass
else:
    st.write(f'**{statement2}**')
    with st.expander(f'**CLICK TO VIEW CLIENTS ON APPT {tm} FOR TPT AFTER TB**'):
        st.write(tba)
st.divider()

st.write('')

########CERVICAL CANCER
cola, colb, colc = st.columns([2,2,1])
colb.write('**CERVICAL CANCER**')
st.write('')
df['CX_STATUS'] = df['CX_STATUS'].astype(str)

cx = df[df['CX_STATUS']=='SCREEN'].copy()

cx = cx[['FACILITY','GD', 'AG','RETURN DATE','CX']].copy()
cx = cx.set_index('FACILITY')
b = cx.shape[0]

if b == 1:
    statement2 = f'ONE CLIENT ON APPT {tm} IS ELLIGIBLE FOR SCREENING'
elif b >1:
    statement2 = f'{b} CLIENTS ON APPT {tm} ARE ELLIGIBLE FOR SCREENING'
else:
    statement2 = f'NO CLIENT ON APPT {tm} IS ELLIGIBLE FOR SCREENING'

if b ==0:
    st.write(f'**{statement2}**')
    pass
else:
    st.write(f'**{statement2}**')
    with st.expander(f'**CLICK TO VIEW CLIENTS ON APPT {tm} THAT ARE ELLIGIBLE FOR SCREENING**'):
        st.write(cx)

########CERVICAL CANCER RESCREENING
cola, colb, colc = st.columns([2,2,1])
colb.write('**CERVICAL CANCER RESCREENING**')
st.write('')
df['RESCREEN'] = df['RESCREEN'].astype(str)

resc = df[df['CX_STATUS']=='RESCREEN'].copy()

resc = resc[['FACILITY','ART', 'GD', 'AG','RETURN DATE','CX','RESCREEN']].copy()
resc = resc.set_index('FACILITY')
b = resc.shape[0]

if b == 1:
    statement2 = f'ONE CLIENT ON APPT {tm} IS ELLIGIBLE FOR RESCREENING'
elif b >1:
    statement2 = f'{b} CLIENTS ON APPT {tm} ARE ELLIGIBLE FOR RESCREENING'
else:
    statement2 = f'NO CLIENT ON APPT {tm} IS ELLIGIBLE FOR RESCREENING'

if b ==0:
    st.write(f'**{statement2}**')
    pass
else:
    st.write(f'**{statement2}**')
    with st.expander(f'**CLICK TO VIEW CLIENTS ON APPT {tm} THAT ARE ELLIGIBLE FOR RESCREENING**'):
        st.write(resc)

st.divider()

st.write('')

########NON SUPPRESSORS
cola, colb, colc = st.columns([2,2,1])
colb.write('**NON SUPPRESSORS**')
st.write('')
df['SUPPRESSION'] = df['SUPPRESSION'].astype(str)

ns = df[df['SUPPRESSION']=='NS'].copy()

ns = ns[['FACILITY','ART', 'HVL','RETURN DATE']].copy()
ns = ns.set_index('FACILITY')
b = ns.shape[0]

if b == 1:
    statement2 = f'ONE CLIENT ON APPT {tm} IS HLV'
elif b >1:
    statement2 = f'{b} CLIENTS ON APPT {tm} ARE HLVs'
else:
    statement2 = f'NO CLIENT ON APPT {tm} IS HLV'

if b ==0:
    st.write(f'**{statement2}**')
    pass
else:
    st.write(f'**{statement2}**')
    with st.expander(f'**CLICK TO VIEW CLIENTS ON APPT {tm} THAT ARE HLV**'):
        st.write(ns)

st.write('')

########NON SUPPRESSORS
cola, colb, colc = st.columns([2,2,1])
colb.write('**NON SUPPRESSORS FOR REBLEEDING**')
st.write('')
df['SUPPRESSION'] = df['SUPPRESSION'].astype(str)

ns = df[df['SUPPRESSION']=='NS'].copy()

ns = ns[['FACILITY','ART', 'HVL','RETURN DATE']].copy()
ns = ns.set_index('FACILITY')
b = ns.shape[0]

if b == 1:
    statement2 = f'ONE CLIENT ON APPT {tm} IS HLV'
elif b >1:
    statement2 = f'{b} CLIENTS ON APPT {tm} ARE HLVs'
else:
    statement2 = f'NO CLIENT ON APPT {tm} IS HLV'

if b ==0:
    st.write(f'**{statement2}**')
    pass
else:
    st.write(f'**{statement2}**')
    with st.expander(f'**CLICK TO VIEW CLIENTS ON APPT {tm} THAT ARE HLV**'):
        st.write(ns)

st.write('')

########NS TO REBLEED
# cola, colb, colc = st.columns([2,2,1])
# colb.write('**NS TO REBLEED**')
# st.write('')
# df['REBLEED'] = df['REBLEED'].astype(str)

# virb = df[df['REBLEED']=='YES'].copy()

# virb = virb[['FACILITY','ART', 'HVL','RETURN DATE', 'VL DATE', 'REBLEED']].copy()
# vir = virb.set_index('FACILITY')
# b = virb.shape[0]

# if b == 1:
#     statement2 = f'ONE HLV ON APPT {tm} IS DUE FOR REBLEEDING'
# elif b >1:
#     statement2 = f'{b} HLV ON APPT {tm} ARE DUE FOR REBLEEDING'
# else:
#     statement2 = f'NO HLV ON APPT {tm} IS DUE FOR REBLEEDING'

# if b ==0:
#     st.write(f'**{statement2}**')
#     pass
# else:
#     st.write(f'**{statement2}**')
#     with st.expander(f'**CLICK TO VIEW HLVs ON APPT {tm} THAT ARE DUE FOR REBLEEDING**'):
#         st.write(virb)

st.write('')

########LOW LEVEL VIREMIA
cola, colb, colc = st.columns([2,2,1])
colb.write('**LOW LEVEL VIREMIAS**')
st.write('')
df['VIREMIA'] = df['VIREMIA'].astype(str)

vir = df[df['VIREMIA']=='LLV'].copy()

vir = vir[['FACILITY','ART', 'LVL_results','RETURN DATE']].copy()
vir = vir.set_index('FACILITY')
b = vir.shape[0]

if b == 1:
    statement2 = f'ONE CLIENT ON APPT {tm} IS LLV'
elif b >1:
    statement2 = f'{b} CLIENTS ON APPT {tm} ARE LLVs'
else:
    statement2 = f'NO CLIENT ON APPT {tm} IS LLV'

if b ==0:
    st.write(f'**{statement2}**')
    pass
else:
    st.write(f'**{statement2}**')
    with st.expander(f'**CLICK TO VIEW CLIENTS ON APPT {tm} THAT ARE LLV**'):
        st.write(vir)

st.divider()

st.write('')

########NOT ON DTG
cola, colb, colc = st.columns([2,2,1])
colb.write('**CLIENTS NOT ON DTG**')
st.write('')
df['NOT'] = df['NOT'].astype(str)

dtg = df[df['NOT']=='NOT ON DTG'].copy()

dtg = dtg[['FACILITY','ART', 'ARV','RETURN DATE']].copy()
dtg = dtg.set_index('FACILITY')
b = dtg.shape[0]

if b == 1:
    statement2 = f'ONE CLIENT ON APPT {tm} IS NOT ON DTG'
elif b >1:
    statement2 = f'{b} CLIENTS ON APPT {tm} ARE NOT ON DTG'
else:
    statement2 = f'ALL CLIENTS ON APPT {tm} ON DTG'

if b ==0:
    st.write(f'**{statement2}**')
    pass
else:
    st.write(f'**{statement2}**')
    with st.expander(f'**CLICK TO VIEW CLIENTS ON APPT {tm} THAT ARE NOT ON DTG**'):
        st.write(dtg)

st.divider()

st.write('')

########PREGNANT
cola, colb, colc = st.columns([2,2,1])
colb.write('**PMTCT MOTHERS ON APPT**')
st.write('')
df['PT'] = df['PT'].astype(str)

pr = df[df['PT']=='YES'].copy()

pr = pr[['FACILITY','ART','AG', 'PT','RETURN DATE']].copy()
pr = pr.set_index('FACILITY')
b = pr.shape[0]

if b == 1:
    statement2 = f'ONE MOTHER IS ON APPT {tm}'
elif b >1:
    statement2 = f'{b} MOTHERS ARE ON APPT {tm}'
else:
    statement2 = f'NO MOTHER IS ON APPT {tm}'

if b ==0:
    st.write(f'**{statement2}**')
    pass
else:
    st.write(f'**{statement2}**')
    with st.expander(f'**CLICK TO VIEW MOTHERS ON APPT {tm}**'):
        st.write(pr)    
