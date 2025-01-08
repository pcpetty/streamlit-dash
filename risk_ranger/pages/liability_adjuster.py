import streamlit as st
from utils.database import fetch_data, save_data

def liability_adjuster_dashboard():
    st.title("Liability Adjuster Dashboard")
    st.subheader("View and Manage Pending Claims")
    # Filters for Claims
    st.sidebar.header("Filter Claims")
    date_filter = st.sidebar.date_input("Filter by Date")
    location_filter = st.sidebar.text_input("Filter by Location")
    # Base Query
    query = "SELECT * FROM accident_reports WHERE status = 'pending'"
    params = {}
    # Apply Filters
    if date_filter:
        query += " AND accident_date = :accident_date"
        params["accident_date"] = date_filter.strftime('%Y-%m-%d')
    if location_filter:
        query += " AND accident_location ILIKE :location"
        params["location"] = f"%{location_filter}%"
    try:
        # Fetch Claims
        claims = fetch_data(query, params)
        if not claims.empty:
            st.table(claims)
            # Select a Claim to View/Edit
            selected_claim_id = st.selectbox("Select a Claim to View/Edit", claims["id"].tolist())
            if st.button("View Claim"):
                view_claim(selected_claim_id)
        else:
            st.info("No pending claims found with the given filters.")
    except Exception as e:
        st.error(f"Failed to fetch claims: {e}")
def view_claim(claim_id):
    """
    Displays the details of a specific claim.
    """
    st.subheader(f"Details for Claim ID: {claim_id}")
    # Fetch Claim Details
    query = "SELECT * FROM accident_reports WHERE id = :claim_id;"
    params = {"claim_id": claim_id}
    try:
        claim = fetch_data(query, params)
        if not claim.empty:
            st.write(claim)
            # Edit Claim Section
            if st.checkbox("Edit Claim"):
                adjuster_notes = st.text_area("Adjuster Notes", value=claim["adjuster_notes"].iloc[0])
                status = st.selectbox(
                    "Update Status",
                    ["pending", "approved", "rejected"],
                    index=["pending", "approved", "rejected"].index(claim["status"].iloc[0])
                )
                if st.button("Save Changes"):
                    update_query = """
                        UPDATE accident_reports
                        SET adjuster_notes = :notes, status = :status
                        WHERE id = :claim_id
                    """
                    update_params = {
                        "notes": adjuster_notes,
                        "status": status,
                        "claim_id": claim_id
                    }
                    try:
                        save_data(update_query, update_params)
                        st.success("Claim updated successfully!")
                    except Exception as e:
                        st.error(f"Failed to update claim: {e}")
        else:
            st.warning("Claim not found.")
    except Exception as e:
        st.error(f"Failed to fetch claim details: {e}")
