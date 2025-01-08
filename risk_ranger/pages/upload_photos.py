# Libraries and Modules
import streamlit as st
import os
from utils.pdf_generator import upload_photo_to_database
from utils.database import db_connect
# ------------------------------------------------------------------------------------------------
# Upload Photos
# ------------------------------------------------------------------------------------------------
def upload_photo():
    """
    Handles photo uploads, saving them locally, and uploading them to the database.
    """
    st.title("Upload Accident Photos")
    st.info("Upload photos related to the accident report. Supported formats: JPG, JPEG, PNG.")
    # Photo upload widget
    uploaded_photo = st.file_uploader("Choose a photo to upload:", type=["jpg", "jpeg", "png"])
    # If a photo is uploaded
    if uploaded_photo is not None:
        # Preview the uploaded photo
        st.image(uploaded_photo, caption="Uploaded Photo", use_column_width=True)
        # Create a directory for storing photos if it doesn't exist
        photo_dir = "uploads/photos"
        os.makedirs(photo_dir, exist_ok=True)
        # Save the photo locally
        photo_path = os.path.join(photo_dir, uploaded_photo.name)
        try:
            with open(photo_path, "wb") as f:
                f.write(uploaded_photo.getbuffer())
            st.success(f"Photo saved locally at {photo_path}.")
        except Exception as e:
            st.error(f"Failed to save the photo: {e}")
            return
        # Upload the photo to the database
        if st.button("Upload to Database"):
            try:
                conn = db_connect()
                upload_photo_to_database(uploaded_photo, conn)
                st.success("Photo successfully uploaded to the database.")
            except Exception as e:
                st.error(f"Failed to upload the photo to the database: {e}")
    else:
        st.warning("Please upload a photo to continue.")