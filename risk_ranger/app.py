# RISK RANGER STREAMLIT VERSION
import streamlit as st
from pages import login, admin, home, accident_report, driver_lookup, vehicle_lookup, flt_lookup, upload_photos, safety_generalist, liability_adjuster
from utils.database import initialize_users_table

# Role-to-Page Mapping
ROLE_PAGE_MAPPING = {
    "superuser": ["Home", "Accident Report Form", "Driver Lookup", "Vehicle Lookup", "FLT Lookup", "Admin", "Upload Photos"],
    "safety_generalist": ["Home", "Accident Report Form", "Driver Lookup", "Vehicle Lookup", "Upload Photos"],
    "liability_adjuster": ["Home", "Driver Lookup", "Vehicle Lookup", "FLT Lookup"],
}
# Page Function Mapping
PAGE_FUNCTION_MAPPING = {
    "Login": login.login,
    "Home": home.home,
    "Accident Report Form": accident_report.accident_form,
    "Driver Lookup": driver_lookup.driver_lookup,
    "Vehicle Lookup": vehicle_lookup.vehicle_lookup,
    "FLT Lookup": flt_lookup.flt_lookup,
    "Admin": admin.render_admin_dashboard,
    "Safety Generalist": safety_generalist.safety_generalist_dashboard,
    "Liability Adjuster": liability_adjuster.liability_adjuster_dashboard,
    "Upload Photos": upload_photos.upload_photo,
}
def check_authentication():
    return "authenticated" in st.session_state and st.session_state["authenticated"]
def main():
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    if not check_authentication():
        page = "Login"  # Redirect to Login if not authenticated
    else:
        role = st.session_state.get("role", "user")
        available_pages = ROLE_PAGE_MAPPING.get(role, [])
        page = st.sidebar.radio("Go to", available_pages)
    
    # Render Selected Page
    page_function = PAGE_FUNCTION_MAPPING.get(page, lambda: st.error("Page not found!"))
    page_function()
if __name__ == "__main__":
    # Initialize Session State
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.session_state["role"] = None
    # Initialize Database Button (Admin Only)
    if st.sidebar.button("Initialize Database"):
        initialize_users_table()
    # Run the Main Application
    main()