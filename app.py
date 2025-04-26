import streamlit as st
import pandas as pd
import datetime
import random
import smtplib
from email.message import EmailMessage
import streamlit.components.v1 as components

# 🛠 FIX: Set page config FIRST
st.set_page_config(page_title="Graduation Party 🎓", page_icon="🎉", layout="centered")

# -------------------------
# CONFIGURATION
# -------------------------
ADMIN_PASSWORD = "gradparty2025"
GUEST_PASSWORD = "party2025"
CSV_FILE = "rsvps.csv"
PARTY_DATE = datetime.datetime(2025, 6, 12)
ADMIN_EMAILS = ["mikael.held@gmail.com", "kim.held@gmail.com"]
SENDER_EMAIL = "your_email@gmail.com"  # Change this to your sending email
SENDER_PASSWORD = "your_app_password"  # Change this to your email app password
IMAGE_FILE = "studentmottagning.png"  # Updated for GitHub deployment

# -------------------------
# EMAIL FUNCTION
# -------------------------
def send_email(to_email, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        st.error(f"Email failed to send: {e}")

# -------------------------
# INITIAL LOAD
# -------------------------
try:
    rsvps = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    rsvps = pd.DataFrame(columns=[
        "Timestamp", "Name", "Email", "Graduation", "Dinner", "Open House", "Food Allergies"
    ])

# -------------------------
# CUSTOM STYLING
# -------------------------
st.markdown("""
    <style>
    body {
        background-image: url('https://images.unsplash.com/photo-1521335629791-ce4aec67dd47?fit=crop&w=1350&q=80');
        background-size: cover;
        background-position: center;
        margin: 0;
        padding: 0;
    }
    .main {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1rem;
        margin: auto;
        max-width: 700px;
    }
    h1, h2, h3, h4, p, div {
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    img {
        -webkit-user-drag: none;
        -khtml-user-drag: none;
        -moz-user-drag: none;
        -o-user-drag: none;
        user-drag: none;
        pointer-events: none;
    }
    @media (max-width: 768px) {
        .main {
            padding: 1rem;
            margin: 1rem;
        }
        h1 {
            font-size: 26px;
        }
    }
    </style>
""", unsafe_allow_html=True)

components.html("""
<script>
    if (window.innerWidth < 768) {
        alert('🎉 Welcome to the Graduation Party RSVP! Love from Leopoldine & Zacharias 🎓');
    }
</script>
""", height=0)

# -------------------------
# APP LAYOUT
# -------------------------
st.title("🎓 You're Invited to the Graduation Celebration!")

# Display Invitation Image
st.image(IMAGE_FILE, use_column_width=True)

# Countdown to Party
today = datetime.datetime.now()
days_left = (PARTY_DATE - today).days
if days_left > 0:
    st.markdown(f"<div style='text-align: center; font-size: 22px; color: #ff4b4b;'>🎉 Only {days_left} days left until the party! 🎉</div>", unsafe_allow_html=True)
else:
    st.markdown("<div style='text-align: center; font-size: 22px; color: #4BB543;'>🎉 The party is happening today! 🎉</div>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; font-size: 20px; color: #4a4a4a;'>
Join us to celebrate this special milestone with love, laughter, and joy from Leopoldine and Zacharias! 🎉
</div>
""", unsafe_allow_html=True)

view = st.sidebar.radio("Select view", ["Guest RSVP", "Admin Panel"])

# -------------------------
# GUEST RSVP FORM & ADMIN PANEL (TO BE CONTINUED)
# -------------------------
# Here you would continue with your RSVP form and Admin Panel code as it was before!
