# streamlit_pydeck_demo.py

import streamlit as st
import pandas as pd
import pydeck as pdk
import math

# Function to load data
@st.cache_data
def load_data():
    df = pd.read_csv("RainDaily_Tabular.csv")
    return df

df = load_data()

province = st.sidebar.selectbox(
    'Province', df['province'].unique(), index=None
)
date = st.sidebar.selectbox(
    'Date',df['date'].unique(), index=None
)

if province:
    province_df = df[df['province'] == province]
else :
    province_df = df

if date:
    date_df = province_df[province_df['date']==date]
else :
    date_df = province_df



# Main app
st.title('PyDeck Demo')

# Function to create map
def create_map(dataframe):
    layer = pdk.Layer(
            "HeatmapLayer",
            dataframe,
            get_position=["longitude", "latitude"],
            get_weight="rain",  
            opacity=0.5,
            pickable=True
    )

    view_state = pdk.ViewState(
        longitude=dataframe['longitude'].mean(),
        latitude=dataframe['latitude'].mean(),
        zoom=9
    )

    return pdk.Deck(layers=[layer], initial_view_state=view_state, map_style="mapbox://styles/mapbox/light-v11", tooltip={"text": "{name}\n{address}"})


# Display Map
st.write('### Map')
map = create_map(date_df)
st.pydeck_chart(map)

# Display data
st.dataframe(date_df)

st.line_chart(date_df.pivot_table(
    index='date', columns='province', values='rain'))

st.bar_chart(date_df.groupby(
    'province')['rain'].sum().reset_index().set_index('province'))

with open("./assignment11.py", "r") as f:
    code = f.read()
st.code(code, language="python")

max_rain_date = date_df.groupby('date')['rain'].sum().idxmax()
top_province = date_df.groupby('province')['rain'].sum().idxmax()

st.text("Date with highest total rain: "+str(max_rain_date))
st.text('Province with highest rain: '+str(top_province))
st.write('')