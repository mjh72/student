import streamlit as st
import pandas as pd
import datetime
import random
import smtplib
from email.message import EmailMessage
import gspread
from google.oauth2 import service_account
import streamlit.components.v1 as components
import plotly.express as px

# 🛠 FIX: Set page config FIRST
st.set_page_config(page_title="Graduation Party 🎓", page_icon="🎉", layout="centered")

# -------------------------
# CONFIGURATION
# -------------------------
ADMIN_PASSWORD = "gradparty2025"
GUEST_PASSWORD = "party2025"
PARTY_DATE = datetime.datetime(2025, 6, 12)
ADMIN_EMAILS = ["mikael.held@gmail.com", "kim.held@gmail.com"]
SENDER_EMAIL = st.secrets["email"]["address"]
SENDER_PASSWORD = st.secrets["email"]["password"]
IMAGE_FILE = "studentmottagning.png"
ARROW_IMAGE = "arrow.png"
BACKGROUND_MUSIC = "https://www.bensound.com/bensound-music/bensound-celebration.mp3"
SHEET_NAME = "Graduation_RSVP_Leopoldine_Zacharias"

# -------------------------
# GOOGLE SHEETS CONNECTION
# -------------------------
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
)
client = gspread.authorize(credentials)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1nTmF8-5iKdCqsYZbO4iuSZ8c6txftnd1kiKMOsZemDo/edit#gid=0").sheet1

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
# LOAD RSVPs
# -------------------------
def load_rsvps():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# -------------------------
# SAVE RSVP
# -------------------------
def save_rsvp(new_rsvp):
    sheet.append_row([
        new_rsvp["Timestamp"],
        new_rsvp["Name"],
        new_rsvp["Email"],
        new_rsvp["Party Size"],
        str(new_rsvp["Graduation"]),
        str(new_rsvp["Dinner"]),
        str(new_rsvp["Party Hopping"]),
        new_rsvp["Food Allergies"]
    ])

# -------------------------
# CUSTOM STYLING
# -------------------------
st.markdown("""
    <style>
    body {
        background-color: #f5f5f5;
    }
    .main {
        background-color: rgba(255, 255, 255, 0.95);
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
        user-drag: none;
        pointer-events: none;
    }
    .arrow {
        text-align: center;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Background Music
components.html(f"""
<audio autoplay loop>
  <source src="{BACKGROUND_MUSIC}" type="audio/mpeg">
Your browser does not support the audio element.
</audio>
""", height=0)

# Countdown Script
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

st.image(IMAGE_FILE, use_container_width=True)

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

st.markdown("""
<div style='text-align: center;'>
<a href="https://calendar.google.com/calendar/r/eventedit?text=Graduation+Party+for+Leopoldine+%26+Zacharias&dates=20250612T150000Z/20250612T210000Z&details=Celebrate+the+graduation+party!&location=Filmgatan+30,+Solna" target="_blank">📅 Add to Google Calendar</a>
</div>
""", unsafe_allow_html=True)

if "rsvp_mode" not in st.session_state:
    st.session_state.rsvp_mode = False

if not st.session_state.rsvp_mode:
    st.image(ARROW_IMAGE, use_column_width=False)
    if st.button("🎟️ Reserve Your Seats!"):
        st.session_state.rsvp_mode = True

view = "Guest RSVP" if st.session_state.rsvp_mode else None

admin_view = st.sidebar.radio("Admin Options", ["None", "Admin Panel"])

# -------------------------
# ADMIN PANEL UPGRADES
# -------------------------
if admin_view == "Admin Panel":
    st.header("🔒 Admin Panel")
    password = st.text_input("Enter admin password", type="password")
    if password == ADMIN_PASSWORD:
        st.success("Access granted ✅")
        rsvps = load_rsvps()
        st.dataframe(rsvps)
        total_guests = rsvps["Party Size"].sum()
        st.markdown(f"## 🎉 Total expected guests: {total_guests}")

        st.subheader("📊 RSVP Statistics")
        grad_attending = rsvps[rsvps["Graduation"] == "True"]["Party Size"].sum()
        dinner_attending = rsvps[rsvps["Dinner"] == "True"]["Party Size"].sum()
        partyhopping_attending = rsvps[rsvps["Party Hopping"] == "True"]["Party Size"].sum()

        stats_df = pd.DataFrame({
            "Event": ["Graduation", "Dinner", "Party Hopping"],
            "Attendees": [grad_attending, dinner_attending, partyhopping_attending]
        })

        fig = px.bar(stats_df, x="Event", y="Attendees", color="Event", title="Guest Attendance Overview")
        st.plotly_chart(fig)

        st.download_button("📥 Download RSVP list", rsvps.to_csv(index=False), file_name="rsvps.csv")
    elif password:
        st.error("Incorrect password. Try again.")
