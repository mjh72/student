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

st.set_page_config(page_title="Graduation Party 🎓", page_icon="🎉", layout="centered")

# CONFIGURATION
ADMIN_PASSWORD = "gradparty2025"
GUEST_PASSWORD = "party2025"
PARTY_DATE = datetime.datetime(2025, 6, 12)
ADMIN_EMAILS = ["mikael.held@gmail.com", "kim.held@gmail.com"]
SENDER_EMAIL = st.secrets["email"]["address"]
SENDER_PASSWORD = st.secrets["email"]["password"]
IMAGE_FILE = "studentmottagning.png"
ARROW_IMAGE = "arrow.png"
BACKGROUND_MUSIC = "https://www.bensound.com/bensound-music/bensound-celebration.mp3"

# GOOGLE SHEETS CONNECTION
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
)
client = gspread.authorize(credentials)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1nTmF8-5iKdCqsYZbO4iuSZ8c6txftnd1kiKMOsZemDo/edit#gid=0").sheet1

# EMAIL FUNCTION

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

# LOAD RSVPs

def load_rsvps():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# SAVE RSVP

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

# CUSTOM STYLING
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #ff4b4b;
        color: white;
        padding: 0.75rem 1.5rem;
        font-size: 24px;
        border-radius: 12px;
        border: none;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #ff0000;
    }
    body {
        background-color: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)

# Background Music Toggle
music_on = st.sidebar.checkbox("🎵 Play Music", value=True)
if music_on:
    components.html(f"""
    <audio autoplay loop>
      <source src="{BACKGROUND_MUSIC}" type="audio/mpeg">
    Your browser does not support the audio element.
    </audio>
    """, height=0)

# TITLE AND IMAGE
st.title("🎓 You're Invited to the Graduation Celebration!")

st.image(IMAGE_FILE, use_container_width=True)

# PARTY INFO
st.markdown("""
<div style='text-align: center; font-size: 20px; color: #4a4a4a;'>
Join us to celebrate this special milestone with love, laughter, and joy from Leopoldine and Zacharias! 🎉
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; font-size: 20px; color: #333; margin-top: 20px;'>
<h3>📅 Graduation Party Info</h3>
<b>When:</b> 🗓️ June 12, 2025<br>
<b>Time:</b> 🕔 17:00 – 23:00<br>
<b>Where:</b> 📍 Filmgatan 30, Solna<br>
<b>What:</b> 🎓 Graduation ceremony, dinner, and party hopping!<br>
<p style='margin-top: 10px;'>You can add this event manually to your calendar, or use Google Calendar below:</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; margin-top: 10px;'>
<a href="https://calendar.google.com/calendar/r/eventedit?text=Graduation+Party+for+Leopoldine+%26+Zacharias&dates=20250612T150000Z/20250612T210000Z&details=Celebrate+the+graduation+party!&location=Filmgatan+30,+Solna" target="_blank">📅 Add to Google Calendar</a>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; margin-top: 20px;'>
<a href="https://maps.google.com/?q=Filmgatan+30,+Solna" target="_blank">🗺️ View Party Location on Map</a>
</div>
""", unsafe_allow_html=True)

# GUEST LOGIN
if "rsvp_mode" not in st.session_state:
    st.session_state.rsvp_mode = False
if "guest_authenticated" not in st.session_state:
    st.session_state.guest_authenticated = False

if not st.session_state.rsvp_mode:
    st.image(ARROW_IMAGE, width=150)
    if st.button("🎟️ Reserve Your Seats!"):
        st.session_state.rsvp_mode = True

if st.session_state.rsvp_mode and not st.session_state.guest_authenticated:
    guest_password = st.text_input("Enter Guest Password to RSVP", type="password")
    if guest_password == GUEST_PASSWORD:
        st.session_state.guest_authenticated = True
        st.success("✅ Access granted! Fill in your RSVP below.")
    elif guest_password:
        st.error("Incorrect password. Please try again.")

# RSVP FORM
if st.session_state.rsvp_mode and st.session_state.guest_authenticated:
    st.header("🎉 RSVP Form")
    with st.form("RSVP"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        party_size = st.number_input("How many people in your group?", min_value=1, step=1)
        graduation = st.checkbox("Will you attend the Graduation Ceremony?")
        dinner = st.checkbox("Will you attend the Dinner?")
        party_hopping = st.checkbox("Will you attend the Party Hopping?")
        food_allergies = st.text_input("Food Allergies or Special Diet?")

        submit_rsvp = st.form_submit_button("Submit RSVP")

        if submit_rsvp:
            new_rsvp = {
                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Name": name,
                "Email": email,
                "Party Size": party_size,
                "Graduation": graduation,
                "Dinner": dinner,
                "Party Hopping": party_hopping,
                "Food Allergies": food_allergies
            }
            save_rsvp(new_rsvp)
            st.success("🎉 Thank you for your RSVP!")
            st.balloons()
            send_email(email, "Graduation RSVP Confirmation", "Thank you for RSVPing to the Graduation Party! 🎓🎉")
            for admin in ADMIN_EMAILS:
                send_email(admin, "New RSVP Received", f"New RSVP from {name} ({email})")

            st.markdown("""
            <div style='text-align: center; font-size: 24px; color: #4BB543; margin-top: 30px;'>
            ✅ Your spot is reserved! We look forward to celebrating with you! 🎉
            </div>
            """, unsafe_allow_html=True)

# REAL-TIME RSVP FEED
st.header("📜 Latest RSVPs")
try:
    rsvps = load_rsvps()
    if not rsvps.empty:
        latest_rsvps = rsvps.sort_values("Timestamp", ascending=False).head(5)
        for idx, row in latest_rsvps.iterrows():
            st.info(f"{row['Timestamp']} - {row['Name']} ({row['Party Size']} people)")
    else:
        st.write("No RSVPs yet!")
except Exception as e:
    st.warning("Could not load real-time RSVPs.")

# LIVE GUEST COUNTER
try:
    rsvps = load_rsvps()
    if "Party Size" in rsvps.columns:
        total_guests = rsvps["Party Size"].sum()
        st.markdown(f"<div style='text-align: center; font-size: 22px; color: #4BB543; margin-top: 20px;'>🎉 {total_guests} guests have already RSVPed!</div>", unsafe_allow_html=True)
except Exception as e:
    st.warning("Could not load live guest counter.")

# REMINDER EMAILS
if datetime.datetime.now() >= (PARTY_DATE - datetime.timedelta(days=3)):
    try:
        all_rsvps = load_rsvps()
        for idx, row in all_rsvps.iterrows():
            guest_email = row["Email"]
            send_email(guest_email, "Reminder: Graduation Party Soon!", "🎓 Reminder: The Graduation Party for Leopoldine and Zacharias is happening in 3 days! We can't wait to see you!")
        st.success("🎉 Reminder emails sent!")
    except Exception as e:
        st.warning("Could not send reminder emails.")

# ADMIN PANEL
admin_view = st.sidebar.radio("Admin Options", ["None", "Admin Panel"])
if admin_view == "Admin Panel":
    st.header("🔒 Admin Panel")
    password = st.text_input("Enter admin password", type="password")
    if password == ADMIN_PASSWORD:
        st.success("Access granted ✅")
        rsvps = load_rsvps()
        st.dataframe(rsvps)
        if "Party Size" in rsvps.columns:
            total_guests = rsvps["Party Size"].sum()
            st.markdown(f"## 🎉 Total expected guests: {total_guests}")

        st.subheader("📊 RSVP Statistics")
        if "Graduation" in rsvps.columns and "Dinner" in rsvps.columns and "Party Hopping" in rsvps.columns:
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
