import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import database_activities as dba

if 'login_status' not in st.session_state or not st.session_state['login_status']:
    st.session_state['login_status'] = False
    st.write('Please login on the main page.')

if st.session_state['login_status']:

    if 'clicked_see_activities_update' not in st.session_state:
        st.session_state['clicked_see_activities_update'] = False

    def click_see_activities_update():
        st.session_state['clicked_see_activities_update'] = True

    st.title('Update an already registered activity.')
    
    cid = st.text_input('Input CID to see your registered activities', help='Input your Chalmers ID.')
    st.button('See registered activities.', on_click=click_see_activities_update)
    
    if st.session_state['clicked_see_activities_update']:
        st.write('Here are registered activities for '+cid+':')
        res = dba.fetch_cid(cid)
        if len(res) == 0:
            st.write('None')
        elif len(res) > 0:
            df = pd.DataFrame.from_dict(res, orient='columns')
            df['index'] = np.arange(len(df))+1
            df.set_index('index', inplace=True)
            st.dataframe(df[['title', 'reg_time']])

            pa = st.selectbox('Which activitity do you want to revise?', df.index.tolist())
            cols = ['key', 'title', 'CID', 'name', 'division', 'category', 'comment', 'links', 'time']
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
                end_t = datetime.now().year+3
                if '-' in vals[-1]:
                    values = [int(vals[-1].split('-')[0]),int(vals[-1].split('-')[1])]
                else:
                    values = [int(vals[-1]), int(vals[-1])]
                time = st.slider('Year(s) the activity was done', min_value=2015, max_value=end_t, value=values)
                if time[0] == time[1]:
                    time = str(time[0])
                else:
                    time = str(time[0])+'-'+str(time[1])
                comment = st.text_area('Brief description', value=vals[6], help='Write what you did.')
                links = st.text_area('Links (if available)', value=vals[7], help='Provide links to webpages or articles.')
                submit = st.form_submit_button('Submit')
                if submit:
                    dba.delete_key(vals[0])
                    dba.insert_activity(title, cid, name, division, category, time, comment, links)
