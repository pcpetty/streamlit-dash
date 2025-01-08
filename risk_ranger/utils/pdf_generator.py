# RISK RANGER STREAMLIT VERSION # ------------------------------------------------------------------------------------------------
# Import Libraries and Modules # ------------------------------------------------------------------------------------------------
import streamlit as st
import os
from fpdf import FPDF
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
from sqlalchemy import text
import logging
from utils.helpers import generate_flt_number_with_check
from psycopg2 import sql

# Configure logging
logging.basicConfig(level=logging.INFO)
# PDF Generation Function
def generate_pdf(data, output_dir="generated_reports"):
    """
    Generates a PDF report from a dictionary of data.
    Args:
        data (dict): Data to include in the PDF.
        output_dir (str): Directory to save the generated PDF.
    Returns:
        str: Path to the generated PDF.
    """
    try:
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        # Add data to the PDF
        for key, value in data.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
        # Save PDF
        pdf_path = os.path.join(output_dir, "accident_report.pdf")
        pdf.output(pdf_path)
        logging.info(f"PDF generated: {pdf_path}")
        return pdf_path
    except Exception as e:
        logging.error(f"Error generating PDF: {e}")
        st.error("Failed to generate PDF.")
        return None

# Streamlit PDF Download Function
def download_pdf_button():
    """
    Provides a button to download the generated PDF.
    """
    if "accident_report" in st.session_state:
        pdf_path = generate_pdf(st.session_state["accident_report"])
        if pdf_path:
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Download PDF",
                    data=pdf_file,
                    file_name="accident_report.pdf",
                    mime="application/pdf"
                )
        else:
            st.error("Failed to generate PDF.")
    else:
        st.error("No accident report data to generate PDF.")

# Photo Upload Function
def upload_photo_to_database(uploaded_photo, conn):
    """
    Uploads a photo to the database and associates it with an FLT number.
    Args:
        uploaded_photo: The uploaded photo file from Streamlit.
        conn: Database connection object.
    """
    if uploaded_photo is None:
        raise ValueError("No photo was uploaded.")
    try:
        # Save photo path and generate FLT number
        photo_path = f"uploads/photos/{uploaded_photo.name}"
        flt_number = generate_flt_number_with_check(conn)
        # Insert into database
        with conn.cursor() as cur:
            cur.execute(
                sql.SQL("INSERT INTO accident_photos (report_id, photo_path) VALUES (%s, %s)"),
                (flt_number, photo_path)
            )
            conn.commit()
        st.success(f"Photo successfully uploaded and associated with FLT Number: {flt_number}")
    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"Failed to upload photo to database: {e}")

# Streamlit Photo Uploader
def photo_uploader():
    """
    Streamlit component for uploading photos.
    """
    uploaded_file = st.file_uploader("Upload Accident Photo", type=["jpg", "png"])
    if uploaded_file:
        db_config = {
            "host": os.getenv("DB_HOST"),
            "database": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD")
        }
        upload_photo_to_database(uploaded_file, db_config)
