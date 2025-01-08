import streamlit as st
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def initialize_session_state():
    """
    Initializes session state keys for the application.
    Ensures that default keys are present with appropriate values.
    """
    default_keys = {
        "authenticated": False,
        "username": None,
        "role": None,
        "accident_report": {},  # Example: Holds accident report data
        "report_drafts": {},   # Example: Holds draft reports by FLT number
        "uploaded_photos": []  # Example: Stores uploaded photo paths
    }

    for key, default_value in default_keys.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
            logging.info(f"Session state key '{key}' initialized with value: {default_value}")

def clear_session_state(keys_to_clear=None):
    """
    Clears specific keys in the session state or all keys if none are specified.
    
    Args:
        keys_to_clear (list, optional): List of keys to clear. Defaults to None.
    """
    if keys_to_clear is None:
        keys_to_clear = list(st.session_state.keys())

    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
            logging.info(f"Session state key '{key}' cleared.")

# Example: Using initialize_session_state
if __name__ == "__main__":
    initialize_session_state()
    st.write("Session state initialized.")
    if st.button("Clear Authentication State"):
        clear_session_state(keys_to_clear=["authenticated", "username", "role"])
