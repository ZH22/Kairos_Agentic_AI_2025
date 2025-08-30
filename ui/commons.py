import streamlit as st

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

# ---------- 1.  one-time initialisation ----------
def init_keys():
    if "listings" not in st.session_state:
        st.session_state.listings = []  # Each listing: dict with keys

    if "user" not in st.session_state:
        st.session_state.user = None