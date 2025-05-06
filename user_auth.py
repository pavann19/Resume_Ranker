import streamlit as st
import hashlib

user_db = {}
user_history_db = {}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(username, password):
    return username in user_db and user_db[username] == hash_password(password)

def add_user(username, password):
    if username not in user_db:
        user_db[username] = hash_password(password)
        return True
    return False

def login_signup():
    st.sidebar.title("User Login/Signup")
    choice = st.sidebar.selectbox("Choose action", ["Login", "Sign Up"])
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if choice == "Sign Up":
        if st.sidebar.button("Create Account"):
            if add_user(username, password):
                st.success("Account created successfully! Please login.")
            else:
                st.warning("Username already exists.")

    elif choice == "Login":
        if st.sidebar.button("Login"):
            if check_credentials(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome back, {username}!")
                st.rerun()

            else:
                st.error("Invalid credentials. Please try again.")

def save_history(username, resume_data):
    if username not in user_history_db:
        user_history_db[username] = []
    user_history_db[username].append(resume_data)

def get_resume_history(username):
    return user_history_db.get(username, [])
