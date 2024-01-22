import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import plotly.express as px
import database_activities as dba


st.title('Statistics on the ACE utilization database')
try:
    res = dba.fetch_all()
    if len(res) == 0:
        st.write('There are no entries in the database.')
    else:
        df = pd.DataFrame.from_dict(res, orient='columns')
        df['date'] = df['reg_time'].str.split(' ').str[0]
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    
        st.write('There are '+str(len(df))+' entries in the database.')
        st.markdown('- '+str(len(df['CID'].unique()))+' people have made entries.')
        st.markdown('- '+str(len(df.loc[df['division'].notna(), 'division'].unique()))+' divisions are represented.')
        st.markdown('- '+str(len(df['category'].unique()))+' utilization categories are included.')
    
        cont1 = st.container()
        with cont1:
            st.subheader('When were items entered into the database?')
            start = datetime(2023, 6, 1)
            now = datetime.now()
            mo_diff = relativedelta(now, start).months + 12*relativedelta(now, start).years
            if relativedelta(now, start).days > 0:
                mo_diff += 1
            dfp = pd.DataFrame(pd.NA, index=range(mo_diff), columns=['Month', 'New entries'])
            for i in range(mo_diff):
                this_month = start + relativedelta(months=i)
                dfp.loc[i, 'Month'] = this_month
                antal = len(df[(df['date']>=this_month)&(df['date']<this_month+relativedelta(months=1))].index)
                dfp.loc[i, 'New entries'] = antal
    
            fig = px.bar(dfp, x='Month', y='New entries')
            fig.update_layout(xaxis_tickformat = '%b %Y')
            fig.update_xaxes(nticks = len(dfp))
            st.plotly_chart(fig)
    
        cont2 = st.container()
        with cont2:
            st.subheader('When were the activities carried out?')
            dfp = df.explode('time')
            dfp.loc[~dfp['category'].isin(st.session_state['cats']), 'category'] = 'Unknown'
            dfp.loc[~dfp['division'].isin(st.session_state['divs']), 'division'] = 'Unknown'
            dfp['cy'] = dfp['category']+dfp['time'].astype(str)
            dfp1 = dfp[['cy', 'division']].groupby('cy').count()
            dfp1.columns = ['Count']
            dfp1[['Year', 'Category']] = dfp[['time', 'category', 'cy']].groupby('cy').first()
            fig = px.bar(dfp1, x='Year', y='Count', color='Category')
            st.plotly_chart(fig)
        
        cont3 = st.container()
        with cont3:
            st.subheader('In which divisions were the activities carried out?')
            dfp = df[['division', 'category', 'CID']].copy()
            dfp.loc[~dfp['category'].isin(st.session_state['cats']), 'category'] = 'Unknown'
            dfp.loc[~dfp['division'].isin(st.session_state['divs']), 'division'] = 'Unknown'
            dfp['dc'] = dfp['division'] + dfp['category']
            dfp2 = dfp.groupby('dc').count()
            dfp2[['division', 'category']] = dfp[['division', 'category', 'dc']].groupby('dc').first()
            dfp2[['Count', 'Division', 'Category']] = dfp2[['CID', 'division', 'category']]
            fig = px.bar(dfp2, x='Division', y='Count', color='Category')
            st.plotly_chart(fig)

except:
    st.write('Cannot load database right now, try reloading the page.')
