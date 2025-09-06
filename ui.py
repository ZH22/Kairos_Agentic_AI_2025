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


# Custom router logic for intermediate evaluation page
if "page" not in st.session_state:
    st.session_state.page = "Home"

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

if st.session_state.page == "evaluation":
    import ui.evaluation_ui as evaluation_ui
    evaluation_ui.display()
else:
    st.sidebar.title("E-Commerce App")
    page = st.sidebar.radio("Go to", ["Home", "Browse", "Post Item", "My Listings"],
                            index=["Home", "Browse", "Post Item", "My Listings"].index(st.session_state.page) if st.session_state.page in ["Home", "Browse", "Post Item", "My Listings"] else 0)
    st.session_state.page = page
    if page == "Home":
        home_ui.display()
    elif page == "Browse":
        browse_ui.display()
    elif page == "Post Item":
        postItem_ui.display()
    elif page == "My Listings":
        myListings_ui.display()
