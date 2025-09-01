import streamlit as st
import pandas as pd
from io import BytesIO
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import UI Element Files
import sys
sys.path.append("ui")
from ui.commons import init_keys
import ui.home_ui as home_ui
import ui.browse_ui as browse_ui
import ui.postItem_ui as postItem_ui
import ui.myListings_ui as myListings_ui


# Initialize session state storage if not exists
init_keys()
# ====================================================================

# Sidebar navigation
st.sidebar.title("E-Commerce App")
page = st.sidebar.radio("Go to", ["Home", "Browse", "Post Item", "My Listings"])

# --- Home ---
if page == "Home":
    home_ui.display()

# --- Browse ---
elif page == "Browse":
    browse_ui.display()

# --- Post Item ---
elif page == "Post Item":
    postItem_ui.display()
    
# --- My Listings ---
elif page == "My Listings":
    myListings_ui.display()
