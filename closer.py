import streamlit as st
import smtplib
import json
from email.message import EmailMessage

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
        return {"faith_in_you": 0, "comeback_of_love": 0}

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

    I noticed the changes in me, and I really appreciate you accepting my feelings.  

    🌟 Faith in You: {faith}/100  
    ❤️ Comeback of Love: {comeback}/100  

    It means a lot to me. Thank you!

    Best Regards,  
    {user_name}
    """

    if message_type == "decrease":
        subject_user = "⚠️ Relationship Advice: Handle Issues Wisely"
        subject_admin = "⚠️ Issues Arise – Let's Address Them Together"

        user_body = f"""
        Hello {user_name},

        Problems come and go in all relationships. Sit down and have a chat with your partner to solve the current issue.  

        Don’t let small problems pile up and create a rift like before. Take time to talk and sort things out. 

        🌟 Faith in You: {faith}/100  
        ❤️ Comeback of Love: {comeback}/100  

        Stay strong!

        Best Regards,  
        Admin
        """

        admin_body = f"""
        Hello {admin_name},

        Just a reminder: Problems come and go in every relationship.  

        Sit down and talk with your partner to solve the current issue. Small problems, if ignored, can turn into big ones. Let's not repeat past mistakes.  

        🌟 Faith in You: {faith}/100  
        ❤️ Comeback of Love: {comeback}/100  

        Have a conversation, listen, and fix things together.  

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

# Login form
st.title("Login")
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

# If authenticated, show respective pages
if st.session_state.authenticated:
    st.header(f"Hello, {st.session_state.username}!")

    if st.session_state.role == "admin":
        st.subheader("Admin Panel")

        # Admin sets new values
        new_faith = st.slider("Faith in You", 0, 100, saved_values["faith_in_you"])
        new_comeback = st.slider("Comeback of Love", 0, 100, saved_values["comeback_of_love"])

        # Save button: Only updates permanent storage when clicked
        if st.button("Save Changes"):
            if new_faith > saved_values["faith_in_you"] or new_comeback > saved_values["comeback_of_love"]:
                message_type = "increase"
            else:
                message_type = "decrease"

            save_values(new_faith, new_comeback)  # Save to JSON
            send_email(new_faith, new_comeback, message_type)  # Send email based on change type
            st.success("Values saved successfully!")

        # Display current values
        st.write(f"**Faith in You:** {new_faith}")
        st.write(f"**Comeback of Love:** {new_comeback}")

    elif st.session_state.role == "user":
        st.subheader("User View")
        st.write(f"**Faith in You:** {saved_values['faith_in_you']}")
        st.write(f"**Comeback of Love:** {saved_values['comeback_of_love']}")

    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.role = None
        st.session_state.username = ""
        st.rerun()
