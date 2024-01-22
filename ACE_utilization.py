import streamlit_authenticator as stauth
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import io
from datetime import datetime

import database_users as dbu
import database_activities as dba

#emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title='Utilization at ACE', page_icon=':boomerang:', layout='centered')
st.title('Welcome to the utilization database of ACE!')

# User authentication
users = dbu.fetch_all_users()

usernames = [user['key'] for user in users]
names = [user['name'] for user in users]
hashed_passwords = [user['password'] for user in users]

credentials = {'usernames':{}}
for i in range(len(usernames)):
    credentials['usernames'][usernames[i]] = {'name':names[i], 'password':hashed_passwords[i]}

authenticator = stauth.Authenticate(credentials, 'ACE utilization', 'abcdef', cookie_expiry_days=0)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == False:
    st.error('Username or password is incorrect')
if authentication_status == None:
    st.error('Please input username and password')

st.session_state['login_status'] = authentication_status


#Lists used throughout session
st.session_state['divs'] = ['Applied Acoustics', 'Architectural Theory and Methods', 'Building Design',
                'Building Services Engineering', 'Building Technology', 'Construction Management',
                'Geology and Geotechnics', 'Structural Engineering', 
                'Urban Design and Planning', 'Water Environment Technology']
st.session_state['cats'] = ['Research collaboration', 'Competence development', 'Technical services', 'Design and development',
                'Commercialization and startups', 'Expert advise', 'Information dissemination', 'Engagement in networks', 'Other']

#Run app VP login
if authentication_status and username == 'admin':
    st.markdown('Welcome admin')
    authenticator.logout('Logout', 'sidebar')
    
    if 'clicked_see_activities_admin' not in st.session_state:
        st.session_state['clicked_see_activities_admin'] = False

    def click_see_activities_admin():
        st.session_state['clicked_see_activities_admin'] = True

    st.button('See registered activities.', on_click=click_see_activities_admin)
    
    if st.session_state['clicked_see_activities_admin']:
        st.write('Here are all registered activities')
        try:
            res = dba.fetch_all()
            if len(res) > 0:
                df = pd.DataFrame.from_dict(res, orient='columns')
                df['index'] = np.arange(len(df))+1
                df.set_index('index', inplace=True)
                cols = ['reg_time', 'CID', 'title', 'name', 'division', 'category', 'time', 'comment', 'links', 'key']
                st.dataframe(df[cols])
    
                pa = st.multiselect('Which activitity do you want to delete?', df.index.tolist())
                keys = df.loc[pa, 'key'].tolist()
    
                delete = st.button('Delete')
                if delete:
                    for k in keys:
                        dba.delete_key(k)
    
                @st.cache_data
                def convert_res2pkl(df0):
                    f = io.BytesIO()
                    pickle.dump(df0, f)
                    return f
    
                st.subheader('Download database')
                pkl = convert_res2pkl(res)
                now = datetime.now()
                ts = str(now.year)+'_'+str(now.month)+'_'+str(now.day)+'_'+str(now.hour)+'_'+str(now.minute)
                st.download_button('Download database', data=pkl, file_name='UtilDB_'+ts+'.pickle')
            else:
                st.write('None')
        except:
            st.write('Cannot load database right now, try reloading the page.')

#Run app normal login
elif authentication_status:
    st.markdown('Here you can:')
    st.markdown('- **Register** a utilization activity')
    st.markdown('- **Update** information about a previously registered activity')
    st.markdown('- **Delete** a previously registered entry')
    st.markdown('- **Download** a table with your utilization activities')
    st.markdown('- **View** statistics for ACE')
    st.markdown('Choose what you want to do in the sidebar menu.')

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
    
    authenticator.logout('Logout', 'sidebar')
    