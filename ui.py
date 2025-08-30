import streamlit as st
import pandas as pd
from io import BytesIO
import datetime

# Import UI Element Files
import sys
sys.path.append("ui")
import home_ui
import browse_ui
import postItem_ui
import myListings_ui

# Initialize session state storage if not exists
if "listings" not in st.session_state:
    st.session_state.listings = []  # Each listing: dict with keys

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
