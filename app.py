import streamlit as st
import pandas as pd
import datetime
import random
import smtplib
from email.message import EmailMessage
import gspread
from google.oauth2 import service_account
import streamlit.components.v1 as components

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
        str(new_rsvp["Graduation"]),
        str(new_rsvp["Dinner"]),
        str(new_rsvp["Open House"]),
        new_rsvp["Food Allergies"]
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

if "rsvp_mode" not in st.session_state:
    st.session_state.rsvp_mode = False

if not st.session_state.rsvp_mode:
    if st.button("📋 Click here to RSVP!"):
        st.session_state.rsvp_mode = True

view = "Guest RSVP" if st.session_state.rsvp_mode else None

admin_view = st.sidebar.radio("Admin Options", ["None", "Admin Panel"])

# -------------------------
# GUEST RSVP FORM & ADMIN PANEL
# -------------------------
if view == "Guest RSVP":
    st.header("📋 RSVP Form")
    language = st.selectbox("🌐 Select Language / Välj Språk", ("🇬🇧 English", "🇸🇪 Svenska"))
    guest_password = st.text_input("🔒 Enter invitation password", type="password")

    if guest_password == GUEST_PASSWORD:
        with st.form("rsvp_form"):
            if language == "🇬🇧 English":
                name = st.text_input("Full Name")
                email = st.text_input("Email Address")
                grad = st.checkbox("I will attend the Graduation Ceremony 📚")
                dinner = st.checkbox("I will attend the Dinner 🍽️")
                open_house = st.checkbox("I will attend the Open House 🏡")
                allergies = st.text_area("Food allergies / Dietary needs", placeholder="None")
                submit_label = "Submit RSVP"
                success_message = "🎉 Thank you for your RSVP! We can't wait to celebrate with you! 🎉"
                email_subject = "Graduation Party RSVP Confirmation 🎓"
                email_body = lambda name, grad, dinner, open_house, allergies: f"Hi {name},\n\nThank you for your RSVP!\nGraduation: {grad}\nDinner: {dinner}\nOpen House: {open_house}\nFood Allergies: {allergies}\n\nLove, Leopoldine & Zacharias"
            else:
                name = st.text_input("Fullständigt Namn")
                email = st.text_input("E-postadress")
                grad = st.checkbox("Jag kommer till Examensceremonin 📚")
                dinner = st.checkbox("Jag kommer till Middagen 🍽️")
                open_house = st.checkbox("Jag kommer till Öppet Hus 🏡")
                allergies = st.text_area("Allergier / Specialkost", placeholder="Ingen")
                submit_label = "Skicka OSA"
                success_message = "🎉 Tack för din OSA! Vi ses på festen! 🎉"
                email_subject = "Bekräftelse: OSA till studentfirande 🎓"
                email_body = lambda name, grad, dinner, open_house, allergies: f"Hej {name},\n\nTack för din OSA!\nExamensceremoni: {grad}\nMiddag: {dinner}\nÖppet Hus: {open_house}\nAllergier/Specialkost: {allergies}\n\nVi ses snart! 🎉\nHälsningar, Leopoldine & Zacharias"

            submitted = st.form_submit_button(submit_label)
            if submitted:
                new_rsvp = {
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Name": name,
                    "Email": email,
                    "Graduation": grad,
                    "Dinner": dinner,
                    "Open House": open_house,
                    "Food Allergies": allergies
                }
                save_rsvp(new_rsvp)
                st.success(success_message)
                st.balloons()
                subject = email_subject
                body = email_body(name, grad, dinner, open_house, allergies)
                send_email(email, subject, body)
                for admin_email in ADMIN_EMAILS:
                    send_email(admin_email, f"New RSVP from {name}! 🎉", body)

elif admin_view == "Admin Panel":
    st.header("🔒 Admin Panel")
    password = st.text_input("Enter admin password", type="password")
    if password == ADMIN_PASSWORD:
        st.success("Access granted ✅")
        rsvps = load_rsvps()
        st.dataframe(rsvps)
        st.download_button("📥 Download RSVP list", rsvps.to_csv(index=False), file_name="rsvps.csv")
    elif password:
        st.error("Incorrect password. Try again.")
