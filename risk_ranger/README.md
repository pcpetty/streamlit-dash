# Project Structure

risk_ranger/
│
├── app.py                  # Main entry point
├── pages/                  # Modular pages for Streamlit multipage apps
│   ├── home.py
│   ├── accident_report.py
│   ├── admin.py
│   └── upload_photos.py
├── utils/                  # Utility functions and helpers
│   ├── database.py         # DB connection, queries, etc.
│   ├── session_state.py    # Session state helpers
│   └── pdf_generator.py    # PDF generation code
├── static/                 # Static assets
│   └── uploads/            # Uploaded photos
├── templates/              # Template files for HTML or PDF
└── README.md               # Project documentation
