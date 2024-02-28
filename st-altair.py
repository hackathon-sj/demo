
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import pandas as pd
from snowflake.snowpark import Session

# Establish Snowflake session
@st.cache_resource
def create_session():
    return Session.builder.configs(st.secrets.snowflake).create()

session = create_session()
#st.success("Connected to Snowflake!")

st.title('Sales Forecast Visualization Application')
st.set_option('deprecation.showPyplotGlobalUse', False)

st.markdown("""
This app will build **forecast model** adding holiday information & generate predictions for units sold, total sales & operating profit.
- Below is sample Adidas sales dataset for last 2 years consist of different footwear products
( Men's Street Footwear,Men's Athletic Footwear,Men's Apparel,Women's Street Footwear,Women's Athletic Footwear,Women's Apparel) **sold across NYC**.
* **Python libraries:** pandas, streamlit, matplotlib

""")

#conn = st.connection("snowflake")

def load_data(table_name):
    ## Read in data table
    st.write(f"Here's some example data from `{table_name}`:")
    table = session.table(table_name)
    
    ## Do some computation on it
    table = table.limit(20)
       
    ## Collect the results. This will run the query and download the data
    table = table.collect()
    return table

# Select and display data table
table_name = "ADIDAS.PUBLIC.SALES_DATA"

## Display data table
with st.expander("Expand this area to see sample sales dataset"):
    df = load_data(table_name)
    st.dataframe(df)


with st.expander("Expand this area to explore first part"):
    st.markdown("""
- First part will generate forecasting model for units sold for only one product- **Men's Apparel**.
- Since we have sales dataset till 31-Jan-2024,it will generate predictions for units sold for the next 30 days.
- Finally we will generate visualizations in the form of line chart.

""")

    col1, col2, col3 = st.columns(3,gap="small")
    with col1:
        if 'button_clicked1' not in st.session_state:
            st.session_state.button_clicked1 = False
        if st.button("Create Forecasting Model!"):
            st.session_state.button_clicked1=True
            session.sql("CREATE OR REPLACE forecast ADIDAS.PUBLIC.sales_forecast (INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'ADIDAS.PUBLIC.Mens_Apparel_sales'),TIMESTAMP_COLNAME => 'TIMESTAMP',TARGET_COLNAME => 'UNITS_SOLD');").collect()
        if st.session_state.button_clicked1:
            st.success("Forecasting Model created successfully !")
    with col2:
        if 'button_clicked2' not in st.session_state:
            st.session_state.button_clicked2 = False

        if st.button("Create Predictions!"):
            st.session_state.button_clicked2=True
            session.sql("CALL ADIDAS.PUBLIC.sales_forecast!FORECAST(FORECASTING_PERIODS => 30);").collect()
            session.sql("CREATE OR REPLACE TABLE ADIDAS.PUBLIC.sales_predictions AS (SELECT * FROM TABLE(RESULT_SCAN(-1)));").collect()
        if st.session_state.button_clicked2:
            st.success("Predictions created successfully !")
    with col3:
        if 'button_clicked3' not in st.session_state:
            st.session_state.button_clicked3 = False

        if st.button("Create Visualizations!"):
            st.session_state.button_clicked3 = True
        # Execute your SQL command and fetch the results into a DataFrame directly
            df = session.sql("SELECT timestamp, units_sold, NULL AS forecast FROM ADIDAS.PUBLIC.Mens_Apparel_sales UNION SELECT TS AS timestamp, NULL AS units_sold, forecast FROM ADIDAS.PUBLIC.sales_predictions ORDER BY timestamp asc").to_pandas()
    
        # Plotting using Matplotlib
            fig, ax = plt.subplots(figsize=(10, 6))  # You can adjust the figure size as needed
            ax.plot(df['TIMESTAMP'], df['UNITS_SOLD'], label='Units Sold', color='blue', linewidth=2)
            ax.plot(df['TIMESTAMP'], df['FORECAST'], label='Forecast', color='yellow', linewidth=2)

        # Beautifying the plot
            ax.set_xlabel('Timestamp', fontsize=14)
            ax.set_ylabel('Values', fontsize=14)
            ax.set_title('Units Sold Forecast Visualization', fontsize=16)
            ax.grid(True)
            ax.legend()
            st.session_state.fig = fig
            # Show the plot in Streamlit
            
        if st.session_state.button_clicked3:
        
            st.pyplot(st.session_state.fig)
            st.success("Visualization created")

#st.divider()
st.write(":heavy_minus_sign:" * 32) 
st.write(":heavy_minus_sign:" * 32) 
#st.divider()
st.markdown("""
- Second part will generate forecasting model for units sold for multiple products- **Men's Apparel**,**Men's Athletic Footwear** & **Men's Street Footwear**.
- Since we have sales dataset till 31-Jan-2024,it will generate predictions for units sold for the next 30 days.
- Finally we will generate visualizations in the form of line chart.

""")

col4, col5, col6 = st.columns(3,gap="small")
with col4:
    if 'button_clicked4' not in st.session_state:
        st.session_state.button_clicked4 = False
    if st.button("Build Forecasting Model!"):
        st.session_state.button_clicked4=True
        session.sql("CREATE OR REPLACE forecast ADIDAS.PUBLIC.allproducts_forecast (INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'ADIDAS.PUBLIC.allproducts_sales'),SERIES_COLNAME => 'PRODUCT',TIMESTAMP_COLNAME => 'TIMESTAMP',TARGET_COLNAME => 'UNITS_SOLD');").collect()
    if st.session_state.button_clicked4:
        st.success("Forecasting Model created successfully !")
with col5:
    if 'button_clicked5' not in st.session_state:
        st.session_state.button_clicked5 = False
    if st.button("Create Predictions !"):
        st.session_state.button_clicked5=True
        session.sql("CALL ADIDAS.PUBLIC.allproducts_forecast!forecast(INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'ADIDAS.PUBLIC.us_forecast_data'),SERIES_COLNAME => 'product',TIMESTAMP_COLNAME => 'timestamp');").collect()
        session.sql("CREATE OR REPLACE TABLE ADIDAS.PUBLIC.us_sales_predictions AS (SELECT * FROM TABLE(RESULT_SCAN(-1)));").collect()
    if st.session_state.button_clicked5:
        st.success("Predictions created successfully !")
with col6:
    if 'button_clicked6' not in st.session_state:
        st.session_state.button_clicked6 = False
    if st.button("Create Visualizations !"):
        st.session_state.button_clicked6=True
        # Fetch data into a DataFrame
        df = session.sql("SELECT to_date(timestamp)as timestamp, units_sold, product, NULL AS forecast FROM ADIDAS.PUBLIC.allproducts_sales where to_date(timestamp ) > (SELECT max(to_date(timestamp)) - interval ' 1 months' FROM ADIDAS.PUBLIC.allproducts_sales) UNION SELECT to_date(TS) AS timestamp, NULL AS units_sold, series AS product, forecast FROM ADIDAS.PUBLIC.us_sales_predictions ORDER BY timestamp, product asc").to_pandas()
        
    
# Altair tooltip for interactive exploration
        tooltip = [alt.Tooltip('TIMESTAMP:T', title='TIMESTAMP'),
                    alt.Tooltip('PRODUCT:N', title='PRODUCT'),
                    alt.Tooltip('UNITS_SOLD:Q', title='UNITS SOLD'),
                    alt.Tooltip('FORECAST:Q', title='FORECAST')]
# Create a base chart with common encoding
        base = alt.Chart(df).encode(
            alt.X('TIMESTAMP:T', title='Timestamp'),
            alt.Color('PRODUCT:N', legend=alt.Legend(title="Product"))
         ).properties(
            width='container'
         )
         
# Define the units sold line
        units_sold_line = base.mark_line().encode(
            alt.Y('UNITS_SOLD:Q', title='Values', scale=alt.Scale(zero=False)),
            tooltip=tooltip
        )
# Define the forecast line
        forecast_line = base.mark_line(strokeDash=[5,5]).encode(
            alt.Y('FORECAST:Q', scale=alt.Scale(zero=False)),
            tooltip=tooltip
        )
# Combine the charts
        #chart = alt.layer(units_sold_line, forecast_line).resolve_scale(y='independent')
        #chart = alt.layer( forecast_line).resolve_scale(y='independent')
        chart = alt.layer(units_sold_line, forecast_line).interactive()
        #chart.grid(True)
        #chart.legend()
        st.session_state.chart = chart

# Display the chart in Streamlit
    if st.session_state.button_clicked6:

        st.altair_chart(st.session_state.chart, use_container_width=True)
        st.success("Visualization created")
        



