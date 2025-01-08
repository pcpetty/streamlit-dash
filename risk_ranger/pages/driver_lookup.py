# Libraries and Modules
import streamlit as st 
from utils.helpers import text_input_with_default
from utils.database import fetch_data
import uuid
# ------------------------------------------------------------------------------------------------
# DRIVER LOOKUP PAGE # ------------------------------------------------------------------------------------------------
def driver_lookup():
    prefix = "driver_lookup"
    """
    Provides a UI for looking up driver information.
    """
    st.subheader("Driver Lookup")
    driver_id = text_input_with_default("Enter Driver ID or Name:", key=f"{prefix}_driver_id_{uuid.uuid4()}")
    
    if st.button("Search Driver"):
        query = """
        SELECT * FROM drivers 
        WHERE driver_id = %s OR driver_name ILIKE %s
        """
        params = (driver_id, f"%{driver_id}%")
        driver_data = fetch_data(query, params)
        
        if not driver_data.empty:
            st.write(driver_data)
        else:
            st.warning("No driver found!")