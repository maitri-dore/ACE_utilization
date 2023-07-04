import os
from deta import Deta
import streamlit as st
from datetime import datetime

DETA_KEY = st.secrets['DETA_KEY']

deta = Deta(DETA_KEY)

db = deta.Base('ACE_util_db')

def insert_activity(title, CID, name, division, category, time, comment, links):
    now = datetime.now()
    xlist = []
    for x in [str(now.month), str(now.day), str(now.hour), str(now.minute)]:
        if len(x) == 2:
            xlist.append(x)
        else:
            xlist.append('0'+x)
    reg_time = str(now.year)+'-'+xlist[0]+'-'+xlist[1]+' '+xlist[2]+':'+xlist[3]
    key = CID + '...' + str(title)  + '...' + reg_time
    return db.put({'key':key, 'reg_time':reg_time, 'title':title, 'CID':CID, 'name':name, 'division':division, 'category':category, 'time':time, 'comment':comment, 'links':links})

def fetch_all():
    res = db.fetch()
    return res.items

def fetch_cid(cid):
    res = db.fetch({'CID':cid})
    return res.items

def delete_key(key):
    return db.delete(key)

