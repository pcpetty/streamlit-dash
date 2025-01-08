# Libraries and Modules
import streamlit as st
import uuid
import os 
from utils.database import save_data
from utils.pdf_generator import generate_pdf
from utils.accident_helpers import (
    get_company_info, get_additional_remarks, load_information, get_police_information, get_tow_information, get_vehicle, get_driver, collect_person_reporting_details, accident_or_incident, dot_recordable, post_accident_testing, followup_needed, injury_details, post_accident_testing_timeline, citation_info
)
from utils.database import fetch_data
from utils.helpers import text_input_with_default, get_yes_no, get_or_set_session_data, generate_flt_number_with_check
# ------------------------------------------------------------------------------------------------
# USER ACCIDENT FORM # ------------------------------------------------------------------------------------------------
# Accident Report Form
def accident_form():
    """
    Displays the accident report form, collects data, uploads it to the database, and generates a PDF.
    """
    st.title("Accident Report Form")

    # Section 1: General Information
    st.header("General Information")
    company_info = get_company_info()
    accident_date = st.date_input("Accident Date:")
    accident_time = st.time_input("Accident Time:")
    accident_location = st.text_input("Accident Location or Address:")
    accident_description = st.text_area("Brief Description of the Accident:")
    weather_info = st.selectbox("Weather Conditions:", ['Clear', 'Overcast', 'Rainy', 'Windy', 'Snowy'])
    road_conditions = st.selectbox("Road Conditions:", ['Dry', 'Wet', 'Icy', 'Snowy'])

    # Section 2: Driver and Vehicle Information
    st.header("Driver and Vehicle Information")
    v1_driver = get_driver("V1 Driver")
    v1_vehicle = get_vehicle("V1 Vehicle")
    v2_driver = get_driver("V2 Driver")
    v2_vehicle = get_vehicle("V2 Vehicle")

    # Section 3: Additional Details
    st.header("Additional Details")
    tow_info = get_tow_information()
    police_info = get_police_information()
    load_info = load_information()
    reporting_details = collect_person_reporting_details()
    classification = accident_or_incident()
    dot_info = dot_recordable()
    testing_result = post_accident_testing()
    followup_info = followup_needed()
    injury_info = injury_details()
    additional_remarks = get_additional_remarks()

    # Display Information Summary
    st.subheader("Summary of Information")
    st.write(f"Company: {company_info}")
    st.write(f"Date: {accident_date}, Time: {accident_time}")
    st.write(f"Location: {accident_location}")
    st.write(f"Description: {accident_description}")
    st.write(f"Weather: {weather_info}, Road: {road_conditions}")
    st.write(f"Driver 1: {v1_driver}, Vehicle 1: {v1_vehicle}")
    st.write(f"Driver 2: {v2_driver}, Vehicle 2: {v2_vehicle}")
    st.write(f"Towing Information: {tow_info}")
    st.write(f"Police Information: {police_info}")
    st.write(f"Load Information: {load_info}")
    st.write(f"DOT Recordable: {dot_info}")
    st.write(f"Injury Details: {injury_info}")
    st.write(f"Additional Remarks: {additional_remarks}")

    # Submit Data
    if st.button("Submit Accident Report"):
        flt_number = generate_flt_number_with_check()  # Generate unique FLT number
        st.success(f"FLT Number Generated: {flt_number}")

        # Save to Database
        query = """
            INSERT INTO accident_reports (
                company_info, accident_date, accident_time,
                accident_location, accident_description, weather_info, road_conditions,
                v1_driver, v1_vehicle, v2_driver, v2_vehicle,
                injury_occurred, injury_description, hospital, hospital_name,
                accident_type, incident_type, flt_number
            ) VALUES (
                :company_info, :accident_date, :accident_time,
                :accident_location, :accident_description, :weather_info, :road_conditions,
                :v1_driver, :v1_vehicle, :v2_driver, :v2_vehicle,
                :injury_occurred, :injury_description, :hospital, :hospital_name,
                :accident_type, :incident_type, :flt_number
            )
        """
        params = {
            "company_info": company_info,
            "accident_date": accident_date.strftime('%Y-%m-%d'),
            "accident_time": accident_time.strftime('%H:%M:%S'),
            "accident_location": accident_location,
            "accident_description": accident_description,
            "weather_info": weather_info,
            "road_conditions": road_conditions,
            "v1_driver": v1_driver,
            "v1_vehicle": v1_vehicle,
            "v2_driver": v2_driver,
            "v2_vehicle": v2_vehicle,
            "injury_occurred": injury_info.get("injury_occurred", False),
            "injury_description": injury_info.get("injury_description", ""),
            "hospital": injury_info.get("hospital", False),
            "hospital_name": injury_info.get("hospital_name", ""),
            "accident_type": classification.get("accident_type", ""),
            "incident_type": classification.get("incident_type", ""),
            "flt_number": flt_number,
            "police_officer_name": police_info.get("officer_name", ""),
            "police_badge_number": police_info.get("badge_number", ""),
            "police_report_number": police_info.get("report_number", ""),
            "police_department": police_info.get("department", ""),
            "tow_company": tow_info.get("company_name", ""),
            "tow_driver": tow_info.get("driver_name", ""),
            "tow_contact": tow_info.get("contact_number", ""),
            "tow_location": tow_info.get("location", ""),
        }

        save_data(query, params)
        st.success("Accident report successfully submitted!")
        
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


        # Generate PDF
        generate_pdf(flt_number, params)

