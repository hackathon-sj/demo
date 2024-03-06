import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
from snowflake.snowpark import Session
from st_pages import add_page_title

#add_page_title(layout="small")
#add_page_title()

# Establish Snowflake session
st.cache_data.clear()
st.cache_resource.clear()

st.header(':jeans: **Part One-Forecasting demand for Men\'s apparel**')

#st.title('Sales Forecast Visualization Application')

def create_session():
    return Session.builder.configs(st.secrets["snowflake"]).create()

session = create_session()

st.divider()

c1, c2 = st.columns([1,2])
with c1:
 st.info('**💡 **Team Data Maverick**💡**')




def make_heatmap ():
    
 # Assuming 'df' is a pandas DataFrame with 'TIMESTAMP', 'UNITS_SOLD', and 'FORECAST' columns
    df = session.sql("SELECT timestamp, units_sold, NULL AS forecast FROM ADIDAS.PUBLIC.Mens_Apparel_sales UNION SELECT TS AS timestamp, NULL AS units_sold, forecast FROM ADIDAS.PUBLIC.sales_predictions ORDER BY timestamp asc").to_pandas()

    # Convert TIMESTAMP from string to datetime if not already
    #df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])

    # Creating line charts for Units Sold and Forecast
    line_units_sold = alt.Chart(df).mark_line(color='blue', size=2).encode(
        x='TIMESTAMP:T',
        y='UNITS_SOLD:Q',
        tooltip=['TIMESTAMP', 'UNITS_SOLD']
    ).properties(
        title='Units Sold'
    )

    line_forecast = alt.Chart(df).mark_line(color='yellow', size=2).encode(
        x='TIMESTAMP:T',
        y='FORECAST:Q',
        tooltip=['TIMESTAMP', 'FORECAST']
    ).properties(
        title='Forecast'
    )

    # Combine the charts
    chart = alt.layer(line_units_sold, line_forecast).resolve_scale(
        y='independent'
    ).properties(
        title='Units Sold for Mens Apparel- Forecast Visualization',
        width='container',
        height=300  # You can adjust the height as needed
    )

    return chart





#with st.expander("Expand this area to explore **first** part",expanded=False):
#st.markdown("""
#- First part will generate forecasting model for units sold for only one product- **Men's Apparel**.
#- Since we have sales dataset till 31-Jan-2024,it will generate predictions for units sold for the number of days selected by user.
#- Finally we will generate visualizations in the form of line chart.
#""")
st.write('✏️ **Step 1:- Create Forecasting model for units sold for product -Men\'s Apparel**')
if 'button_clicked1' not in st.session_state:
    st.session_state.button_clicked1 = False
if st.button("Create Forecasting Model!"):
    st.session_state.button_clicked1=True
    session.sql("CREATE OR REPLACE forecast ADIDAS.PUBLIC.sales_forecast (INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'ADIDAS.PUBLIC.Mens_Apparel_sales'),TIMESTAMP_COLNAME => 'TIMESTAMP',TARGET_COLNAME => 'UNITS_SOLD');").collect()
if st.session_state.button_clicked1:
    st.success("Forecasting Model created successfully !")

#st.columns((1.5, 4.5, 2), gap='medium')
Days = st.selectbox(
     '**:red[Select Forecasting Period in days]**',
     ('30', '60', '90'),help="it helps")

st.write('Selected days:', Days)

st.write('✏️ **Step 2:- Create Predictions for units sold for the number of days selected by user**')
if 'button_clicked2' not in st.session_state:
    st.session_state.button_clicked2 = False
if st.button("Create Predictions!"):
    st.session_state.button_clicked2=True
    session.sql("CALL ADIDAS.PUBLIC.sales_forecast!FORECAST(FORECASTING_PERIODS =>"+Days+");").collect()
    session.sql("CREATE OR REPLACE TABLE ADIDAS.PUBLIC.sales_predictions AS (SELECT * FROM TABLE(RESULT_SCAN(-1)));").collect()
if st.session_state.button_clicked2:
    st.success("Predictions created successfully !")

st.write('✏️ **Step 3:- Create Visualization**')
if 'button_clicked3' not in st.session_state:
    st.session_state.button_clicked3 = False
if st.button("View Line Chart !"):
    st.session_state.button_clicked3=True

   # st.write(":heavy_minus_sign:" * 29) 


#col = st.columns((1.5, 4.5, 2), gap='medium')
#col1,col2 = st.columns([2.5,2])

#with col1:
# with st.expander("Expand this area to visualize line chart for **first** part"):
#with st.container():
#st.markdown('#### Visualization 1')
st.write(":heavy_minus_sign:" * 29)     
 
heatmap_chart = make_heatmap()
if st.session_state.button_clicked3:
    st.altair_chart(heatmap_chart, use_container_width=True)
    st.success("Visualization created")




st.divider()

c1, c2, c3 = st.columns(3)
with c1:
    st.info('**💡 **Team Data Maverick**💡**')