import streamlit as st
from src.core.db_handler import DbHandler
from src.ui.helpers.commons import init_keys

# Toast functionality removed for restructuring

def display():

    sst = st.session_state

    # Toast functionality removed for restructuring

    # Init Db Handler object
    db = DbHandler()
    users = db.get_users()
    usernames = [u["username"] for u in users]

    # Welcome banner
    st.markdown(
        """
        <div style="
            background: linear-gradient(90deg, #4CAF50, #45a049);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            color: white;
            text-align: center;
        ">
            <h2 style="margin: 0; color: white;">🎆 Welcome to Kairos!</h2>
            <p style="margin: 10px 0; font-size: 16px;">AI-powered campus marketplace - Find what you need, connect with fellow students</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔍 Find Items", use_container_width=True):
            st.session_state.active_page = "Browse"
            st.rerun()
    with col2:
        if st.button("📝 List Items", use_container_width=True):
            st.session_state.active_page = "Post Item"
            st.rerun()
    
    st.title("Welcome to Kairos 🤝") 
    st.write("**Your AI-powered campus connector** - Discover items you need and connect directly with student sellers")
    
    # Value proposition
    st.markdown("""
    ### 🎯 What Makes Kairos Special?
    - **Smart Discovery**: AI helps you find exactly what you need
    - **Campus Community**: Connect safely with fellow students  
    - **Direct Contact**: Message sellers directly to arrange pickup
    - **Market Intelligence**: Get fair pricing insights
    """)


    st.header("👤 Choose Your Profile")
    st.write("Select a user profile to explore how students connect on Kairos:")
    option = st.selectbox(
        "Available profiles (Demo accounts):",
        (usernames),
        help="Each profile has different items and preferences for testing"
    )

    # Add selected user to state on first run
    if("selected_user" not in sst):
        sst["selected_user"] = option
    elif option != sst["selected_user"]:
        sst["selected_user"] = option
        st.success(f"User Changed to: {option}")
        st.rerun()
    
    # (Note: Did not use 'key' property in selectBox as 
    #   session state will be removed if unrendered)
    sst.user = option