import streamlit_authenticator as stauth
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time
from datetime import datetime

#emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title='Utilization at ACE', page_icon=':boomerang:', layout='centered')
st.title('Welcome to the utilization database of ACE!')

conn = st.connection('gsheets', type=GSheetsConnection)

users = conn.read(worksheet='login', usecols=[0, 1, 2])
usernames = users['user'].tolist()
names = users['username'].tolist()
passwords = users['password'].tolist()

credentials = {'usernames':{}}
for i in range(len(usernames)):
    credentials['usernames'][usernames[i]] = {'name':names[i], 'password':passwords[i]}

authenticator = stauth.Authenticate(credentials, 'ACE utilization', 'abcdef', cookie_expiry_days=0)

name, authentication_status, username = authenticator.login('main')

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
st.session_state['headings'] = ['key', 'CID', 'name', 'category', 'division', 
                                  'title', 'comment', 'links', 
                                  'time_start', 'time_end', 'reg_time']

# #Run app VP login
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
        st.cache_data.clear()
        df = conn.read(worksheet='summary', usecols=range(6))
        df = df.groupby('key').first()
        df = df.reset_index()
        st.dataframe(df)
        cidlist = df['CID'].unique()

        update = st.button('Update')
        if update:
            summary = [['key', 'CID', 'name', 'category', 'division', 'year']]
            for c in cidlist:
                time.sleep(2)
                dfc = conn.read(worksheet=c, usecols=range(11))
                for ix in dfc.index:
                    time_start = dfc.loc[ix, 'time_start']
                    time_end = dfc.loc[ix, 'time_end']
                    for y in range(time_start, time_end+1):
                        summary.append(dfc.loc[ix, ['key', 'CID', 'name', 'category', 'division']].tolist()+[y])
            summary = pd.DataFrame(summary[1:], columns=summary[0])
            conn.update(worksheet='summary', data=summary)
            print(summary.head())

        download = st.button('Download')
        if download:
            dflist = []
            for c in cidlist:
                time.sleep(2)
                dfc = conn.read(worksheet=c, usecols=range(11))
                dflist.append(dfc)
            dfout = pd.concat(dflist, axis=0, ignore_index=True)
            st.dataframe(dfout)

            @st.cache_data
            def convert_df(df0):
                return df0.to_csv(sep='\t').encode('utf-8')

            tsv = convert_df(dfout)
            now = datetime.now()
            ts = str(now.year)+'_'+str(now.month)+'_'+str(now.day)+'_'+str(now.hour)+'_'+str(now.minute)
            st.download_button('Press to download database', data=tsv, file_name='UtilDB_'+ts+'.txt')

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
    
