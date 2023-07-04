import streamlit as st
import pandas as pd
import numpy as np
import database_activities as dba

if 'login_status' not in st.session_state or not st.session_state['login_status']:
    st.session_state['login_status'] = False
    st.write('Please login on the main page.')

if st.session_state['login_status']:
    @st.cache_data
    def convert_df(df0):
        return df0.to_csv(sep='\t').encode('latin1')
    
    st.title('Download all your activities.')
    cid = st.text_input('Input CID and press enter. Then press the Download button.', help='Input your Chalmers ID.')
    res = dba.fetch_cid(cid)
    if len(res) > 0:
        df = pd.DataFrame.from_dict(res, orient='columns')
        df['index'] = np.arange(len(df))+1
        df.set_index('index', inplace=True)
        cols = ['title', 'CID', 'name', 'division', 'category', 'time', 'comment', 'links', 'reg_time']
        tsv = convert_df(df[cols])
        st.download_button('Download', data=tsv, file_name=cid+'_utilization_data.txt')


