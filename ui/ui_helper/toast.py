import streamlit as st

# To add to top of file where toast is supposed to be shown
def show_toast():
  sst = st.session_state
  toast = sst.pop("pending_toast", None)
  if toast:
    st.toast(**toast)
  
def add_toast(message_body, toast_icon = "✅"):
  sst = st.session_state
  message = {"body": f"{message_body}", "icon": toast_icon}
  sst["pending_toast"] = message