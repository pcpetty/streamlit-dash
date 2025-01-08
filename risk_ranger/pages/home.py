import streamlit as st

def home():
    """
    Displays the home page with an overview of the application.
    """
    # App Branding
    st.title("Welcome to Risk Ranger")
    st.image("static/uploads/RRLOGOSMALL.png", use_column_width=True)  # Replace with your app logo
    st.subheader("Your Safety Management Companion")
    st.markdown("""
        Risk Ranger streamlines accident reporting, driver and vehicle lookups, and claim management.
        Whether you're a safety generalist, liability adjuster, or administrator, we have the tools you need!
    """)
    # Role-Based Content
    if "role" in st.session_state:
        role = st.session_state["role"]
        st.success(f"Logged in as: {st.session_state['username']} ({role})")
        if role == "superuser":
            st.info("As a **Superuser**, you have access to all features, including user management and detailed reports.")
        elif role == "safety_generalist":
            st.info("As a **Safety Generalist**, you can create accident reports and track ongoing cases.")
        elif role == "liability_adjuster":
            st.info("As a **Liability Adjuster**, you can manage claims, adjust financials, and review reports.")
    else:
        st.warning("You are not logged in. Please log in to access the full features.")
    # Quick Links
    st.markdown("## Quick Links")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Accident Reports"):
            st.experimental_set_query_params(page="accident_reports")
    with col2:
        if st.button("Driver Lookup"):
            st.experimental_set_query_params(page="driver_lookup")
    with col3:
        if st.button("Tutorial"):
            st.experimental_set_query_params(page="tutorial")
    # App Updates or Announcements
    st.markdown("## Announcements")
    st.markdown("""
    - **Version 1.0.0 Released!** Check out the new accident reporting features.
    - **Upcoming Maintenance:** Scheduled for this weekend. Expect brief downtime.
    """)
    # Footer
    st.markdown("---")
    st.markdown("© 2025 Risk Ranger | Built for safety and efficiency.")

