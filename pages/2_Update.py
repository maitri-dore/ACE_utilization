import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import numpy as np
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import random

if 'login_status' not in st.session_state or not st.session_state['login_status']:
    st.session_state['login_status'] = False
    st.write('Please login on the main page.')

if st.session_state['login_status']:

    if 'clicked_see_activities_update' not in st.session_state:
        st.session_state['clicked_see_activities_update'] = False

    def click_see_activities_update():
        st.session_state['clicked_see_activities_update'] = True

    st.title('Update an already registered activity')
    
    cid = st.text_input('Input CID to see your registered activities', help='Input your Chalmers ID.')
    st.button('See registered activities.', on_click=click_see_activities_update)
    
    if st.session_state['clicked_see_activities_update']:
        st.write('Here are registered activities for '+cid+':')
        try:
            conn = st.connection('gsheets', type=GSheetsConnection)
            st.cache_data.clear()
            df = conn.read(worksheet=cid, usecols=range(11))

            if len(df) == 0:
                st.write('None')
            elif len(df) > 0:
                st.dataframe(df[['title', 'category', 'reg_time']])
    
                pa = st.selectbox('Which activitity do you want to revise?', df.index.tolist())
                cols = ['key', 'title', 'CID', 'name', 'division', 'category', 'comment', 'links', 'time_start', 'time_end']
                vals = df.loc[pa, cols].tolist()
    
                st.write('Update form below, then click submit.')
                with st.form('Update_form', clear_on_submit=True):
                    title = st.text_input('Short title', value=vals[1], help='Write a short title of the activity.')
                    cid = st.text_input('CID', value=vals[2], help='Input your Chalmers ID.')
                    name = st.text_input('Your name', value=vals[3], help='Write your name.')
                    divisionlist = ['']+st.session_state['divs']
                    try:
                        ix1 = divisionlist.index(vals[4])
                    except:
                        ix1 = 0
                    division = st.selectbox('Division(s)', divisionlist, index=ix1, help='Choose your division.')
                    catlist = ['']+st.session_state['cats']
                    try:
                        ix2 = catlist.index(vals[5])
                    except:
                        ix2 = 0
                    category = st.selectbox('Type of activity', catlist, index=ix2, help='See definitions and examples on the first page.')
                    thisy = datetime.now().year
                    time = st.slider('Year(s) the activity was done', min_value=thisy-10, max_value=thisy+4, value=vals[-2:])

                    comment = st.text_area('Brief description', value=vals[6], help='Write what you did.')
                    links = st.text_area('Links (if available)', value=vals[7], help='Provide links to webpages or articles.')
                    submit = st.form_submit_button('Submit')

                    randnr = str(random.randint(10,99))
                    now = datetime.now()
                    mo = str(now.month)
                    if len(mo) == 1:
                        mo = '0'+mo
                    da = str(now.day)
                    if len(da) == 1:
                        da = '0'+da
                    ts = str(now.year)+'-'+mo+'-'+da+'-'+str(now.hour)+'-'+str(now.minute)
                    key = cid + '__' + ts + '__' + randnr

                    if submit:
                        df.loc[pa] = [key, cid, name, category, division, title, comment, links, time[0], time[-1], ts]
                        conn.update(worksheet=cid, data=df)

        except:
            st.write('Cannot read from the database right now, try reloading the page.')