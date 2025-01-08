
import streamlit as st 
# from ..utils.helpers import text_input_with_default
from utils.database import fetch_data
import logging
# ------------------------------------------------------------------------------------------------
# VEHICLE LOOKUP PAGE
# ------------------------------------------------------------------------------------------------
def vehicle_lookup():
    """
    Provides a UI for looking up vehicle information with enhanced error handling and input validation.
    """
    st.subheader("Vehicle Lookup")
    logging.info("Vehicle Lookup page loaded.")
    # Input field for vehicle lookup
    vehicle_id = st.text_input("Enter Vehicle ID or License Plate:", key="vehicle_lookup_id").strip()
    # Button to trigger the search
    if st.button("Search Vehicle"):
        # Validate input
        if not vehicle_id:
            st.warning("Please enter a valid Vehicle ID or License Plate.")
            return
        # SQL query to fetch vehicle data
        query = """
        SELECT * FROM vehicles 
        WHERE vehicle_id = %s OR license_plate ILIKE %s
        LIMIT 50
        """
        params = (vehicle_id, f"%{vehicle_id}%")
        try:
            vehicle_data = fetch_data(query, params)
            if not vehicle_data.empty:
                st.success("Vehicle found!")
                st.write(vehicle_data)
            else:
                st.warning("No vehicle found matching the provided ID or license plate.")
        except Exception as e:
            logging.error(f"Error fetching vehicle data: {e}")
            st.error("An error occurred while fetching vehicle data. Please try again later.")
# ------------------------------------------------------------------------------------------------
