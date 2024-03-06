from pathlib import Path

import streamlit as st

#with st.echo("below"):
from st_pages import Page, add_page_title, show_pages

st.set_page_config(
    #page_title="Ex-stream-ly Cool App",
    #page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.divider()

c1, c2 = st.columns([1,2])
with c1:
 st.info('**💡 **Team Data Maverick**💡**')

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




show_pages(
    [
        Page("example_app/st-home.py", "Home", "🏠"),
            # Can use :<icon-name>: or the actual icon
        Page("example_app/st-partone.py", "Part One", ":jeans:"),
            # The pages appear in the order you pass them
        Page("example_app/st-parttwo.py", "Part Two", ":shoe:"),
        #Page("example_app/st-partone.py", "Part Three", ":line-chart:"),
        #Page("example_app/st-partone.py", "Part One", ":jeans:"),
            #Page("example_app/example_two.py", "Example Two", "✏️"),
            # Will use the default icon and name based on the filename if you don't
            # pass them
            #Page("example_app/example_three.py"),
            #Page("example_app/example_five.py", "Example Five", "🧰"),
    ]
)

add_page_title()  # Optional method to add title and icon to current page

st.divider()

c1, c2 = st.columns([1,2])
with c1:
 st.info('**💡 **Team Data Maverick**💡**')