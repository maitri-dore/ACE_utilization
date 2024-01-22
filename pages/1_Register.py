import streamlit as st
from datetime import datetime


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

        thisy = datetime.now().year
        time = st.slider('Year(s) the activity was done', min_value=thisy-10, max_value=thisy+4, value=[thisy-1,thisy])
        if time[0] == time[1]:
            time = [time[0]]
        else:
            time = list(range(time[0], time[1]+1))

        comment = st.text_area('Brief description of the activity', help='Write what you did.')
    
        links = st.text_area('Links (if available)', help='Provide links to webpages or articles.')

        submit = st.form_submit_button('Submit')
        if submit:
            dba.insert_activity(title, cid, name, division, category, time, comment, links)

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

