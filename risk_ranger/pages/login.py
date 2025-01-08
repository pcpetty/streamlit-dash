# ------------------------------------------------------------------------------------------------
# Risk Ranger Login # ------------------------------------------------------------------------------------------------
# Libraries and Modules
import streamlit as st
import logging
from utils.database import db_connect, authenticate_user
from utils.session_state import initialize_session_state, clear_session_state

# Configure logging
logging.basicConfig(level=logging.INFO)

def login():
    """
    Handles user login and session state management.
    """
    # Initialize session state
    initialize_session_state()
    st.title("Risk Ranger Login")
    st.subheader("Please log in to continue.")
    # Login Form
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    login_button = st.button("Login")
    if login_button:
        # Authenticate user
        role = authenticate_user(username, password)
        if role:
            # Update session state
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["role"] = role
            st.success(f"Welcome, {username} ({role})")
            st.experimental_rerun()  # Refresh the page to update session state
        else:
            st.error("Invalid username or password. Please try again.")
    # Handle authenticated state
    if st.session_state["authenticated"]:
        st.success(f"Logged in as: {st.session_state['username']} ({st.session_state['role']})")
        st.button("Logout", on_click=clear_session_state)
# ------------------------------------------------------------------------------------------------