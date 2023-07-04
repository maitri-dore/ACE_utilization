import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
import plotly.express as px

import database_activities as dba

if 'login_status' not in st.session_state or not st.session_state['login_status']:
    st.session_state['login_status'] = False
    st.write('Please login on the main page.')

if st.session_state['login_status']:

    st.title('Statistics on the ACE utilization database.')

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
            df['first_yr'] = df['time']
            df.loc[df['time'].str.contains('-'), 'first_yr'] = df.loc[df['time'].str.contains('-'), 'time'].str.split('-').str[0]
            df['first_yr'] = df['first_yr'].apply(int)
            df['end_yr'] = df['time']
            df.loc[df['time'].str.contains('-'), 'end_yr'] = df.loc[df['time'].str.contains('-'), 'time'].str.split('-').str[1]
            df['end_yr'] = df['end_yr'].apply(int) + 1
            
            yrlist = []
            catlist = []
            divlist = []
            for i in df.index:
                years = list(range(df.loc[i, 'first_yr'], df.loc[i, 'end_yr']))
                cats = [df.loc[i, 'category']]*len(years)
                divs = [df.loc[i, 'division']]*len(years)
                yrlist = yrlist + years
                catlist = catlist + cats
                divlist = divlist + divs
            dfp = pd.DataFrame({'Year':yrlist, 'Category':catlist, 'Count':divlist})
            dfp.loc[~dfp['Category'].isin(st.session_state['cats']), 'Category'] = 'Unknown'
            dfp.loc[~dfp['Count'].isin(st.session_state['divs']), 'Count'] = 'Unknown'
            dfp['cy'] = dfp['Category']+dfp['Year'].astype(str)
            
            dfp1 = dfp[['Count', 'cy']].groupby('cy').count()
            dfp1[['Year', 'Category']] = dfp[['Year', 'Category', 'cy']].groupby('cy').first()[['Year', 'Category']]
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
