import streamlit as st
import smtplib
import json
from email.message import EmailMessage

# Set page layout to wide
st.set_page_config(layout="wide")

# Load credentials from Streamlit secrets
admin_email = st.secrets["credentials"]["admin_email"]
admin_password = st.secrets["credentials"]["admin_password"]
admin_name = st.secrets["credentials"]["admin_name"]

user_email = st.secrets["credentials"]["user_email"]
user_password = st.secrets["credentials"]["user_password"]
user_name = st.secrets["credentials"]["user_name"]

# Load email settings
smtp_server = st.secrets["email"]["smtp_server"]
smtp_port = st.secrets["email"]["smtp_port"]
sender_email = st.secrets["email"]["sender_email"]
sender_password = st.secrets["email"]["sender_password"]
recipient_user_email = st.secrets["email"]["recipient_user_email"]
recipient_admin_email = st.secrets["email"]["recipient_admin_email"]

DATA_FILE = "data.json"

# Function to load saved values
def load_saved_values():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        default_data = {"faith_in_you": 0, "comeback_of_love": 0}
        with open(DATA_FILE, "w") as file:
            json.dump(default_data, file)
        return default_data

# Function to save values
def save_values(faith, comeback):
    data = {"faith_in_you": faith, "comeback_of_love": comeback}
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

# Load last saved values
saved_values = load_saved_values()

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = ""

# Logout button (Top-right corner)
if st.session_state.authenticated:
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.role = None
            st.session_state.username = ""
            st.rerun()

st.title("❤️ Relationship Tracker")

# Login form (Only show if not authenticated)
if not st.session_state.authenticated:
    st.subheader("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email == admin_email and password == admin_password:
            st.session_state.authenticated = True
            st.session_state.role = "admin"
            st.session_state.username = admin_name
            st.success(f"Logged in as Admin ({admin_name})")
        elif email == user_email and password == user_password:
            st.session_state.authenticated = True
            st.session_state.role = "user"
            st.session_state.username = user_name
            st.success(f"Logged in as User ({user_name})")
        else:
            st.error("Invalid email or password")

# Show content only if authenticated
if st.session_state.authenticated:
    st.header(f"Hello, {st.session_state.username}! 😊")

    if st.session_state.role == "admin":
        st.subheader("Admin Panel 🎛️")

        # Admin sets new values (sliders)
        new_faith = st.slider("🌟 Faith in You", 0, 100, saved_values["faith_in_you"], step=10)
        new_comeback = st.slider("❤️ Comeback of Love", 0, 100, saved_values["comeback_of_love"], step=10)

        # Save button: Only updates permanent storage when clicked
        if st.button("✅ Save Changes"):
            if new_faith > saved_values["faith_in_you"] or new_comeback > saved_values["comeback_of_love"]:
                message_type = "increase"
            else:
                message_type = "decrease"

            save_values(new_faith, new_comeback)  # Save to JSON
            st.success("Values saved successfully!")

        # **NEW:** Display selected values below the save button using columns
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🌟 Faith in You", new_faith)
        with col2:
            st.metric("❤️ Comeback of Love", new_comeback)

    elif st.session_state.role == "user":
        st.subheader("User View 👀")

        # Display current values side by side
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🌟 Faith in You", saved_values["faith_in_you"])
        with col2:
            st.metric("❤️ Comeback of Love", saved_values["comeback_of_love"])
