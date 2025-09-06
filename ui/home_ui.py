import streamlit as st
from db_Handler import DbHandler
from commons import init_keys

from ui_helper.toast import show_toast, add_toast;

def display():

    sst = st.session_state

    # Shows toast on rerun (if applicable)
    show_toast()

    # Init Db Handler object
    db = DbHandler()
    users = db.get_users()
    usernames = [u["username"] for u in users]

    st.title("Welcome to Kairos 🛍️") 
    st.write("A simple e-commerce prototype built with Streamlit.")


    st.header("Select your User")
    option = st.selectbox(
        "Which Example User Experience would you like to try?",
        (usernames),
    )

    # Add selected user to state on first run
    if("selected_user" not in sst):
        sst["selected_user"] = option
    elif option != sst["selected_user"]:
        sst["selected_user"] = option
        add_toast(f"User Changed to : { option }")
        st.rerun()

    # (Note: Did not use 'key' property in selectBox as 
    #   session state will be removed if unrendered)
    sst.user = option
