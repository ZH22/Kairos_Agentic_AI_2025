import streamlit as st
import pandas as pd
from io import BytesIO
import datetime
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Import UI Element Files
from src.ui.helpers.commons import init_keys
import src.ui.pages.home_ui as home_ui
import src.ui.pages.browse_ui as browse_ui
import src.ui.pages.postItem_ui as postItem_ui
import src.ui.pages.myListings_ui as myListings_ui
from src.ui.components.help_system import contextual_help_system


# Initialize session state storage if not exists
init_keys()
# ====================================================================

# Sidebar navigation

# --- Custom CSS for sidebar styling ---
st.markdown(
    """
    <style>
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #fafafa;
        padding-top: 20px;
    }
    /* Navigation buttons */
    .nav-button {
        display: block;
        padding: 10px 16px;
        margin: 6px 0;
        border-radius: 10px;
        text-decoration: none;
        font-size: 16px;
        color: black;
    }
    .nav-button:hover {
        background-color: #f0f0f0;
    }
    .nav-button-selected {
        background-color: #FF5A5F;
        color: white !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar navigation with emojis ---
st.sidebar.title("🤝 Kairos Connector")
st.sidebar.caption("AI-powered campus marketplace")



# Define pages with clear descriptions
pages = {
    "🏠 Start Here": "Home",
    "🔍 Find Items": "Browse", 
    "📝 List Items": "Post Item",
    "📋 My Listings": "My Listings",
}

# Track active page in session state
if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"

# Render nav buttons
for emoji_label, page_name in pages.items():
    button_type = "nav-button-selected" if st.session_state.active_page == page_name else "nav-button"
    if st.sidebar.button(emoji_label, key=page_name):
        st.session_state.active_page = page_name

page = st.session_state.active_page

# --- Evaluation Page (Special handling) ---
if page == "evaluation":
    import src.ui.pages.evaluation_ui as evaluation_ui
    contextual_help_system("evaluation")
    evaluation_ui.display()

# --- Home ---
elif page == "Home":
    contextual_help_system("home")
    home_ui.display()

# --- Browse Page (Chat + Toggle Search Listings) ---
elif page == "Browse":
    contextual_help_system("browse")
    browse_ui.display()

# --- Post Item ---
elif page == "Post Item":
    contextual_help_system("post")
    postItem_ui.display()
    
# --- My Listings ---
elif page == "My Listings":
    contextual_help_system("mylistings")
    myListings_ui.display()
