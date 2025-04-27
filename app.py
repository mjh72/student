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

# Sidkonfiguration
st.set_page_config(page_title="Studentfirande 🎓", page_icon="🎉", layout="centered")

# KONFIGURATION
ADMIN_PASSWORD = "gradparty2025"
GUEST_PASSWORD = "party2025"
PARTY_DATE = datetime.datetime(2025, 6, 12)
ADMIN_EMAILS = ["mikael.held@gmail.com", "kim.held@gmail.com"]
SENDER_EMAIL = st.secrets["email"]["address"]
SENDER_PASSWORD = st.secrets["email"]["password"]
IMAGE_FILE = "studentmottagning.png"
ARROW_IMAGE = "arrow.png"
BACKGROUND_MUSIC = "https://www.bensound.com/bensound-music/bensound-celebration.mp3"

# GOOGLE SHEETS-KOPPLING
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
)
client = gspread.authorize(credentials)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1nTmF8-5iKdCqsYZbO4iuSZ8c6txftnd1kiKMOsZemDo/edit#gid=0").sheet1

# FUNKTION FÖR E-POST

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
        st.error(f"E-post misslyckades att skickas: {e}")

# LADDA RSVP

def load_rsvps():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# SPARA RSVP

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

# FRONTEND ÖVERSÄTTNING

st.title("🎓 Du är inbjuden till studentfirandet!")
st.image(IMAGE_FILE, use_container_width=True)

st.markdown("""
<div style='text-align: center; font-size: 20px; color: #4a4a4a;'>
Kom och fira denna milstolpe tillsammans med Leopoldine och Zacharias! 🎉
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; font-size: 20px; color: #333; margin-top: 20px;'>
<h3>📅 Information om Studentfirandet</h3>
<b>När:</b> 🗓️ 12 juni 2025<br>
<b>Tid:</b> 🕔 17:00 – 23:00<br>
<b>Plats:</b> 📍 Filmgatan 30, Solna<br>
<b>Vad:</b> 🎓 Ceremoni, middag och efterfest!
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; margin-top: 10px;'>
<a href="https://calendar.google.com/calendar/r/eventedit?text=Studentfirande+för+Leopoldine+och+Zacharias&dates=20250612T150000Z/20250612T210000Z&details=Kom+och+fira+med+oss!&location=Filmgatan+30,+Solna" target="_blank">📅 Lägg till i Google Kalender</a>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; margin-top: 20px;'>
<a href="https://maps.google.com/?q=Filmgatan+30,+Solna" target="_blank">🗺️ Visa festplats på karta</a>
</div>
""", unsafe_allow_html=True)

# (Fortsätter med RSVP-formulär och Adminpanel på svenska...)
