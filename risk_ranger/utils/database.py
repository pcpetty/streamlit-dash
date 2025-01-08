# Libraries and Modules
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import logging
import os
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
from psycopg2.extras import RealDictCursor
from psycopg2 import connect, Error
import pandas as pd
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Database configuration dictionary
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "risk_ranger"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT", 5432),
}

DATABASE_URL = os.getenv("DATABASE_URL")

# Validate environment variables
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set or loaded correctly.")

# SQLAlchemy Engine
engine = create_engine(DATABASE_URL)

# Database Connection (psycopg2)
def db_connect():
    try:
        conn = connect(**db_config)
        return conn
    except Error as e:
        logging.error(f"Database connection failed: {e}")
        return None
    
# ------------------------------------------------------------------------------------------------
# initialize_users_table ------------------------------------------------------------------------------------------------
def initialize_users_table():
    conn = db_connect()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            );
        """)
        cur.execute("SELECT COUNT(*) FROM users;")
        if cur.fetchone()[0] == 0:
            cur.execute(
                """
                INSERT INTO users (username, password, role)
                VALUES ('admin', crypt('superpassword', gen_salt('bf')), 'superuser');
                """
            )
        conn.commit()
        st.success("User table initialized successfully.")
    except Exception as e:
        st.error(f"Failed to initialize users table: {e}")
    finally:
        conn.close()

# User Authentication
def authenticate_user(username, password):
    conn = db_connect()
    if not conn:
        return None
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = """
            SELECT role FROM users 
            WHERE username = %s AND password = crypt(%s, password);
        """
        cur.execute(query, (username, password))
        result = cur.fetchone()
        return result["role"] if result else None
    except Exception as e:
        logging.error(f"Authentication failed: {e}")
        return None
    finally:
        conn.close()

# Add User
def add_user(username, password, role):
    conn = db_connect()
    if not conn:
        return
    try:
        cur = conn.cursor()
        query = """
            INSERT INTO users (username, password, role)
            VALUES (%s, crypt(%s, gen_salt('bf')), %s);
        """
        cur.execute(query, (username, password, role))
        conn.commit()
        logging.info(f"User {username} added successfully!")
    except Exception as e:
        logging.error(f"Failed to add user: {e}")
    finally:
        conn.close()

# Fetch All Users
def fetch_all_users():
    conn = db_connect()
    if not conn:
        return []
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id, username, role FROM users;")
        users = cur.fetchall()
        return users
    except Exception as e:
        logging.error(f"Failed to fetch users: {e}")
        return []
    finally:
        conn.close()

# Fetch Data
def fetch_data(query, params=None):
    try:
        with engine.connect() as conn:
            return pd.read_sql_query(query, conn, params=params)
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# Save Data
def save_data(query, params):
    try:
        with engine.connect() as conn:
            conn.execute(text(query), params)
            logging.info("Data saved successfully!")
    except Exception as e:
        logging.error(f"Failed to save data: {e}")

# Save Accident Report
def save_accident_report(report):
    query = """
        INSERT INTO accident_reports (
            company_info, accident_date, accident_time, accident_location,
            accident_description, weather_info, road_conditions,
            v1_driver, v1_vehicle, v2_driver, v2_vehicle, additional_remarks
        ) VALUES (
            :company_info, :accident_date, :accident_time, :accident_location,
            :accident_description, :weather_info, :road_conditions,
            :v1_driver, :v1_vehicle, :v2_driver, :v2_vehicle, :additional_remarks
        );
    """
    save_data(query, report)

# Fetch Accident Reports
def fetch_accident_reports():
    query = "SELECT * FROM accident_reports;"
    try:
        with engine.connect() as conn:
            return conn.execute(text(query)).fetchall()
    except Exception as e:
        logging.error(f"Failed to fetch accident reports: {e}")
        return []

# ------------------------------------------------------------------------------------------------
# Delete user # ------------------------------------------------------------------------------------------------
def delete_user(user_id):
    """
    Deletes a user from the database based on their user ID.
    """
    conn = db_connect()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
        conn.commit()
        st.success(f"User with ID {user_id} deleted successfully!")
    except Exception as e:
        st.error(f"Failed to delete user: {e}")
    finally:
        conn.close()

# ------------------------------------------------------------------------------------------------
# Update user # ------------------------------------------------------------------------------------------------
def update_user(user_id, new_username=None, new_password=None, new_role=None):
    """
    Updates a user's details in the database. Only the provided fields will be updated.
    """
    conn = db_connect()
    if not conn:
        return
    try:
        cur = conn.cursor()
        if new_username:
            cur.execute("UPDATE users SET username = %s WHERE id = %s;", (new_username, user_id))
        if new_password:
            cur.execute("UPDATE users SET password = crypt(%s, gen_salt('bf')) WHERE id = %s;", (new_password, user_id))
        if new_role:
            cur.execute("UPDATE users SET role = %s WHERE id = %s;", (new_role, user_id))
        conn.commit()
        st.success(f"User with ID {user_id} updated successfully!")
    except Exception as e:
        st.error(f"Failed to update user: {e}")
    finally:
        conn.close()
