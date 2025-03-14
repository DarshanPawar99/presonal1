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

# Function to send email notification
def send_email(faith, comeback, message_type):
    subject_user = "🎉 Congratulations! You're on the Right Path"
    subject_admin = "❤️ Keep Up! I Appreciate You Accepting My Feelings"

    user_body = f"""
    Hello {user_name},

    🎉 Great News! Your progress has been updated.

    🌟 Faith in You: {faith}/100  
    ❤️ Comeback of Love: {comeback}/100  

    Keep up the great work!

    Best Regards,  
    Admin
    """

    admin_body = f"""
    Hello {admin_name},

    I appreciate you accepting my feelings and giving feedback.

    🌟 Faith in You: {faith}/100  
    ❤️ Comeback of Love: {comeback}/100  

    Thank you!

    Best Regards,  
    {user_name}
    """

    if message_type == "decrease":
        subject_user = "⚠️ Relationship Advice: Handle Issues Wisely"
        subject_admin = "⚠️ Issues Arise – Let's Address Them Together"

        user_body = f"""
        Hello {user_name},

        Problems come and go in all relationships. 

        🌟 Faith in You: {faith}/100  
        ❤️ Comeback of Love: {comeback}/100  

        Stay strong!

        Best Regards,  
        Admin
        """

        admin_body = f"""
        Hello {admin_name},

        Problems come and go in every relationship.  

        🌟 Faith in You: {faith}/100  
        ❤️ Comeback of Love: {comeback}/100  

        Have a conversation and fix things together.  

        Best Regards,  
        {user_name}
        """

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)

            # Send email to User
            user_msg = EmailMessage()
            user_msg["Subject"] = subject_user
            user_msg["From"] = sender_email
            user_msg["To"] = recipient_user_email
            user_msg.set_content(user_body)
            server.send_message(user_msg)

            # Send email to Admin
            admin_msg = EmailMessage()
            admin_msg["Subject"] = subject_admin
            admin_msg["From"] = sender_email
            admin_msg["To"] = recipient_admin_email
            admin_msg.set_content(admin_body)
            server.send_message(admin_msg)

        st.success("Emails sent successfully!")

    except Exception as e:
        st.error(f"Error sending email: {e}")

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
            st.rerun()  # Refresh the page

# Login form (Only show if not authenticated)
if not st.session_state.authenticated:
    with st.form("login_form"):
        st.subheader("🔐 Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

        if login_button:
            if email == admin_email and password == admin_password:
                st.session_state.authenticated = True
                st.session_state.role = "admin"
                st.session_state.username = admin_name
                st.success(f"Logged in as Admin ({admin_name})")
                st.rerun()  # Refresh the page to hide the login fields
            elif email == user_email and password == user_password:
                st.session_state.authenticated = True
                st.session_state.role = "user"
                st.session_state.username = user_name
                st.success(f"Logged in as User ({user_name})")
                st.rerun()  # Refresh the page to hide the login fields
            else:
                st.error("Invalid email or password")

# Show content only if authenticated
if st.session_state.authenticated:
    st.title("❤️ Relationship Tracker")
    st.header(f"Hello, {st.session_state.username}! 😊")
    st.markdown("---")


    if st.session_state.role == "admin":
        st.subheader("Express your feelings❤️")

        # Admin sets new values
        new_faith = st.slider("🌟 Faith in You", 0, 100, saved_values["faith_in_you"], format="%d")
        new_comeback = st.slider("❤️ Comeback of Love", 0, 100, saved_values["comeback_of_love"], format="%d")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("🌟 Faith in You", new_faith)
        with col2:
            st.metric("❤️ Comeback of Love", new_comeback)

        if st.button("✅ Save Changes"):
            message_type = "increase" if (new_faith > saved_values["faith_in_you"] or new_comeback > saved_values["comeback_of_love"]) else "decrease"

            save_values(new_faith, new_comeback)
            send_email(new_faith, new_comeback, message_type)
            st.success("Values saved successfully!")

    elif st.session_state.role == "user":
        st.subheader("View Progress 👀")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("🌟 Faith in You", saved_values["faith_in_you"])
        with col2:
            st.metric("❤️ Comeback of Love", saved_values["comeback_of_love"])
