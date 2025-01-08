# -------------------------------------------------------------------------
import streamlit as st
# -------------------------------------------------------------------------
# Initialize session state for accident report fields
if "accident_report" not in st.session_state:
    st.session_state["accident_report"] = {
        "driver_name": "",
        "date": "",
        "location": "",
        "description": ""
    }
# Accident Report Form
st.text_input("Driver Name", key="driver_name", on_change=lambda: st.session_state["accident_report"].update({"driver_name": st.session_state.driver_name}))
st.date_input("Date of Accident", key="date", on_change=lambda: st.session_state["accident_report"].update({"date": str(st.session_state.date)}))
st.text_input("Location", key="location", on_change=lambda: st.session_state["accident_report"].update({"location": st.session_state.location}))
st.text_area("Description", key="description", on_change=lambda: st.session_state["accident_report"].update({"description": st.session_state.description}))
st.write("Current Accident Report Data:")
st.json(st.session_state["accident_report"])
# -------------------------------------------------------------------------
# Manage success message in session state
if "success_message" not in st.session_state:
    st.session_state["success_message"] = None
# Add a driver (simulated)
if st.button("Create Driver"):
    # Simulate driver creation logic
    st.session_state["success_message"] = "Driver successfully created!"
# Display the success message
if st.session_state["success_message"]:
    st.success(st.session_state["success_message"])
    if st.button("Dismiss"):
        st.session_state["success_message"] = None
# -------------------------------------------------------------------------
# Photo Upload
uploaded_photo = st.file_uploader("Upload Accident Photo", type=["jpg", "jpeg", "png"])
# Save uploaded photo in session state
if uploaded_photo is not None:
    st.session_state["uploaded_photo"] = uploaded_photo
    st.image(uploaded_photo, caption="Uploaded Photo", use_column_width=True)
# -------------------------------------------------------------------------
with open(f"photos/{uploaded_photo.name}", "wb") as f:
    f.write(uploaded_photo.getbuffer())
# -------------------------------------------------------------------------
from fpdf import FPDF
# Generate PDF Report
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    pdf.output("report.pdf")
    return "report.pdf"

if st.button("Download Report as PDF"):
    if "accident_report" in st.session_state:
        pdf_path = generate_pdf(st.session_state["accident_report"])
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="Download PDF",
                data=pdf_file,
                file_name="accident_report.pdf",
                mime="application/pdf"
            )
    else:
        st.error("No accident report data to generate PDF.")
# -------------------------------------------------------------------------

uploaded_file = st.file_uploader("Upload Accident Photo", type=["jpg", "png"])
if uploaded_file:
    file_path = f"uploads/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File saved to {file_path}")


with open("report.pdf", "rb") as f:
    st.download_button("Download PDF", f, file_name="accident_report.pdf", mime="application/pdf")


photo_path = f"uploads/{uploaded_photo.name}"
with open(photo_path, "wb") as f:
    f.write(uploaded_photo.getbuffer())
cur.execute("INSERT INTO accident_photos (report_id, photo_path) VALUES (%s, %s)", (report_id, photo_path))
