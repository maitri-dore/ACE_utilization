import streamlit as st
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta


if 'login_status' not in st.session_state or not st.session_state['login_status']:
    st.session_state['login_status'] = False
    st.write('Please login on the main page.')

if st.session_state['login_status']:
    import database_activities as dba

    st.title('Register a utilization activity')
    st.markdown('Fill out the fields below.')
    
    with st.form('Reg_form', clear_on_submit=True):
    
        title = st.text_input('Short title', help='Write a short title of the activity.')
        cid = st.text_input('CID', help='Input your Chalmers ID.')
        name = st.text_input('Your name', help='Write your name.')
    
        divisionlist = ['']+st.session_state['divs']
        division = st.selectbox('Division', divisionlist, help='Choose your division.')
    
        catlist = ['']+st.session_state['cats']
        category = st.selectbox('Type of activity', catlist, help='See definitions and examples on the first page.')

        end_t = datetime.now().year+3
        time = st.slider('Year(s) the activity was done', min_value=2015, max_value=end_t, value=[end_t-4,end_t-3])
        if time[0] == time[1]:
            time = str(time[0])
        else:
            time = str(time[0])+'-'+str(time[1])

        comment = st.text_area('Brief description of the activity', help='Write what you did.')
    
        links = st.text_area('Links (if available)', help='Provide links to webpages or articles.')

        submit = st.form_submit_button('Submit')
        if submit:
            dba.insert_activity(title, cid, name, division, category, time, comment, links)

