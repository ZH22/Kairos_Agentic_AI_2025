import streamlit as st
from db_Handler import DbHandler
from commons import init_keys

def display():

    # Init Db Handler object
    db = DbHandler()
    users = db.get_users()
    usernames = [u["username"] for u in users]

    st.write(st.session_state.get("user"))

    st.title("Welcome to Kairos 🛍️") 
    st.write("A simple e-commerce prototype built with Streamlit.")


    st.header("Select your User")
    option = st.selectbox(
        "Which Example User Experience would you like to try?",
        (usernames),
    )

    # (Note: Did not use 'key' property in selectBox as 
    #   session state will be removed if unrendered)
    st.session_state.user = option
