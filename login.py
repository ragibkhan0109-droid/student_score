import streamlit as st
import json
import os

st.set_page_config(page_title="Login", layout="centered")

# ---------------- USERS FILE ----------------
USER_FILE = "users.json"

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# ---------------- TITLE ----------------
st.title("🎓 Student Score Predictor")
st.subheader("Login or Sign Up")

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["Login", "Sign Up"])

# ================= LOGIN =================
with tab1:

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        users = load_users()

        if username in users and users[username] == password:

            st.success("Login Successful ✅")

            # Open app.py
            st.success("Login Successful ✅")

st.write("Click below to open Predictor App")

if st.button("Open Predictor"):
    st.markdown(
        """
        <meta http-equiv="refresh" content="0; url=http://localhost:8501/app">
        """,
        unsafe_allow_html=True
    )

        else:
            st.error("Invalid Username or Password")

# ================= SIGNUP =================
with tab2:

    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):

        users = load_users()

        if new_user in users:
            st.warning("Username already exists")

        elif new_pass != confirm:
            st.error("Passwords do not match")

        else:
            users[new_user] = new_pass
            save_users(users)

            st.success("Account Created Successfully ✅")