# Libraries and Modules
import streamlit as st
from utils.database import fetch_all_users, add_user, save_data
from utils.session_state import initialize_session_state

def render_admin_dashboard():
    """
    Displays the Admin Dashboard with functionality to manage users.
    Only accessible to superusers.
    """
    initialize_session_state()
    # Check if the user is authenticated and has superuser privileges
    if not st.session_state["authenticated"] or st.session_state["role"] != "superuser":
        st.error("Access denied. Superuser privileges are required.")
        return
    st.title("Admin Dashboard")
    st.write("Welcome, Superuser!")
    # Add User Form
    st.subheader("Add New User")
    new_username = st.text_input("New Username", key="admin_new_username")
    new_password = st.text_input("New Password", type="password", key="admin_new_password")
    new_role = st.selectbox("Role", ["superuser", "safety_generalist", "liability_adjuster"], key="admin_new_role")
    if st.button("Add User"):
        if new_username and new_password:
            add_user(new_username, new_password, new_role)
            st.success(f"User '{new_username}' added successfully!")
        else:
            st.error("Both username and password are required.")
        if st.button("Add User"):
            add_user(new_username, new_password, new_role)
            log_admin_action(st.session_state["username"], "add_user", f"Added user {new_username} with role {new_role}")
            st.success("User added successfully!")
    # Display All Users
    st.subheader("All Users")
    try:
        users = fetch_all_users()
        if users:
            st.table(users)
        else:
            st.info("No users found.")
    except Exception as e:
        st.error(f"Failed to fetch users: {e}")
        
import streamlit as st
from utils.database import fetch_all_users, update_user, delete_user

def manage_users():
    st.title("Manage Users")
    users = fetch_all_users()
    if users:
        for user in users:
            st.write(f"Username: {user['username']}, Role: {user['role']}")
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"Edit {user['username']}"):
                    edit_user(user)
            with col2:
                if st.button(f"Delete {user['username']}"):
                    delete_user(user["id"])
    else:
        st.info("No users found.")

def edit_user(user):
    st.text_input("Username", value=user["username"], key=f"edit_username_{user['id']}")
    st.text_input("Role", value=user["role"], key=f"edit_role_{user['id']}")
    if st.button(f"Save Changes for {user['username']}"):
        update_user(user["id"], st.session_state[f"edit_username_{user['id']}"], st.session_state[f"edit_role_{user['id']}"])
        st.success(f"Updated user {user['username']} successfully!")

def log_admin_action(admin_username, action_type, details):
    query = """
        INSERT INTO admin_logs (admin_username, action_type, details)
        VALUES (%s, %s, %s)
    """
    params = (admin_username, action_type, details)
    save_data(query, params)

