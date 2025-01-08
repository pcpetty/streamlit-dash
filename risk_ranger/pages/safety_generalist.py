import streamlit as st
from utils.database import fetch_data, save_data

def safety_generalist_dashboard():
    st.title("Safety Generalist Dashboard")
    st.subheader("View and Manage Open Accident Reports")
    # Filters for Reports
    st.sidebar.header("Filter Reports")
    date_filter = st.sidebar.date_input("Filter by Date")
    location_filter = st.sidebar.text_input("Filter by Location")
    # Base Query
    query = "SELECT * FROM accident_reports WHERE status = 'open'"
    params = {}
    # Apply Filters
    if date_filter:
        query += " AND accident_date = :accident_date"
        params["accident_date"] = date_filter.strftime('%Y-%m-%d')
    if location_filter:
        query += " AND accident_location ILIKE :location"
        params["location"] = f"%{location_filter}%"
    try:
        # Fetch Reports
        reports = fetch_data(query, params)
        if not reports.empty:
            st.table(reports)
            # Select a Report to View/Edit
            selected_report_id = st.selectbox("Select a Report to View/Edit", reports["id"].tolist())
            if st.button("View Report"):
                view_report(selected_report_id)
        else:
            st.info("No open reports found with the given filters.")
    except Exception as e:
        st.error(f"Failed to fetch reports: {e}")
def view_report(report_id):
    """
    Displays the details of a specific report.
    """
    st.subheader(f"Details for Report ID: {report_id}")
    # Fetch Report Details
    query = "SELECT * FROM accident_reports WHERE id = :report_id;"
    params = {"report_id": report_id}
    try:
        report = fetch_data(query, params)
        if not report.empty:
            st.write(report)
            # Edit Report Section
            if st.checkbox("Edit Report"):
                accident_description = st.text_area("Update Accident Description", value=report["accident_description"].iloc[0])
                status = st.selectbox("Update Status", ["open", "closed"], index=["open", "closed"].index(report["status"].iloc[0]))
                if st.button("Save Changes"):
                    update_query = """
                        UPDATE accident_reports
                        SET accident_description = :description, status = :status
                        WHERE id = :report_id
                    """
                    update_params = {
                        "description": accident_description,
                        "status": status,
                        "report_id": report_id
                    }
                    try:
                        save_data(update_query, update_params)
                        st.success("Report updated successfully!")
                    except Exception as e:
                        st.error(f"Failed to update report: {e}")
        else:
            st.warning("Report not found.")
    except Exception as e:
        st.error(f"Failed to fetch report details: {e}")