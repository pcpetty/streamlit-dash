# Libraries and Modules
import streamlit as st 
import logging
import uuid
import random
import string
from sqlalchemy import text
from utils.database import fetch_data, save_data
# ------------------------------------------------------------------------------------------------
# logging -------------------------------------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
def log_all_keys(key):
    """
    Log every key to detect duplicates during execution.
    """
    logging.info(f"Checking key: {key}")
    # Maintain a global set of keys (only during debugging)
    if not hasattr(log_all_keys, "keys_used"):
        log_all_keys.keys_used = set()
    if key in log_all_keys.keys_used:
        logging.error(f"Duplicate key detected: {key}")
    else:
        log_all_keys.keys_used.add(key) 
# ------------------------------------------------------------------------------------------------
# text_input_with_default ------------------------------------------------------------------------------------------------
def text_input_with_default(label, default_value="", key=None):
    """
    Handles text input with a default value in Streamlit.
    Ensures a unique key for each widget.
    """
    if not key:
        key = f"text_input_{label.replace(' ', '_')}"  # Create a unique fallback key
    logging.info(f"Key used for text_input_with_default: {key}")
    input_value = st.text_input(label, value=default_value, key=f"{key}_{uuid.uuid4()}")
    return input_value.strip()
# ------------------------------------------------------------------------------------------------
# get_yes_no -------------------------------------------------------------------------------------------------
def get_yes_no(prompt, base_key):
    """
    Displays a yes or no question in Streamlit and returns a boolean response.
    Args:
        prompt (str): The question to display.
        base_key (str): A unique base key for the Streamlit widget.
    Returns:
        bool: True if "Yes" is selected, False if "No" is selected.
    """
    key = f"{base_key}_radio"  # Ensure unique key for each widget
    response = st.radio(prompt, options=["Yes", "No"], index=1, key=key)  # Default to "No"
    return response == "Yes"
# ------------------------------------------------------------------------------------------------
# get_or_set_session_data --------------------------------------------------------------
def get_or_set_session_data(key, default):
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]
# ---------------------------------------utils/RRLOGOSMALL.png---------------------------------------------------------
# display_logo -------------------------------------------------------------------------------------------------
def display_logo():
    st.image("utils/RRLOGOSMALL.png")
# LOGO SIDEBAR # ------------------------------------------------------------------------------------------------
# Add a smaller logo to the sidebar
st.sidebar.image("utils/RRLOGOSMALL.png")
# LOGO FOOTER --------------------------------------------------------------------------------------------------
# Add a banner at the footer
st.markdown(
    """
    <div style='position: fixed; bottom: 0; width: 100%; text-align: center; background-color: black; color: orange; padding: 10px;'>
        <h4>RiskRanger | Logistics Simplified</h4>
    </div>
    """,
    unsafe_allow_html=True
)
# ------------------------------------------------------------------------------------------------
# generate_flt_number -------------------------------------------------------------------------------------------------
def generate_flt_number():
    """
    Generates a unique FLT (Federal Load Tracking) number.
    The format could be alphanumeric or numeric based on your requirements.
    """
    prefix = "FLT"
    unique_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"{prefix}-{unique_id}"

def generate_flt_number_with_check(db_engine):
    """
    Generates a unique FLT number and checks the database for duplicates.
    """
    while True:
        flt_number = generate_flt_number()
        query = "SELECT COUNT(*) FROM accident_reports WHERE flt_number = :flt_number"
        result = db_engine.execute(text(query), {"flt_number": flt_number}).scalar()
        if result == 0:
            return flt_number
        
        
def edit_accident_report(report_id):
    query = "SELECT * FROM accident_reports WHERE id = %s"
    report = fetch_data(query, (report_id,))
    if report:
        report = report[0]  # Assuming single record
        st.text_input("Accident Date", value=report["accident_date"], key=f"edit_accident_date_{report_id}")
        st.text_area("Description", value=report["description"], key=f"edit_description_{report_id}")
        if st.button(f"Save Changes for Report {report_id}"):
            update_query = """
                UPDATE accident_reports
                SET accident_date = %s, description = %s
                WHERE id = %s
            """
            update_params = (
                st.session_state[f"edit_accident_date_{report_id}"],
                st.session_state[f"edit_description_{report_id}"],
                report_id
            )
            save_data(update_query, update_params)
            st.success(f"Updated report {report_id} successfully!")