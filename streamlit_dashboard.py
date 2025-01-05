# RISK RANGER STREAMLIT VERSION # ------------------------------------------------------------------------------------------------
# Import Libraries and Modules # ------------------------------------------------------------------------------------------------
import streamlit as st
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import textwrap
from fpdf import FPDF
from colorama import init, Fore, Style
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import json
from openpyxl.chart import BarChart, Reference
from pathlib import Path
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
from sqlalchemy import text
import uuid

# ------------------------------------------------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES # ------------------------------------------------------------------------------------------------
load_dotenv()  # Load environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("Database URL is not set or loaded correctly.")
else:
    print(f"Database URL loaded: {DATABASE_URL}")

# ------------------------------------------------------------------------------------------------
# CONNECT TO PSQL DB # ------------------------------------------------------------------------------------------------
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URL)

# Check the connection
try:
    with engine.connect() as conn:
        print("Database connection successful.")
except Exception as e:
    print(f"Database connection failed: {e}")

# ------------------------------------------------------------------------------------------------
# GET DATA FROM PSQL # ------------------------------------------------------------------------------------------------
def fetch_data(query, params=None):
    """
    Executes a query and fetches data from the database.
    Returns a DataFrame.
    """
    try:
        with engine.connect() as conn:
            return pd.read_sql_query(query, conn, params=params)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()
# ------------------------------------------------------------------------------------------------
# SAVE DATA FUNCTION # ------------------------------------------------------------------------------------------------
def save_data(query, params):
    """
    Saves data to the database.
    """
    try:
        with engine.connect() as conn:
            # Use the `execute` method with text to support named parameters
            from sqlalchemy.sql import text
            conn.execute(text(query), params)
            st.success("Data saved successfully!")
    except Exception as e:
        st.error(f"Failed to save data: {e}")
# ------------------------------------------------------------------------------------------------
# LOGO FUNCTION # -------------------------------------------------------------------------------------
def display_logo():
    st.image("RRLOGOBANNER.png")
# LOGO SIDEBAR # ------------------------------------------------------------------------------------------------
# Add a smaller logo to the sidebar
st.sidebar.image(
    "RRLOGOSMALL.png")
# LOGO FOOTER # --------------------------------------------------------------------------------------------------
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
# TUTORIAL FUNCTION # ------------------------------------------------------------------------------------------------
def tutorial():
    """
    Provides a step-by-step accident reporting tutorial.
    """
    # Initialize session state to track the current step
    if "current_step" not in st.session_state:
        st.session_state.current_step = 0
    steps = [
        "First determine if anyone is injured.",
        "Ask for the basic vehicle information before taking a statement from the driver.",
        "Once a statement is obtained, determine if this is an accident or an incident.",
        "Ask for pictures of all vehicles involved from all four sides from a wide angle.",
        "Obtain other motorists' contact and insurance information.",
        "If police are involved, determine if a citation has been issued.",
        "If a citation has been issued, proceed with the post-accident testing SOP.",
        "If any injuries are sustained, determine if EMS will transport anyone from the scene. If so, where are they being transported?",
        "If a tow is required, determine if the vehicle is disabled. If it is being towed, obtain the tow company information.",
    ]
    st.header("Accident Reporting SOP Tutorial")
    # Show the current step
    if st.session_state.current_step < len(steps):
        step = steps[st.session_state.current_step]
        st.markdown(f"**Step {st.session_state.current_step + 1}: {step}**")
        # Button to proceed to the next step
        if st.button("Next", key="next_step"):
            st.session_state.current_step += 1
    else:
        st.success("Tutorial Complete!")
        if st.button("Restart Tutorial"):
            st.session_state.current_step = 0
# ------------------------------------------------------------------------------------------------
# LOGS #-------------------------------------------------------------------------------------------------------
import logging

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
# PROGRAM LOGIC FUNCTIONS AND UTILITY #-------------------------------------------------------------------------------------------------------
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
# INPUT WITH DEFAULT FUNCTION # ------------------------------------------------------------------------------------------------
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
# NUMERIC INPUT WITH DEFAULT FUNCTION ------------------------------------------------------------------------------------------------
# def numeric_input_with_default(label):
#     return numeric_input_with_default(label)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ACCIDENT REPORT DATA COLLECTION FUNCTIONS # ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# PERSON REPORTING FUNCTION # ------------------------------------------------------------------------------------------------
def collect_person_reporting_details(num_entries):
    """
    Collects details for multiple people reporting an incident.
    Args:
        num_entries (int): Number of people reporting.
    Returns:
        list: A list of dictionaries with reporting details.
    """
    details = []
    for i in range(num_entries):
        st.subheader(f"Person {i + 1}")
        name = text_input_with_default(f"Enter name of person reporting:", key=f"reporting_name_{i}")
        contact = text_input_with_default(f"Enter contact info for person reporting:", key=f"reporting_contact_{i}")
        details.append({"name": name, "contact": contact})
    return details
# ------------------------------------------------------------------------------------------------
# LOAD INFO FUNCTION # ------------------------------------------------------------------------------------------------
import uuid

def load_information():
    """
    Collects load-specific information for the accident report.
    """
    st.subheader("Load Information")
    
    # Unique prefix for all keys in this function
    prefix = "load_info"
    # Basic load details
    manifest_number = text_input_with_default("Manifest Number:", key=f"{prefix}_manifest_number_{uuid.uuid4()}")
    origin = text_input_with_default("Load Origin:", key=f"{prefix}_origin_{uuid.uuid4()}")
    destination = text_input_with_default("Load Destination:", key=f"{prefix}_destination_{uuid.uuid4()}")
    
    # Hazardous material details
    hazmat = get_yes_no("Does this involve hazardous materials (HAZMAT)?:", base_key=f"{prefix}_hazmat_status")
    hazmat_description = None
    if hazmat:
        hazmat_description = text_input_with_default(
            "Provide a brief description of the hazmat situation:", 
            key=f"{prefix}_hazmat_description_{uuid.uuid4()}"
        )
    
    # Load failure details
    failure = get_yes_no("Did the load fail in any way?:", base_key=f"{prefix}_failure_status")
    extent_of_failure = None
    if failure:
        extent_of_failure = text_input_with_default(
            "Describe the extent of the failure:", 
            key=f"{prefix}_extent_of_failure_{uuid.uuid4()}"
        )
    
    # Freight spill or damage
    freight_spill_or_damage = get_yes_no("Was there freight spillage or damage as a result of the accident?:", base_key=f"{prefix}_freight_spill_damage")
    
    # Additional load information
    load_weight = st.number_input(
        "Enter load weight (in lbs):", 
        min_value=0, 
        value=0, 
        key=f"{prefix}_load_weight_{uuid.uuid4()}"
    )
    load_type = st.selectbox(
        "Select load type:", 
        ["General Freight", "Household Goods", "Chemicals", "Other"],
        key=f"{prefix}_load_type_{uuid.uuid4()}"
    )
    
    # Return structured data
    return {
        "manifest_number": manifest_number,
        "origin": origin,
        "destination": destination,
        "hazmat": hazmat,
        "hazmat_description": hazmat_description,
        "failure": failure,
        "extent_of_failure": extent_of_failure,
        "freight_spill_or_damage": freight_spill_or_damage,
        "load_weight": load_weight,
        "load_type": load_type
    }
# ------------------------------------------------------------------------------------------------
# TOW INFO FUNCTION # ------------------------------------------------------------------------------------------------
def get_tow_information():
    """
    Collects information about tow services using Streamlit.
    Returns a dictionary with tow-related data.
    """
    prefix = "tow_info"
    st.subheader("Tow Information")
    tow_data = {}
    # Ask if tow is required
    tow_required = st.radio("Is a tow service required?", ["Yes", "No"], index=1)
    tow_data["tow_required"] = tow_required == "Yes"
    # Show additional fields if tow is required
    if tow_data["tow_required"]:
        tow_data["tow_disabling"] = st.radio("Is one or more vehicles disabled?", ["Yes", "No"], index=1) == "Yes"
        tow_data["tow_company_name"] = text_input_with_default("Enter the tow company's name:", key=f"{prefix}_tow_company_name_{uuid.uuid4()}")
        tow_data["tow_company_phone"] = text_input_with_default("Enter the tow company's phone number:", key=f"{prefix}_tow_phone_{uuid.uuid4()}")
        tow_data["tow_company_address"] = st.text_area("Enter the tow yard address:")
    else:
        tow_data.update({
            "tow_disabling": None,
            "tow_company_name": None,
            "tow_company_phone": None,
            "tow_company_address": None,
        })
    return tow_data
# ------------------------------------------------------------------------------------------------
# POLICE INFORMATION FUNCTION # ------------------------------------------------------------------------------------------------
def get_police_information():
    """
    Collects information about police involvement in the accident.
    Returns a dictionary with police-related data.
    """
    prefix = "police_info"
    st.subheader("Police Information")
    police_data = {}
    # Ask if police were involved
    police_involvement = st.radio("Police involved?", ["Yes", "No"], index=1)
    police_data["police_involvement"] = police_involvement == "Yes"
    # Show additional fields if police were involved
    if police_data["police_involvement"]:
        police_data["police_department"] = text_input_with_default("Enter the name of the police department:", key=f"{prefix}_police_department_{uuid.uuid4()}")
        police_data["police_officer"] = text_input_with_default("Enter the officer's name:", key=f"{prefix}_officer_name_{uuid.uuid4()}")
        police_data["police_badge"] = text_input_with_default("Enter the badge number:", key=f"{prefix}_badge_number_{uuid.uuid4()}")
        police_data["police_report"] = text_input_with_default("Enter the police report or case number:", key=f"{prefix}_case_number_{uuid.uuid4()}")
    else:
        police_data.update({
            "police_department": None,
            "police_officer": None,
            "police_badge": None,
            "police_report": None,
        })
    return police_data
# ------------------------------------------------------------------------------------------------
# GET OR CREATE DRIVER FUNCTION - DB OPERATIONS # ----------------------------------------------------------------------------
def get_or_create_driver(name, phone, license_number, license_expiry):
    """
    Retrieves a driver from the database if they exist or creates a new one.
    Returns the driver's database ID.
    """
    try:
        with engine.connect() as conn:
            # Check if the driver already exists
            query_check = text("""
                SELECT driver_id FROM drivers
                WHERE name = :name AND (phone_number = :phone OR phone_number IS NULL)
            """)
            result = conn.execute(query_check, {"name": name, "phone": phone}).fetchone()
            
            if result:
                st.info("Driver found in database.")
                return result[0]  # Return existing driver ID
            
            # Insert a new driver if not found
            query_insert = text("""
                INSERT INTO drivers (name, phone_number, license_number, license_expiry)
                VALUES (:name, :phone, :license_number, :license_expiry)
                RETURNING driver_id
            """)
            result = conn.execute(query_insert, {
                "name": name,
                "phone": phone,
                "license_number": license_number,
                "license_expiry": license_expiry
            }).fetchone()
            
            st.success("New driver created successfully.")
            return result[0]  # Return new driver ID
    except Exception as e:
        st.error(f"Error in get_or_create_driver: {e}")
        return None
# ------------------------------------------------------------------------------------------------        
# V1 DRIVER INFO FUNCTION # ------------------------------------------------------------------------------------------------
def get_driver():
    """
    Collects or retrieves driver details and ensures the driver exists in the database.
    Allows optional skipping of license information and ensures driver creation.
    """
    prefix = "driver_lookup"
    st.subheader("Enter Driver Details")
    
    # Collect driver details
    driver_name = text_input_with_default("Driver name:", key=f"{prefix}_driver_name_{uuid.uuid4()}")
    driver_phone = text_input_with_default("Driver phone number:", key=f"{prefix}_driver_phone_{uuid.uuid4()}")
    license_number = text_input_with_default("Driver license number:", key=f"{prefix}_license_number_{uuid.uuid4()}")
    license_expiry = st.date_input("License expiry date:", key=f"{prefix}_license_date_expiry_{uuid.uuid4()}")
    
    # Handle driver injury only if driver_name is known
    if driver_name != "Unknown":
        driver_injury = st.radio(f"Is the driver injured?", options=["Yes", "No"], index=1)
        driver_injury = driver_injury == "Yes"
    else:
        driver_injury = False
        
    # Placeholder for database interaction
    driver_id = get_or_create_driver(driver_name, driver_phone, license_number, license_expiry)
    
    if not driver_id:
        st.error("Error: Could not retrieve or create driver.")
        return None
    
    # Return all collected driver details
    return {
        "driver_id": driver_id,
        "driver_name": driver_name,
        "driver_phone": driver_phone,
        "license_number": license_number,
        "license_expiry": license_expiry,
        "driver_injury": driver_injury,
    }
# ------------------------------------------------------------------------------------------------    
# GET OR CREATE VEHICLE FUNCTION - DB OPS # ------------------------------------------------------------------------------------------------  
def get_or_create_vehicle(plate_number, make, model, year, color):
    """
    Retrieves a vehicle from the database if it exists or creates a new one.
    Returns the vehicle's database ID.
    """
    try:
        # Use the engine to connect to the database
        with engine.connect() as conn:
            # Check if the vehicle already exists
            query_check = text("""
                SELECT vehicle_id FROM vehicles
                WHERE plate_number = :plate_number
            """)
            result = conn.execute(query_check, {"plate_number": plate_number}).fetchone()
            if result:
                st.info("Vehicle found in database.")
                return result[0]  # Return existing vehicle ID
            
            # Insert a new vehicle if not found
            query_insert = text("""
                INSERT INTO vehicles (plate_number, make, model, year, color)
                VALUES (:plate_number, :make, :model, :year, :color)
                RETURNING vehicle_id
            """)
            result = conn.execute(query_insert, {
                "plate_number": plate_number,
                "make": make,
                "model": model,
                "year": year,
                "color": color
            }).fetchone()
            st.success("New vehicle created successfully.")
            return result[0]  # Return new vehicle ID
    except Exception as e:
        st.error(f"Error in get_or_create_vehicle: {e}")
        return None
# ------------------------------------------------------------------------------------------------
# V1 VEHICLE INFO FUNCTION # ------------------------------------------------------------------------------------------------
def get_vehicle():
    """
    Collects or retrieves vehicle details and ensures the vehicle exists in the database.
    """
    st.subheader("Vehicle Information")
    
    # Collect vehicle details
    plate_number = st.text_input("License plate number:", placeholder="Enter license plate number")
    make = st.text_input("Vehicle make:", placeholder="Enter vehicle make")
    model = st.text_input("Vehicle model:", placeholder="Enter vehicle model")
    year = st.number_input("Vehicle year:", min_value=0000, max_value=2100, step=1, format="%d")
    color = st.text_input("Vehicle color:", placeholder="Enter vehicle color")
    
    # # Attempt to retrieve or create the vehicle in the database
    vehicle_id = get_or_create_vehicle(plate_number, make, model, year, color)
    if not vehicle_id:
        st.error("Error: Could not retrieve or create vehicle.")
        return None
    
    # Return collected and processed vehicle details
    return {
        "vehicle_id": vehicle_id,
        "plate_number": plate_number,
        "make": make,
        "model": model,
        "year": int(year) if year else None,
        "color": color,
    }
# ------------------------------------------------------------------------------------------------
# COMPANY DETAILS FUNCTION # ------------------------------------------------------------------------------------------------
def get_company_info():
    """
    Collects company or division information.
    """
    prefix = "company_info"
    st.subheader("Company Information")
    is_saf = get_yes_no("Is this an SAF (Somewhere Air Freight) accident?", base_key=f"{prefix}_is_saf_{uuid.uuid4()}")
    
    if is_saf:
        saf_branch = st.selectbox(
            "Select the SAF branch:",
            ["SAF", "IQT", "CLP", "INMO"],
            key=f"{prefix}_saf_branch_{uuid.uuid4()}"
        )
        return {"is_saf": True, "saf_branch": saf_branch}
    else:
        carrier = text_input_with_default(
            "Enter the brokered third-party carrier:", key=f"{prefix}_third_party_carrier_{uuid.uuid4()}"
        )
        return {"is_saf": False, "carrier": carrier}
# ------------------------------------------------------------------------------------------------
# TRAILER INFO FUNCTION # ------------------------------------------------------------------------------------------------
def get_trailer() -> dict:
    """
    Collects information about the trailer if connected.
    Returns:
        dict: A dictionary containing trailer connection status and details if connected.
    """
    prefix = "trailer_info"
    st.subheader("Trailer Information")
    trailer_connected = get_yes_no("Is a trailer connected? (y/n):", base_key=f"{prefix}_trailer_connected")
    if trailer_connected:
        trailer_type = st.selectbox("Trailer Type", ['Dry Van', 'Refrigerated', 'Bobtail/None'], key=f"{prefix}_trailer_type_{uuid.uuid4()}")
        trailer_number = text_input_with_default("Enter the trailer number:", key=f"{prefix}_trailer_number_{uuid.uuid4()}").upper().strip()
        
        # Validation
        if not trailer_number:
            st.warning("Trailer number cannot be empty!")
            return {"trailer_connected": trailer_connected}
        
        return {
            "trailer_connected": trailer_connected,
            "trailer_type": trailer_type,
            "trailer_number": trailer_number,
        }
    return {"trailer_connected": False}
# --------------------------------------------------------------------------------------------------
# POST-ACCIDENT-TESTING FUNCTION # ------------------------------------------------------------------------------------------------
def post_accident_testing():
    """
    Evaluates the need for post-accident alcohol and drug testing based on regulatory criteria.
    """
    prefix = "post_accident_testing"
    st.subheader("Post-Accident Alcohol and Drug Testing Criteria")
    # Check for fatality
    fatality = get_yes_no("Was there a fatality as a result of the accident?:", base_key=f"{prefix}_is_fatality")
    if fatality:
        st.success("Testing Required due to a fatality.")
        return {"fatality": True, "testing_required": True}
    # Check for disabling tow or transported injury
    disabling_tow = get_yes_no("Did any vehicle sustain disabling damage requiring it to be towed?:", base_key=f"{prefix}_disabling_tow")
    transported_injury = get_yes_no("Was anyone transported for immediate medical treatment away from the scene?:", base_key=f"{prefix}_transported_injuries")
    # If disabling tow or transported injury, check for citation
    if disabling_tow or transported_injury:
        citation = get_yes_no("Was V1 issued a citation? (y/n): ", base_key=f"{prefix}_citation_issued")
        if citation:
            st.success("Testing Required due to disabling tow or transported injury with citation.")
            return {
                "fatality": False,
                "disabling_tow": disabling_tow,
                "transported_injury": transported_injury,
                "citation": True,
                "testing_required": True
            }
    # No testing required
    st.info("No Testing Required.")
    return {
        "fatality": False,
        "disabling_tow": disabling_tow,
        "transported_injury": transported_injury,
        "citation": False,
        "testing_required": False
    }
# ------------------------------------------------------------------------------------------------
# POST-ACCIDENT-TESTING TIMELINE FUNCTION # ------------------------------------------------------------------------------------------------
def post_accident_testing_timeline():
    """
    Collects details about the post-accident testing timeline and status.
    Returns a structured dictionary of user inputs.
    """
    prefix = "post_accident_timeline"
    st.subheader("Post-Accident Testing Timeline")
    # Steps to initiate the test
    steps_to_initiate_test = text_input_with_default(
        "Describe steps taken to initiate post-accident testing:", key=f"{prefix}_test_steps_{uuid.uuid4()}"
    )
    # Reason if no test can be done
    test_cannot_be_done = text_input_with_default(
        "If no test can be done, document the reason here:", key=f"{prefix}_cannot_test_{uuid.uuid4()}"
    )
    # Drug test completion status
    drug_test_completed = get_yes_no("Was the drug test completed?", base_key=f"{prefix}_drug_test_complete")
    # Alcohol test within 2 hours
    bat_within_2_hours = get_yes_no("Was the alcohol test attempted within 2 hours?", base_key=f"{prefix}_bat_2_hours")
    # Alcohol test completion status
    alcohol_test_completed = get_yes_no("Was the alcohol test completed?", base_key=f"{prefix}_bat_complete")
    # Return structured dictionary with all responses
    result = {
        "steps_to_initiate_test": steps_to_initiate_test,
        "test_cannot_be_done": test_cannot_be_done,
        "drug_test_completed": drug_test_completed,
        "bat_within_2_hours": bat_within_2_hours,
        "alcohol_test_completed": alcohol_test_completed,
    }
    # Display the summary for user review
    st.subheader("Summary of Post-Accident Testing Timeline")
    st.json(result)  # Nicely formatted display of the dictionary
    return result
# ------------------------------------------------------------------------------------------------
# CITATION FUNCTION # ------------------------------------------------------------------------------------------------
def citation_info():
    """
    Collects details about a citation issued during the accident.
    Returns a dictionary containing citation-related information.
    """
    prefix = "citation_info"
    st.subheader("Citation Information")
    
    # Check if a citation was issued
    citation_issued = get_yes_no("Was the driver issued a citation?", base_key=f"{prefix}_was_citation_issued")
    
    if citation_issued:
        st.info("Collecting citation details...")
        
        # Collect citation details
        citation_issued_date = st.date_input("Input date citation was issued (YYYY-MM-DD):", key=f"{prefix}_citation_date_{uuid.uuid4()}")
        citation_issued_time = st.time_input("Input time citation was issued (HH:MM):", key=f"{prefix}_citation_time_{uuid.uuid4()}")
        citation_description = text_input_with_default("Describe the offense:", key=f"{prefix}_citation_description_{uuid.uuid4}")
        
        # Return the collected data
        return {
            "citation_issued": True,
            "citation_issued_date": citation_issued_date,
            "citation_issued_time": citation_issued_time,
            "citation_description": citation_description,
        }
        
    # When no citation is issued
    st.info("No citation issued. Skipping citation details.")
    return {
        "citation_issued": False
    }
# ------------------------------------------------------------------------------------------------
# DOT RECORDABLE FUNCTION # ------------------------------------------------------------------------------------------------
def dot_recordable():
    """
    Evaluates whether an accident meets the criteria for being DOT recordable.
    """
    prefix = "dot_recordable_info"
    st.subheader("DOT Recordable Accident Criteria")
    public_roadway = get_yes_no("Did the accident occur on a roadway accessible to the public?", base_key=f"{prefix}_public_roadway")
    cmv_involved = get_yes_no("Did the accident involve a CMV?", base_key=f"{prefix}_cmv_involvement")
    fatality = get_yes_no("Did the accident result in a fatality?", base_key=f"{prefix}_fatality_status")
    transported_injury = get_yes_no("Was anyone transported for immediate medical treatment?", base_key=f"{prefix}_transported_injury")
    disabling_tow = get_yes_no("Did the accident involve disabling damage requiring a tow?", base_key=f"{prefix}_is_disabling_tow")
    
    dot_recordable = fatality or (cmv_involved and (transported_injury or disabling_tow))
    
    if dot_recordable:
        st.success("This accident is DOT recordable.")
    else:
        st.info("This accident does not meet the criteria for being DOT recordable.")
        
    return {
        "public_roadway": public_roadway,
        "cmv_involved": cmv_involved,
        "fatality": fatality,
        "transported_injury": transported_injury,
        "disabling_tow": disabling_tow,
        "dot_recordable": dot_recordable
    }
    
# ------------------------------------------------------------------------------------------------
# INJURY INFO # ------------------------------------------------------------------------------------------------
def injury_details():
    """
    Collects details about injuries sustained in the accident.
    """
    prefix = "injury_details"
    st.subheader("Injury Details")
    injury_occurred = get_yes_no("Were there any injuries?", base_key=f"{prefix}_any_injuries_reported")
    
    if injury_occurred:
        injury_description = st.text_area("Describe the injuries sustained:")
        hospital = get_yes_no("Was anyone transported to a hospital?", base_key=f"{prefix}_hospital_needed")
        hospital_name = text_input_with_default("Enter the hospital name:", key=f"{prefix}_hospital_name_{uuid.uuid4()}") if hospital else "N/A"
        
        return {
            "injury_occurred": True,
            "injury_description": injury_description,
            "hospital": hospital,
            "hospital_name": hospital_name
        }
    return {
        "injury_occurred": False,
        "injury_description": None,
        "hospital": False,
        "hospital_name": None
    }
# ------------------------------------------------------------------------------------------------
# FOLLOW-UP FUNCTION # ------------------------------------------------------------------------------------------------
def followup_needed():
    """
    Determines whether follow-up actions are required based on the preventability of the event.
    """
    prefix = "follow_up_needed"
    st.subheader("Follow-Up Required?")
    
    # Check if the accident or incident was preventable
    preventable_accident = get_yes_no("Was the accident preventable?:", base_key=f"{prefix}_was_preventable_accident")
    
    if preventable_accident:
        st.warning("Follow-up is required for all preventable accidents or incidents.")
        return {"followup_needed": True, "preventable": True}
    else:
        st.success("No follow-up is required for non-preventable accidents or incidents.")
        return {"followup_needed": False, "preventable": False}
# ------------------------------------------------------------------------------------------------
# ACCIDENT OR INCIDENT FUNCTION # ------------------------------------------------------------------------------------------------
def accident_or_incident():
    """
    Determines whether the event is classified as an accident or incident.
    """
    prefix = "choose_accident_or_incident"
    st.subheader("Accident or Incident Classification")
    
    # Allow selection between accident or incident
    classification_type = st.radio(
        "Classify this event:",
        options=["Accident", "Incident"],
        key=f"{prefix}_classification_type_{uuid.uuid4()}"
    )
    
    if classification_type == "Accident":
        accident_details = {
            "classification": "Accident",
            "description": text_input_with_default("Describe the accident:", key=f"{prefix}_accident_description_{uuid.uuid4()}"),
            "type": st.selectbox(
                "Select the type of accident:",
                ["Collision", "Roll-over", "Rear-end", "Head-on", "Side-swipe"],
                key=f"{prefix}_accident_type_{uuid.uuid4()}")
        }
        return accident_details
    
    elif classification_type == "Incident":
        incident_details = {
            "classification": "Incident",
            "description": text_input_with_default("Describe the incident:", key=f"{prefix}_incident_description_{uuid.uuid4()}"),
            "type": st.selectbox(
                "Select the type of incident:",
                ["Stationary Object", "Bollard", "Overhead Wires", "Wall", "Unavoidable Debris", "Avoidable Debris", "Animal Strike"],
                key=f"{prefix}_incident_type_{uuid.uuid4()}"
            )
        }
        return incident_details
# ------------------------------------------------------------------------------------------------
# CO DRIVER FUNCTION # ------------------------------------------------------------------------------------------------
def v1_codriver():
    prefix = "codriver"
    codriver_present = get_yes_no("Does V1 have a co-driver?:", base_key=f"{prefix}_codriver_yes")
    if codriver_present:
        codriver_name = text_input_with_default("Enter co-driver name:", key=f"{prefix}_codriver_name_{uuid.uuid4()}").strip()
        codriver_phone = text_input_with_default("Enter co-driver phone number:", key=f"{prefix}_codriver_phone_{uuid.uuid4()}").strip()
        codriver_injury = get_yes_no("Is the co-driver injured?:", base_key=f"{prefix}_codriver_injury")
        return {
            "codriver_present": codriver_present,
            "codriver_name": codriver_name,
            "codriver_phone": codriver_phone,
            "codriver_injury": codriver_injury,
        }
    return {"codriver_present": False}
# ------------------------------------------------------------------------------------------------
# V@ PASSENGER INFO FUNCTION # ------------------------------------------------------------------------------------------------
def get_v2_passengers():
    prefix = "v2_passenger_key"
    st.subheader("V2 Passenger Info")
    has_passengers = get_yes_no("Does V2 have passengers?:", base_key=f"{prefix}_v2_passengers")
    passengers = []
    if has_passengers:
        num_passengers = text_input_with_default("How many passengers are there?", key=f"{prefix}_num_passengers_{uuid.uuid4()}")
        try:
            num_passengers = text_input_with_default(num_passengers)
        except ValueError:
            num_passengers = 0
        for i in range(num_passengers):
            st.text(f"Passenger {i + 1}:")
            passenger_name = text_input_with_default("Enter passenger name", key=f"{prefix}_passenger_name_{uuid.uuid4()}")
            passenger_injury = get_yes_no("Is the passenger injured?", base_key=f"{prefix}_passenger_injury")
            passengers.append({"name": passenger_name, "injured": passenger_injury})
    return {"has_passengers": has_passengers, "passengers": passengers}
# ------------------------------------------------------------------------------------------------
# ADDITIONAL REMARKS FUNCTION # ------------------------------------------------------------------------------------------------
def get_additional_remarks():
    prefix = "additional_remarks"
    st.subheader("Additional Remarks")
    remarks = text_input_with_default("Enter any additional remarks or observations:", key=f"{prefix}_remarks_{uuid.uuid4()}").strip()
    return remarks if remarks else "No additional remarks provided."
# ------------------------------------------------------------------------------------------------
# USER ACCIDENT FORM # ------------------------------------------------------------------------------------------------
def accident_form():
    prefix = "accident_form_keys"
    """
    Displays the accident report form.
    """
    st.header("Accident Information")
    company_info = get_company_info()
    # company_info = st.text_input("Company Info:", key=f"{prefix}company_info_{uuid.uuid4()}")
    accident_date = st.date_input("Accident Date:", key=f"{prefix}_accident_date_{uuid.uuid4()}")
    accident_time = st.time_input("Accident Time:", key=f"{prefix}_accident_time_{uuid.uuid4()}")
    accident_location = st.text_input("Accident Location or Address:", key=f"{prefix}_accident_address_{uuid.uuid4()}")
    accident_description = st.text_area("Accident Description:")

    weather_info = st.selectbox("Weather Conditions:", ['Clear', 'Overcast', 'Rainy', 'Windy', 'Snowy'], key=f"{prefix}_accident_weather_{uuid.uuid4()}")
    road_conditions = st.selectbox("Road Conditions:", ['Dry', 'Wet', 'Icy', 'Snowy'], key=f"{prefix}_road_conditions_{uuid.uuid4()}")

    v1_driver = st.text_input("V1 Driver Name:", key=f"{prefix}_v1_driver_{uuid.uuid4()}")
    v1_vehicle = st.text_input("V1 Vehicle ID or License Plate:", key=f"{prefix}_v1_veh_info_{uuid.uuid4()}")

    v2_driver = st.text_input("V2 Driver Name:", key=f"{prefix}_v2_driver_{uuid.uuid4()}")
    v2_vehicle = st.text_input("V2 Vehicle ID or License Plate:", key=f"{prefix}_v2_veh_info_{uuid.uuid4()}")

    additional_remarks = get_additional_remarks()
    
    return {
        "company_info": company_info,
        "accident_date": accident_date,
        "accident_time": accident_time,
        "accident_location": accident_location,
        "accident_description": accident_description,
        "weather_info": weather_info,
        "road_conditions": road_conditions,
        "v1_driver": v1_driver,
        "v1_vehicle": v1_vehicle,
        "v2_driver": v2_driver,
        "v2_vehicle": v2_vehicle,
        "additional_remarks": additional_remarks
    }


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
# ------------------------------------------------------------------------------------------------
# VEHICLE LOOKUP PAGE # ------------------------------------------------------------------------------------------------
def vehicle_lookup():
    prefix = "vehicle_lookup"
    """
    Provides a UI for looking up vehicle information.
    """
    st.subheader("Vehicle Lookup")
    vehicle_id = text_input_with_default("Enter Vehicle ID or License Plate:", key=f"{prefix}_vehicle_id_{uuid.uuid4()}")
    
    if st.button("Search Vehicle"):
        query = """
        SELECT * FROM vehicles 
        WHERE vehicle_id = %s OR license_plate ILIKE %s
        """
        params = (vehicle_id, f"%{vehicle_id}%")
        vehicle_data = fetch_data(query, params)
        
        if not vehicle_data.empty:
            st.write(vehicle_data)
        else:
            st.warning("No vehicle found!")
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
# ------------------------------------------------------------------------------------------------
# MAIN FUNCTION FOR PROGRAM # ------------------------------------------------------------------------------------------------
def main():
    """
    Main function to render the Streamlit app.
    """
    display_logo()
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Home", "Accident Report Form", "Driver Lookup", "Vehicle Lookup", "Tutorial", "FLT Lookup"],
    )
    if page == "Home":
        st.title("Welcome to RiskRanger")
        st.write("Your safety management companion.")
    elif page == "Accident Report Form":
        st.title("Accident Report Form")
        # Collect data from various sections
        accident_data = accident_form()
        # tow_data = get_tow_information()
        load_info = load_information()
        police_info = get_police_information()
        tow_info = get_tow_information()
        vehicle1 = get_vehicle()
        driver1 = get_driver()
        num_people = st.number_input("Number of people reporting:", min_value=1, max_value=10, value=1, key="num_people")
        reporting_details = collect_person_reporting_details(num_people)
        classification = accident_or_incident()
        dot_info = dot_recordable()
        testing_result = post_accident_testing()
        followup_info = followup_needed()
        injury_info = injury_details()
        accident_or_incident_info = accident_or_incident()
        additional_remarks = get_additional_remarks
        # dot_info = dot_recordable()
        # Display gathered information
        st.write("Classification Result:", classification)
        st.write("Follow-Up Information:", followup_info)
        if dot_info["dot_recordable"]:
            st.write("DOT Recordable Accident Details:", dot_info)
        else:
            st.write("This accident is not DOT recordable.")
        if testing_result["testing_required"]:
            st.write("Testing Details:", testing_result)
        else:
            st.write("No testing required based on the criteria.")
        # Optional Sections
        if st.button("Start Post-Accident Testing Timeline"):
            timeline_data = post_accident_testing_timeline()
            st.write("Timeline Data Submitted:", timeline_data)
        if st.button("Add Citation Information"):
            citation_data = citation_info()
            st.write("Citation Data Collected:", citation_data)
        # Submit Data
        if st.button("Submit Accident Report"):
            st.write("Reporting Details:", reporting_details)
            st.write("Tow Information:", tow_info)
            st.write("Police Information:", police_info)
            st.write("Load Information:", load_info)
            st.write("DOT Recordable Info:", dot_info)
            st.write("Police Information:", police_info)
            st.write("Vehicle 1 Info:", vehicle1)
            st.write("Accident or Incident Info:", accident_or_incident_info)
            st.write("Injury Details:", injury_info)
            st.write("Driver 1 Info:", driver1)
            st.write("Accident Classification:", classification)
            st.write("Additional Remarks:", additional_remarks)
            
            query = """
                INSERT INTO accident_reports (
                    company_info, accident_date, accident_time,
                    accident_location, accident_description, weather_info, road_conditions,
                    v1_driver, v1_vehicle, v2_driver, v2_vehicle,
                    injury_occurred, injury_description, hospital, hospital_name,
                    accident_type, incident_type
                ) VALUES (
                    :company_info, :accident_date, :accident_time,
                    :accident_location, :accident_description, :weather_info, :road_conditions,
                    :v1_driver, :v1_vehicle, :v2_driver, :v2_vehicle,
                    :injury_occurred, :injury_description, :hospital, :hospital_name,
                    :accident_type, :incident_type
                )
            """
            
            params = {
                "company_info": accident_data.get("company_info", ""),
                "accident_date": accident_data.get("accident_date").strftime('%Y-%m-%d'),
                "accident_time": accident_data.get("accident_time").strftime('%H:%M:%S'),
                "accident_location": accident_data.get("accident_location", ""),
                "accident_description": accident_data.get("accident_description", ""),
                "weather_info": accident_data.get("weather_info", ""),
                "road_conditions": accident_data.get("road_conditions", ""),
                "v1_driver": accident_data.get("v1_driver", ""),
                "v1_vehicle": accident_data.get("v1_vehicle", ""),
                "v2_driver": accident_data.get("v2_driver", ""),
                "v2_vehicle": accident_data.get("v2_vehicle", ""),
                "injury_occurred": injury_info.get("injury_occurred", False),
                "injury_description": injury_info.get("injury_description", ""),
                "hospital": injury_info.get("hospital", False),
                "hospital_name": injury_info.get("hospital_name", ""),
                "accident_type": accident_or_incident_info.get("accident_type", ""),
                "incident_type": accident_or_incident_info.get("incident_type", ""),
            }
            
            save_data(query, params)
            
    elif page == "Driver Lookup":
        driver_lookup()
    elif page == "Vehicle Lookup":
        vehicle_lookup()
    elif page == "FLT Lookup":
        flt_lookup()  # Ensure this function is implemented
    elif page == "Tutorial":
        tutorial()
        
if __name__ == "__main__":
    main()
# ------------------------------------------------------------------------------------------------