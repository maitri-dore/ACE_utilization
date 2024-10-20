import streamlit as st
from streamlit_gsheets import GSheetsConnection
import numpy as np

if 'login_status' not in st.session_state or not st.session_state['login_status']:
    st.session_state['login_status'] = False
    st.write('Please login on the main page.')

if st.session_state['login_status']:
    @st.cache_data
    def convert_df(df0):
        return df0.to_csv(sep='\t').encode('latin1')
    
    st.title('Download all your activities')
    cid = st.text_input('Input CID and press enter. Then press the Download button.', help='Input your Chalmers ID.')

    try:
        conn = st.connection('gsheets', type=GSheetsConnection)
        df = conn.read(worksheet=cid, usecols=range(11))

        if len(df) == 0:
            st.write('None')
        elif len(df) > 0:
            st.dataframe(df[['title', 'category', 'reg_time']])

        if len(df) > 0:
            df['index'] = np.arange(len(df))+1
            df.set_index('index', inplace=True)
            cols = ['title', 'CID', 'name', 'division', 'category', 'time_start', 'time_end', 'comment', 'links', 'reg_time']
            tsv = convert_df(df[cols])
            st.download_button('Download', data=tsv, file_name=cid+'_utilization_data.txt')

        else:
            st.write('Nothing is registered for this CID')

    except:
        st.write('Cannot read from the database right now, try reloading the page.')


