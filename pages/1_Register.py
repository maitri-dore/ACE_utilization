import streamlit as st
import streamlit_authenticator as stauth
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import random
import pandas as pd

if 'login_status' not in st.session_state or not st.session_state['login_status']:
    st.session_state['login_status'] = False
    st.write('Please login on the main page.')

if st.session_state['login_status']:

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

        thisy = datetime.now().year
        time = st.slider('Year(s) the activity was done', min_value=thisy-10, max_value=thisy+4, value=[thisy-1,thisy])
        time_start = time[0]
        time_end = time[1]

        comment = st.text_area('Brief description of the activity', help='Write what you did.')
    
        links = st.text_area('Links (if available)', help='Provide links to webpages or articles.')

        submit = st.form_submit_button('Submit')
        if submit:
            st.cache_data.clear()
            conn = st.connection('gsheets', type=GSheetsConnection)
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

            try:
                df = conn.read(worksheet=cid, usecols=range(11))
                df = df.set_index('key')
                df.loc[key] = [cid, name, category, division, title, comment, links, time_start, time_end, ts]
                df = df.reset_index()
                conn.update(worksheet=cid, data=df)
            except:
                df = pd.DataFrame([[key, cid, name, category, division, title, comment, links, time_start, time_end, ts]], columns=st.session_state['headings'])
                conn.create(worksheet=cid, data=df)
                dfsum = conn.read(worksheet='summary', usecols=range(6))
                for y in range(time_start, time_end+1):
                    dfsum.loc[len(dfsum.index)] = [key, cid, name, category, division, y]
                conn.update(worksheet='summary', data=dfsum)

    st.subheader('We categorize utilization activities as follows:')
    st.markdown("""
                - **Research collaboration**. For example, you collaborate with actors from industry or other societal sectors in a research project.
                - **Competence development**. For example, you provide a course to people from the industry or support people's competence development in some other way. (Note this does not include our regular education of Chalmers students)
                - **Technical services**. For example, you provide expert services such as laboratory analyses for people outside of the university.
                - **Design and development**. For example, you contribute to the development of an urban area.
                - **Commercialization and startups**. For example, you startup a company based on your innovation.
                - **Expert advise**. For example, you provide advise to the government, contribute to international reports such as IPCC, contribute to development of new industry standards, etc.
                - **Information dissemination**. For example, you participate in the public debate, present your research to the public, or give a presentation targeting a specific societal sector.
                - **Engagement in networks**. You are part of a network or organization that brings together different researchers and, possibly, stakeholders from society.
                - **Other**. This is for utilization activities that you don't think fit into the categories above.
                """)

