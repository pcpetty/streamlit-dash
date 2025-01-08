# Libraries and Modules
import streamlit as st 
from utils.helpers import text_input_with_default
from utils.database import fetch_data
import uuid
# ------------------------------------------------------------------------------------------------
# CLAIM NUMBER LOOKUP PAGE # ------------------------------------------------------------------------------------------------
def flt_lookup():
    prefix = "flt_lookup"
    st.subheader("FLT Number Lookup")
    flt_number = text_input_with_default("Enter FLT Number:", key=f"{prefix}_flt_{uuid.uuid4()}")
    if st.button("Search by FLT"):
        query = """
        SELECT * FROM accident_reports 
        WHERE reference_key = %s
        """
        params = (flt_number,)
        flt_data = fetch_data(query, params)
        if not flt_data.empty:
            st.write(flt_data)
        else:
            st.warning("No records found for this FLT number.")