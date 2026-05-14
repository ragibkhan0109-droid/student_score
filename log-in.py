# Updated `app.py` with Login & Signup UI

```python
import streamlit as st
import joblib
import pandas as pd
import os
from app import main
main()

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Student Score Predictor", layout="centered")

# =========================
# CUSTOM CSS
# =========================
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f7fa;
    }

    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #1f3b73;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        color: gray;
        margin-bottom: 30px;
    }

    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 45px;
        font-size: 16px;
        font-weight: bold;
        background-color: #1f77ff;
        color: white;
        border: none;
    }

    .stButton>button:hover {
        background-color: #1557c0;
        color: white;
    }

    .block-container {
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# USER DATABASE FILE
# =========================
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


# =========================
# LOAD MODEL
# =========================
model = joblib.load("student_model.pkl")
columns = joblib.load("model_columns.pkl")


# =========================
# SESSION STATE
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


# =========================
# LOGIN / SIGNUP PAGE
# =========================
if not st.session_state.logged_in:

    st.markdown('<div class="title">🎓 Student Score Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Login or create an account to continue</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

    # ================= LOGIN =================
    with tab1:
        login_username = st.text_input("Username")
        login_password = st.text_input("Password", type="password")

        if st.button("Login"):
            users = load_users()

            if login_username in users and users[login_username] == login_password:
                st.session_state.logged_in = True
                st.session_state.username = login_username
                st.success("Login Successful ✅")
                st.rerun()
            else:
                st.error("Invalid Username or Password ❌")

    # ================= SIGNUP =================
    with tab2:
        signup_username = st.text_input("Create Username")
        signup_password = st.text_input("Create Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Create Account"):
            users = load_users()

            if signup_username in users:
                st.warning("Username already exists ⚠️")

            elif signup_password != confirm_password:
                st.error("Passwords do not match ❌")

            elif len(signup_password) < 4:
                st.warning("Password must be at least 4 characters")

            else:
                users[signup_username] = signup_password
                save_users(users)
                st.success("Account Created Successfully ✅")

# =========================
# MAIN APP
# =========================
else:

    st.sidebar.success(f"Welcome, {st.session_state.username} 👋")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    st.markdown('<div class="title">📊 Student Score Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Predict student exam performance using AI</div>', unsafe_allow_html=True)

    # =========================
    # INPUT FIELDS
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        hours = st.number_input("Hours Studied", 0.0, 24.0)
        attendance = st.number_input("Attendance (%)", 0.0, 100.0)
        previous = st.number_input("Previous Score", 0.0, 100.0)
        sleep = st.number_input("Sleep Hours", 0.0, 12.0)
        motivation = st.selectbox("Motivation Level", ["Low", "Medium", "High"])
        teacher = st.selectbox("Teacher Quality", ["Poor", "Average", "Good"])
        school = st.selectbox("School Type", ["Public", "Private"])

    with col2:
        internet = st.selectbox("Internet Access", ["Yes", "No"])
        income = st.selectbox("Family Income", ["Low", "Medium", "High"])
        parent = st.selectbox("Parental Involvement", ["Low", "Medium", "High"])
        education = st.selectbox("Parent Education", ["School", "College"])
        peer = st.selectbox("Peer Influence", ["Negative", "Neutral", "Positive"])
        resources = st.selectbox("Learning Resources", ["Low", "Medium", "High"])
        activities = st.selectbox("Extracurricular Activities", ["Yes", "No"])

    # =========================
    # PREDICTION BUTTON
    # =========================
    if st.button("Predict Score"):

        data = {
            "Hours_Studied": hours,
            "Attendance": attendance,
            "Previous_Scores": previous,
            "Sleep_Hours": sleep,
            "Motivation_Level": motivation,
            "Teacher_Quality": teacher,
            "School_Type": school,
            "Internet_Access": internet,
            "Family_Income": income,
            "Parental_Involvement": parent,
            "Parental_Education_Level": education,
            "Peer_Influence": peer,
            "Learning_Resources": resources,
            "Extracurricular_Activities": activities,
        }

        input_df = pd.DataFrame([data])
        input_df = pd.get_dummies(input_df)
        input_df = input_df.reindex(columns=columns, fill_value=0)

        prediction = model.predict(input_df)

        final_score = max(40, min(100, prediction[0]))
        final_score = int(round(final_score))

        st.success(f"🎯 Predicted Exam Score: {final_score}")

        if final_score >= 80:
            st.balloons()
            st.info("Excellent Performance 🌟")

        elif final_score >= 60:
            st.info("Good Performance 👍")

        else:
            st.warning("Needs Improvement 📚")
```


