import streamlit as st
import pandas as pd
import gspread
import numpy as np
import altair as alt

from google.oauth2.service_account import Credentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
]

skey = st.secrets["gcp_service_account"]
credentials = Credentials.from_service_account_info(
    skey,
    scopes=scopes,
)
client = gspread.authorize(credentials)

url = st.secrets["private_gsheets_url"]

# Perform SQL query on the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)

st.title("My Data Tracker")

tab1, tab2, tab3 = st.tabs(["Social Sports", "Flights", "TBD"])

# social sports history

with tab1:
   st.header("My Social Sports History")
   sheet_name="Social Sports"
   sh = client.open_by_url(url)
   df_social = pd.DataFrame(sh.worksheet(sheet_name).get_all_records())

   st.write(df_social)

   df_social_new = df_social.groupby(['Year','Season'])['Sport'].count().reset_index()
   df_social_new['Year'] = df_social_new['Year'].astype(str)

   social_by_season = alt.Chart(df_social_new, title='Social Sports by Year and Season').mark_bar().encode(
     x='Year', y='Sport', color='Season')

   st.altair_chart(social_by_season, use_container_width=True)

   df_social_new2 = df_social.groupby(['Year','Sport'])['Season'].count().reset_index()
   df_social_new2['Year'] = df_social_new2['Year'].astype(str)

   social_by_sport = alt.Chart(df_social_new2, title='Social Sports by Year and Sport').mark_bar().encode(
     x='Year', y='Season', color='Sport')

   st.altair_chart(social_by_sport, use_container_width=True)

# flight history

with tab2:
   st.header("My Flight History")

   sheet_name="Flights"
   sh = client.open_by_url(url)
   df_flights = pd.DataFrame(sh.worksheet(sheet_name).get_all_records())

   st.write(df_flights)