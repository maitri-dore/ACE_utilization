import streamlit as st
import pandas as pd
import numpy as np
import database_activities as dba

if 'login_status' not in st.session_state or not st.session_state['login_status']:
    st.session_state['login_status'] = False
    st.write('Please login on the main page.')

if st.session_state['login_status']:

    if 'clicked_see_activities_del' not in st.session_state:
        st.session_state['clicked_see_activities_del'] = False

    def click_see_activities_del():
        st.session_state['clicked_see_activities_del'] = True

    st.title('Delete a previously registered activity.')
    
    cid = st.text_input('Input CID to see your registered activities', help='Input your Chalmers ID.')
    st.button('See registered activities.', on_click=click_see_activities_del)
    
    if st.session_state['clicked_see_activities_del']:
        st.write('Here are registered activities for '+cid+':')
        res = dba.fetch_cid(cid)
        if len(res) > 0:
            df = pd.DataFrame.from_dict(res, orient='columns')
            df['index'] = np.arange(len(df))+1
            df.set_index('index', inplace=True)
            st.dataframe(df[['title', 'reg_time']])

            pa = st.selectbox('Which activitity do you want to delete?', df.index.tolist())
            key = df.loc[pa, 'key']

            delete = st.button('Delete')
            if delete:
                dba.delete_key(key)

        else:
            st.write('None')
