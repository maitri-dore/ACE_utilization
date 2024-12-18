import streamlit as st
from streamlit_gsheets import GSheetsConnection

if 'login_status' not in st.session_state or not st.session_state['login_status']:
    st.session_state['login_status'] = False
    st.write('Please login on the main page.')

if st.session_state['login_status']:

    if 'clicked_see_activities_del' not in st.session_state:
        st.session_state['clicked_see_activities_del'] = False

    def click_see_activities_del():
        st.session_state['clicked_see_activities_del'] = True

    st.title('Delete a previously registered activity')
    
    cid = st.text_input('Input CID to see your registered activities', help='Input your Chalmers ID.')
    st.button('See registered activities.', on_click=click_see_activities_del)

    if st.session_state['clicked_see_activities_del']:
        st.write('Here are registered activities for '+cid+':')
        st.cache_data.clear()
        try:
            conn = st.connection('gsheets', type=GSheetsConnection)
            df = conn.read(worksheet=cid, usecols=range(11), ttl=2)
    
            if len(df) == 0:
                st.write('None')
            elif len(df) > 0:
                st.dataframe(df[['title', 'category', 'reg_time']])

                pa = st.selectbox('Which activitity do you want to delete?', df.index.tolist())
                key = df.loc[pa, 'key']
    
                delete = st.button('Delete')
                if delete:
                    data1 = conn.read(worksheet='summary', ttl=5)
                    data1 = data1[data1['key']!=key]
                    data1 = data1.reset_index(drop=True)
                    conn.update(worksheet='summary', data=data1)

                    data2 = conn.read(worksheet=cid, ttl=5)
                    data2 = data2[data2['key']!=key]
                    data2 = data2.reset_index(drop=True)
                    conn.update(worksheet=cid, data=data2)
            else:
                st.write('None')

        except:
            st.write('Cannot read from the database right now, try reloading the page.')

