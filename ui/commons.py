import streamlit as st
from db_Handler import DbHandler

# Predefined categories
categories_list = [
    "Accomodation",
    "Clothing and Accessories",
    "Everything Else",
    "Food and Drink Containers",
    "Furniture and Appliances",
    "Sports and Fitness",
    "Tech and Gadgets",
    "Textbooks and Study Materials"
]

condition_list = ["New", "Like New", "Used", "Heavily Used"]

# ---------- 1.  one-time initialisation ----------
def init_keys():
    if "listings" not in st.session_state:

        # Import from external and save to local session
        db = DbHandler()
        st.session_state.listings = db.get_listings() # Returns an array of listing objects

    if "user" not in st.session_state:
        st.session_state.user = None

def refresh_listings_from_db():
    """Refresh listings from database"""
    db = DbHandler()
    st.session_state.listings = db.get_listings()