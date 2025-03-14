import streamlit as st
import smtplib
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

# Initialize session state for authentication and slider values
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = ""

if "faith_in_you" not in st.session_state:
    st.session_state.faith_in_you = 0  # Default value

if "comeback_of_love" not in st.session_state:
    st.session_state.comeback_of_love = 0  # Default value

# Function to send email notification
def send_email(faith, comeback):
    # Email to the User
    user_msg = EmailMessage()
    user_msg["Subject"] = "🎉 Congratulations! You're on the Right Path"
    user_msg["From"] = sender_email
    user_msg["To"] = recipient_user_email

    user_body = f"""
    Hello {user_name},

    🎉 Great News! Your progress has been updated.

    🌟 Faith in You: {faith}/100  
    ❤️ Comeback of Love: {comeback}/100  

    Keep up the great work!

    Best Regards,  
    Admin
    """
    user_msg.set_content(user_body)

    # Email to the Admin
    admin_msg = EmailMessage()
    admin_msg["Subject"] = "❤️ Keep Up! I Appreciate You Accepting My Feelings"
    admin_msg["From"] = sender_email
    admin_msg["To"] = recipient_admin_email

    admin_body = f"""
    Hello {admin_name},

    I noticed the changes in me, and I really appreciate you accepting my feelings.  

    🌟 Faith in You: {faith}/100  
    ❤️ Comeback of Love: {comeback}/100  

    It means a lot to me. Thank you!

    Best Regards,  
    {user_name}
    """
    admin_msg.set_content(admin_body)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(user_msg)  # Send email to user
            server.send_message(admin_msg)  # Send email to admin
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

        # Capture slider updates
        new_faith = st.slider("Faith in You", 0, 100, st.session_state.faith_in_you)
        new_comeback = st.slider("Comeback of Love", 0, 100, st.session_state.comeback_of_love)

        # Check if values have changed
        if new_faith != st.session_state.faith_in_you or new_comeback != st.session_state.comeback_of_love:
            st.session_state.faith_in_you = new_faith
            st.session_state.comeback_of_love = new_comeback
            send_email(new_faith, new_comeback)  # Send email to both user & admin

        st.write(f"**Faith in You:** {st.session_state.faith_in_you}")
        st.write(f"**Comeback of Love:** {st.session_state.comeback_of_love}")

    elif st.session_state.role == "user":
        st.subheader("User View")
        st.write(f"**Faith in You:** {st.session_state.faith_in_you}")
        st.write(f"**Comeback of Love:** {st.session_state.comeback_of_love}")

    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.role = None
        st.session_state.username = ""
        st.rerun()
