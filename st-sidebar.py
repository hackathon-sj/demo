import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
from snowflake.snowpark import Session

# Establish Snowflake session
st.cache_data.clear()
st.cache_resource.clear()

def create_session():
    return Session.builder.configs(st.secrets["snowflake"]).create()

session = create_session()

st.title('Sales Forecast Visualization Application')

st.markdown("""
This app will build **forecast model** adding holiday information & generate predictions for units sold, total sales & operating profit.
- Below is a sample Adidas sales dataset for the last 2 years consisting of different footwear products
(Men's Street Footwear, Men's Athletic Footwear, Men's Apparel, Women's Street Footwear, Women's Athletic Footwear, Women's Apparel) **sold across NYC**.
* **Python libraries:** pandas, streamlit, matplotlib, altair
""")

def load_data(table_name):
    st.write(f"Here's some example data from `{table_name}`:")
    table = session.table(table_name)
    table = table.limit(20)
    table = table.collect()
    return table

table_name = "ADIDAS.PUBLIC.SALES_DATA"

with st.expander("See sample sales dataset"):
    df = load_data(table_name)
    st.dataframe(df)


def make_heatmap ():
        df = session.sql("SELECT timestamp, units_sold, NULL AS forecast FROM ADIDAS.PUBLIC.Mens_Apparel_sales UNION SELECT TS AS timestamp, NULL AS units_sold, forecast FROM ADIDAS.PUBLIC.sales_predictions ORDER BY timestamp asc").to_pandas()
    
        # Plotting using Matplotlib
        #fig, ax = plt.subplots(figsize=(10, 6))
        fig, ax = plt.subplots()  # You can adjust the figure size as needed
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
        


        return st.session_state.fig


# Sidebar for actions
with st.sidebar:
    if 'button_clicked1' not in st.session_state:
        st.session_state.button_clicked1 = False
    if st.button("Create Forecasting Model!"):
        st.session_state.button_clicked1=True
        session.sql("CREATE OR REPLACE forecast ADIDAS.PUBLIC.sales_forecast (INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'ADIDAS.PUBLIC.Mens_Apparel_sales'),TIMESTAMP_COLNAME => 'TIMESTAMP',TARGET_COLNAME => 'UNITS_SOLD');").collect()
    if st.session_state.button_clicked1:
        st.success("Forecasting Model created successfully !")
        
    if 'button_clicked2' not in st.session_state:
        st.session_state.button_clicked2 = False
    if st.button("Create Predictions!"):
        st.session_state.button_clicked2=True
        session.sql("CALL ADIDAS.PUBLIC.sales_forecast!FORECAST(FORECASTING_PERIODS => 30);").collect()
        session.sql("CREATE OR REPLACE TABLE ADIDAS.PUBLIC.sales_predictions AS (SELECT * FROM TABLE(RESULT_SCAN(-1)));").collect()
    if st.session_state.button_clicked2:
        st.success("Predictions created successfully !")
    
    if 'button_clicked3' not in st.session_state:
        st.session_state.button_clicked3 = False
    if st.button("Create Visualizations!"):
        st.session_state.button_clicked3=True


col = st.columns((1.5, 4.5, 2), gap='medium')

with col[0]:
    st.markdown('#### Visualization')
     
    heatmap= make_heatmap()
    if st.session_state.button_clicked3:
        
        st.pyplot(heatmap,use_container_width=True)
        #st.success("Visualization created")
     
    if st.button("Build Forecasting Model!"):
        # Build Forecasting Model logic here
        st.success("Forecasting Model created successfully !")
    if st.button("Generate Predictions!"):
        # Generate Predictions logic here
        st.success("Predictions created successfully !")
    if st.button("Generate Visualizations!"):
        # Generate Visualizations logic for col6 here
        # Visualization logic here (use fit-to-screen mode)
        st.success("Visualization created")
