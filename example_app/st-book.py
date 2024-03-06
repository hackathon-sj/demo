import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
from snowflake.snowpark import Session
from pathlib import Path
import streamlit_book as stb



#with st.echo("below"):
from st_pages import Page, add_page_title, show_pages

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
   - 1. Choose a dataset of your choice (ex: Sales), load the data in Snowflake
   - 2. Create a model to forecast the demand (ex: for Products or Items)
   - 3. Augment additional data like Holiday, Weather etc and see if this improves the model.
   - 4. Perform trend analysis & identify anomalies
   - 5. Develop a Snowflake Streamlit App to showcase the workflow (inputs, process, output).
    
    **Over & Beyond**
   - 1. Async model retraining using Snowflake Tasks powered by Notifications via Email
   - 2. E2E Solution & Architecture Diagram (hand-drawn is fine too)
   - 3. Integrate with NLP to SQL

""")
st.divider()

st.title('Sales Forecast Visualization Application')

#show_pages(
#    [
#        Page("example_app/st-home.py", "Home", "🏠"),
#            # Can use :<icon-name>: or the actual icon
#        Page("example_app/st-partone.py", "Part One", ":jeans:"),
#            # The pages appear in the order you pass them
#        Page("example_app/st-parttwo.py", "Part Two", ":shoe:"),
#        Page("example_app/st-partthree.py", "Part Three", ":dollar:"),
#        #Page("example_app/st-partone.py", "Part One", ":jeans:"),
#            #Page("example_app/example_two.py", "Example Two", "✏️"),
#            # Will use the default icon and name based on the filename if you don't
#            # pass them
#            #Page("example_app/example_three.py"),
#            #Page("example_app/example_five.py", "Example Five", "🧰"),
#    ]
#)



stb.set_book_config(
                            menu_title="Book",
                            menu_icon="lightbulb",
                            options=[
                                   "Home",
                                   "Part One"
                                   ], 
                            paths=[
                                   "example_app/", 
                                   "example_app"
                                   ],
                            icons=[
                                   "",
                                   "paint-bucket"
                                   ],
                            )

#add_page_title()  # Optional method to add title and icon to current page

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

