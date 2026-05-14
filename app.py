import streamlit as st
import json
import os

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Student Score Predictor",
    layout="centered"
)

# ================= USERS FILE =================
USER_FILE = "users.json"

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

# ================= LOAD USERS =================
def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

# ================= SAVE USERS =================
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ================= LOGIN / SIGNUP PAGE =================
if not st.session_state.logged_in:

    st.title("🎓 Student Score Predictor")

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

    # ================= LOGIN =================
    with tab1:

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            users = load_users()

            if username in users and users[username] == password:

                st.session_state.logged_in = True

                st.success("Login Successful ✅")

                st.rerun()

            else:
                st.error("Invalid Username or Password ❌")

    # ================= SIGNUP =================
    with tab2:

        new_user = st.text_input("Create Username")
        new_pass = st.text_input("Create Password", type="password")
        confirm_pass = st.text_input("Confirm Password", type="password")

        if st.button("Create Account"):

            users = load_users()

            if new_user in users:

                st.warning("Username already exists ⚠️")

            elif new_pass != confirm_pass:

                st.error("Passwords do not match ❌")

            else:

                users[new_user] = new_pass

                save_users(users)

                st.success("Account Created Successfully ✅")

# ================= MAIN APP =================
else:

    st.title("📊 Student Score Predictor")

    st.success("Welcome 👋")

    st.subheader("Enter Student Details")

    col1, col2 = st.columns(2)

    # ================= LEFT SIDE =================
    with col1:

        hours = st.number_input("Hours Studied", 0.0, 24.0)

        attendance = st.number_input(
            "Attendance",
            0.0,
            100.0
        )

        previous = st.number_input(
            "Previous Score",
            0.0,
            100.0
        )

        sleep = st.number_input(
            "Sleep Hours",
            0.0,
            12.0
        )

        motivation = st.selectbox(
            "Motivation Level",
            ["Low", "Medium", "High"]
        )

        teacher = st.selectbox(
            "Teacher Quality",
            ["Poor", "Average", "Good"]
        )

        school = st.selectbox(
            "School Type",
            ["Public", "Private"]
        )

    # ================= RIGHT SIDE =================
    with col2:

        internet = st.selectbox(
            "Internet Access",
            ["Yes", "No"]
        )

        income = st.selectbox(
            "Family Income",
            ["Low", "Medium", "High"]
        )

        parent = st.selectbox(
            "Parental Involvement",
            ["Low", "Medium", "High"]
        )

        education = st.selectbox(
            "Parent Education",
            ["School", "College"]
        )

        peer = st.selectbox(
            "Peer Influence",
            ["Negative", "Neutral", "Positive"]
        )

        resources = st.selectbox(
            "Learning Resources",
            ["Low", "Medium", "High"]
        )

        activities = st.selectbox(
            "Extracurricular Activities",
            ["Yes", "No"]
        )

# ================= PREDICT BUTTON =================
    if st.button("Predict Final Score"):

        final_score = (
            hours * 2
            + attendance * 0.2
            + previous * 0.5
            + sleep * 1.5
        )

        # Motivation effect
        if motivation == "High":
            final_score += 5

        elif motivation == "Medium":
            final_score += 3

        # Teacher effect
        if teacher == "Good":
            final_score += 5

        elif teacher == "Average":
            final_score += 2

        # Internet effect
        if internet == "Yes":
            final_score += 3

        # Resources effect
        if resources == "High":
            final_score += 5

        elif resources == "Medium":
            final_score += 2

        # Activities effect
        if activities == "Yes":
            final_score += 2

        # Score limit
        final_score = max(0, min(100, final_score))

        # Round value
        final_score = round(final_score, 2)

        # Output
        st.success(f"🎯 Predicted Final Score: {final_score}")

        # Performance message
        if final_score >= 80:

            st.balloons()

            st.info("Excellent Performance 🌟")

        elif final_score >= 60:

            st.info("Good Performance 👍")

        else:

            st.warning("Needs Improvement 📚")

    
    # ================= LOGOUT BUTTON =================
if st.button("Logout", key="logout_btn"):
    st.session_state.logged_in = False
    st.rerun()