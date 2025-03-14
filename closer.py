import streamlit as st

# Load credentials from Streamlit secrets
admin_email = st.secrets["credentials"]["admin_email"]
admin_password = st.secrets["credentials"]["admin_password"]
admin_name = st.secrets["credentials"]["admin_name"]

user_email = st.secrets["credentials"]["user_email"]
user_password = st.secrets["credentials"]["user_password"]
user_name = st.secrets["credentials"]["user_name"]

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = ""

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
        st.subheader("Admin Page")
        value = st.slider("Set Value (0 to 100)", 0, 100)
        st.session_state.value = value
        st.write(f"Current value: {value}")

    elif st.session_state.role == "user":
        st.subheader("User Page")
        value = st.session_state.get("value", 0)  # Default to 0 if not set
        st.write(f"Current value: {value}")

    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.role = None
        st.session_state.username = ""
        st.rerun()
