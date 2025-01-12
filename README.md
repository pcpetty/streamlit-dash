# **Risk Ranger: A Streamlit-Based Accident Reporting and Management System**

![Risk Ranger Logo](assets/RRLOGOSMALL.png)

## **Overview**
**Risk Ranger** is a comprehensive web-based accident reporting and management system built with Streamlit. It integrates seamlessly with PostgreSQL to provide a robust backend, modular utility functions, and a streamlined user experience for safety management professionals. This project combines technical proficiency, creativity, and problem-solving skills to tackle real-world challenges in accident reporting and claims management.

Designed as a **capstone project**, Risk Ranger serves as both a testament to my learning journey and a practical application of data engineering, software development, and UI/UX design principles. It reflects my passion for problem-solving, my commitment to building professional-grade solutions, and my readiness to transition into a data engineering or software development role.

---

## **Project Features**
- **Role-Based Access Control**:
  - Superusers can manage users and oversee system operations.
  - Safety Generalists can create and edit accident reports.
  - Liability Adjusters can manage claims and financial records.

- **Comprehensive Accident Reporting**:
  - Modular accident report form with sections for driver, vehicle, towing, police, and DOT compliance data.
  - Dynamic data validation and submission to a PostgreSQL database.
  - Generated FLT numbers to uniquely identify accident reports.

- **Advanced Lookups**:
  - Driver, vehicle, and FLT lookups with query capabilities for quick data retrieval.

- **Photo and Document Uploads**:
  - Upload accident photos or supporting documents.
  - Photos stored locally and linked in the PostgreSQL database.

- **PDF Report Generation**:
  - Export accident reports to professionally formatted PDF files for easy sharing and archiving.

- **Interactive Tutorial**:
  - Step-by-step accident reporting guide to educate users on the workflow and processes.

- **Streamlined UI/UX**:
  - Modular design for scalability and maintainability.
  - Role-specific dashboards tailored for each user group.

---

## **Goals and Objectives**
### **Project Goals**
- Develop a real-world solution for accident reporting that integrates backend, frontend, and database engineering.
- Demonstrate my ability to tackle complex problems and deliver functional, user-friendly applications.
- Showcase modular, clean, and maintainable code adhering to best practices.
- Learn and apply concepts such as:
  - Role-based authentication.
  - Advanced SQL queries and database design.
  - Streamlit UI design and optimization.
  - File handling, PDF generation, and API integration.

### **Personal Goals**
- Push the boundaries of my self-taught journey into data engineering and software development.
- Build a **capstone project** that highlights my passion, grit, and readiness to excel in a technical role.
- Provide a tangible, working example of my abilities to potential recruiters.

---

## **Learning and Struggles**
The journey to build Risk Ranger has been challenging yet rewarding. Here are some key takeaways:
- **Database Mastery**: Designing and optimizing a PostgreSQL database to handle real-world data flows.
- **Role-Based Access Control**: Implementing session state management to secure and personalize user experiences.
- **Error Handling and Robustness**: Ensuring the application handles edge cases gracefully.
- **Streamlit Framework**: Leveraging Streamlit’s power to create an intuitive and dynamic web app.
- **Modularity and Clean Code**: Refactoring over 1,000 lines of code into manageable modules for better maintainability.
- **Persistence Through Challenges**:
  - Debugging complex database integrations.
  - Managing state across pages in a multi-user application.
  - Balancing functionality with performance and design.

---

## **Why Risk Ranger Matters**
This project is more than just an app. It represents:
- **Dedication**: Hundreds of hours spent learning, debugging, and perfecting the application.
- **Growth**: A tangible measure of how far I’ve come in my self-taught programming journey.
- **Impact**: The ability to streamline safety processes and improve accident management workflows.
- **Potential**: A showcase of what I can bring to your team—problem-solving skills, technical expertise, and a relentless drive to deliver.

---

## **Technical Highlights**
- **Languages**: Python, SQL
- **Frameworks**: Streamlit
- **Database**: PostgreSQL
- **Libraries**: SQLAlchemy, FPDF, Pandas, OpenPyxl, Psycopg2, Colorama
- **Environment Management**: Python Virtual Environment
- **Version Control**: Git and GitHub

---

## **Challenges Overcome**
1. **Session State Management**:
   - Seamlessly transitioning between pages while maintaining user authentication and form state.
2. **Error Handling**:
   - Writing robust try-except blocks to ensure graceful failure recovery.
3. **PDF Generation**:
   - Dynamically creating structured reports with FPDF to meet professional standards.
4. **Photo and Document Handling**:
   - Securely uploading and associating media files with database records.

---

## **Next Steps**
1. **Enhancements**:
   - Add edit and delete functionality for reports, users, and claims.
   - Implement advanced admin tracking for accountability.
   - Enhance data visualizations using Streamlit's plotting libraries.

2. **Optimization**:
   - Improve database query performance.
   - Optimize the UI for mobile and tablet users.

3. **Deployment**:
   - Deploy Risk Ranger to a cloud environment for public access and scalability.

---

## **Call to Action**
I’m eager to bring this level of dedication, innovation, and problem-solving to your organization. 

### **Why Hire Me?**
- I’ve built Risk Ranger from the ground up—managing every aspect from database design to UI implementation.
- My learning journey is a testament to my ability to adapt, grow, and tackle new challenges head-on.
- I’m not just passionate about coding—I’m passionate about creating impactful solutions.

---

## **How You Can Help**
- Let’s discuss how my skills align with your team’s needs.
- Explore Risk Ranger live (or in a demo session).
- Reach out to me for a coffee chat—I’d love to share more about this journey!

---

## **Contact**
- **Email**: [colepetty57@gmail.com](mailto:colepetty57@gmail.com])
- **GitHub**: [pcpetty](https://github.com/pcpetty)
- **LinkedIn**: [Cole Petty](https://linkedin.com/in/cole-petty-095027121)

Let’s build something great together!


# Project Structure
risk_ranger/                 # Parent folder / directory
├── app.py                   # Main entry point
├── pages/                   # Individual page modules
│   ├── login.py             # Login logic
│   ├── admin.py             # Admin dashboard
│   ├── home.py              # Landing page
│   ├── accident_reports.py  # Accident report form
│   ├── driver_lookup.py     # Driver lookup
│   ├── vehicle_lookup.py    # Vehicle lookup
│   ├── flt_lookup.py        # FLT lookup
│   ├── upload_photos.py     # Upload photo functionality
│   ├── tutorial.py          # Accident reporting tutorial
│   ├── safety_generalist.py # Safety Generalist dashboard
│   └── liability_adjuster.py# Liability Adjuster dashboard
├── utils/                   # Utility functions
│   ├── database.py          # All database-related logic
│   ├── pdf_generator.py     # PDF generation
│   ├── session_state.py     # Session state logic
│   ├── accident_helpers.py  # Accident report helpers
│   └── helpers.py           # General helper functions
├── static/                  # Static files (e.g., images, CSS)
│   └── uploads/             # Handles photo uploads to website and psql database
├── templates/               # PDF templates or HTML templates
├── README.md                # Documentation
├── .env                     # Database environment variables
├── .gitignore               # Gitignore for venv
├── requirements.txt         # Required libraries and modules
├── LICENSE.md               # Licensing and use
└── SECURITY.md              # Security guidelines

    Core Functions:
        - Database connections and queries (e.g., db_connect, fetch_data, save_data, get_or_create_driver).
        - Authentication (e.g., authenticate_user, add_user).

    Page-Specific Features:
        - Accident Report Form (accident_form, get_company_info, get_driver, etc.).
        - Home page (landing and welcome)
        - Login page (login / create profile)
        - Tutorial page (learn how to use reporting system)
        - Upload photos (upload accident photos and documents)
        - Driver Lookup (driver_lookup).
        - Vehicle Lookup (vehicle_lookup).
        - FLT Lookup (flt_lookup).

    Shared Utilities
        Input helpers (text_input_with_default, get_yes_no).
        Logging (log_all_keys).
        Tutorial steps.
        Session state
        PDF generation

    UI Components
        Navigation (sidebar and top-level navigation).
        Page templates (e.g., logo, footer).
        Modular forms (e.g., load_information, get_tow_information, etc.).

1. Main Entry File (app.py)

This will be the central point of execution, responsible for:

    Initializing Streamlit.
    Rendering the sidebar navigation.
    Routing to different pages.

2. Page-Specific Modules (pages/)

Each page (e.g., Accident Report, Driver Lookup, etc.) will have its own file under the pages/ directory. For example:

    pages/accident_reports.py for accident-related functionalities.
    pages/driver_lookup.py for driver lookup.
    pages/tutorial.py for the tutorial page.

3. Database Operations Module (utils/db.py)

Centralized database-related operations like db_connect, fetch_data, save_data.
4. Utility Module (utils/helpers.py)

For shared helper functions like text_input_with_default, get_yes_no, log_all_keys.
5. Assets and Static Files

    Images, logos, and other assets in a directory like assets/.
    Templates for PDF reports, if needed.

6. Session State Management

Centralized session state operations, ensuring consistency across pages.
