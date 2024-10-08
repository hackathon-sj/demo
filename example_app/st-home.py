import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
from snowflake.snowpark import Session
from pathlib import Path
import importlib.util
import os


# Establish Snowflake session



st.cache_data.clear()
st.cache_resource.clear()

st.divider()

c1, c2 = st.columns([1,2])
with c1:
 st.info('**💡 **Team Data Maverick**💡**')



def create_session():
    return Session.builder.configs(st.secrets["snowflake"]).create()

session = create_session()


 
 #st.info('**💡 Team Data Maverick 💡**', icon="💡")

    #"## Declaring the pages in your app:"
st.markdown("""
    **Problem Statement 1: Prediction & Anomaly Detection in Snowflake (Cortex)**

    **Ask**
   -  Choose a dataset of your choice (ex: Sales), load the data in Snowflake
   -  Create a model to forecast the demand (ex: for Products or Items)
   -  Augment additional data like Holiday, Weather etc and see if this improves the model.
   -  Perform trend analysis & identify anomalies
   -  Develop a Snowflake Streamlit App to showcase the workflow (inputs, process, output).
    
    **Over & Beyond**
   -  Async model retraining using Snowflake Tasks powered by Notifications via Email
   -  E2E Solution & Architecture Diagram (hand-drawn is fine too)
   -  Integrate with NLP to SQL

""")
st.divider()

st.title('Sales Forecast Visualization Application')



st.markdown("""
This app will build **forecast model** adding holiday information & generate predictions for units sold, total sales & operating profit.
- Below is a sample Adidas sales dataset for the last 2 years consist of below products sold across **NYC** **:sun_with_face:**
    - **Men's Street Footwear**
    - **Men's Athletic Footwear**
    - **Men's Apparel**
* **Python libraries:** pandas, streamlit, matplotlib, altair
""")



def load_data(table_name):
    st.write(f"Here's some example data from `{table_name}`:")
    table = session.table(table_name)
    table = table.limit(20)
    table = table.collect()
    return table

table_name = "ADIDAS.PUBLIC.SALES_DATA"

col1,col2 = st.columns([2,1])

with col1:
 with st.expander("View and Download data"):
    df = load_data(table_name)
    st.dataframe(df)

st.divider()

c1, c2, c3 = st.columns(3)
with c1:
    st.info('**💡 **Team Data Maverick**💡**')