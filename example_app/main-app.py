import streamlit as st
import importlib.util
import os


# Establish Snowflake session

st.set_page_config(
 #   #page_title="Ex-stream-ly Cool App",
    #page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Define your pages with icons
pages = {
    "🏠 Home": "example_app/st-home.py",
    "👖 Part One": "example_app/st-partone.py",
    "🥿 Part Two": "example_app/st-parttwo.py",
    "💰 Part Three": "example_app/st-partthree.py",
    "💵 Part Four": "example_app/st-partfour.py"
}

# Sidebar for navigation with icons
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Get the corresponding page path
page_path = pages[selection]

# Function to dynamically import the selected page
def load_page(page_path):
    page_name = os.path.basename(page_path).replace(".py", "")
    spec = importlib.util.spec_from_file_location(page_name, page_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

# Load and display the selected page
try:
    load_page(page_path)
except Exception as e:
    st.error(f"Error loading {selection}: {e}")