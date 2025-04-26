import streamlit as st
import pandas as pd
import datetime
import random
import smtplib
from email.message import EmailMessage

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
SENDER_EMAIL = "mikael.held@gmail.com"  # Change this to your sending email
SENDER_PASSWORD = "gjja owjt xcmh bhpf"  # Change this to your email app password

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
    }
    .main {
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 15px;
        padding: 2rem;
    }
    h1, h2, h3, h4 {
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# APP LAYOUT
# -------------------------
st.title("🎓 You're Invited to the Graduation Celebration!")

# Countdown to Party
today = datetime.datetime.now()
days_left = (PARTY_DATE - today).days
if days_left > 0:
    st.markdown(f"<div style='text-align: center; font-size: 24px; color: #ff4b4b;'>🎉 Only {days_left} days left until the party! 🎉</div>", unsafe_allow_html=True)
else:
    st.markdown("<div style='text-align: center; font-size: 24px; color: #4BB543;'>🎉 The party is happening today! 🎉</div>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; font-size: 22px; color: #4a4a4a;'>
Join us to celebrate this special milestone with love, laughter, and joy! 🎉
</div>
""", unsafe_allow_html=True)

view = st.sidebar.radio("Select view", ["Guest RSVP", "Admin Panel"])

# -------------------------
# GUEST RSVP FORM
# -------------------------
if view == "Guest RSVP":
    st.header("📋 RSVP Form")
    guest_password = st.text_input("Enter invitation password", type="password")

    if guest_password == GUEST_PASSWORD:
        with st.form("rsvp_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            grad = st.checkbox("I will attend the Graduation Ceremony 📚")
            dinner = st.checkbox("I will attend the Dinner 🍽️")
            open_house = st.checkbox("I will attend the Open House 🏡")
            allergies = st.text_area("Food allergies / Dietary needs", placeholder="None")

            submitted = st.form_submit_button("Submit RSVP")

            if submitted:
                if name and email:
                    new_rsvp = {
                        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Name": name,
                        "Email": email,
                        "Graduation": grad,
                        "Dinner": dinner,
                        "Open House": open_house,
                        "Food Allergies": allergies
                    }
                    rsvps = pd.concat([rsvps, pd.DataFrame([new_rsvp])], ignore_index=True)
                    rsvps.to_csv(CSV_FILE, index=False)

                    st.success("🎉 Thank you for your RSVP! We can't wait to celebrate with you! 🎉")
                    st.balloons()
                    st.snow()
                    st.markdown("""
                        <div style='text-align: center; font-size:30px;'>🎊🎊🎊 Congratulations! 🎊🎊🎊</div>
                    """, unsafe_allow_html=True)
                    st.markdown("""
                        <div style='text-align: center; font-size:20px; color:#ff9900;'>Your spot at the celebration is confirmed! 🎉</div>
                    """, unsafe_allow_html=True)

                    # Send emails
                    subject = "Graduation Party RSVP Confirmation 🎓"
                    body = f"Hi {name},\n\nThank you for your RSVP!\n\nGraduation: {grad}\nDinner: {dinner}\nOpen House: {open_house}\nFood Allergies: {allergies}\n\nWe can't wait to see you! 🎉\n\nLove, Mikael & Kim"
                    send_email(email, subject, body)

                    for admin_email in ADMIN_EMAILS:
                        admin_subject = f"New RSVP from {name}! 🎉"
                        admin_body = f"{name} just RSVP'd!\n\nGraduation: {grad}\nDinner: {dinner}\nOpen House: {open_house}\nFood Allergies: {allergies}\nEmail: {email}"
                        send_email(admin_email, admin_subject, admin_body)
                else:
                    st.error("🚫 Please fill out at least your name and email!")
    elif guest_password:
        error_messages = [
            "🎉 Wrong password, but the party must go on!",
            "🎓 Graduation rockstars only!",
            "🎈 Oops! Password party fail!",
            "🎊 Keep trying, future graduate!"
        ]
        selected_message = random.choice(error_messages)
        st.markdown(f"""
            <div style='text-align: center; font-size:26px; color:#ff4b4b;'>
            {selected_message}
            </div>
        """, unsafe_allow_html=True)

        st.image("https://media.giphy.com/media/3oz8xKaR836UJOYeOc/giphy.gif")
        st.markdown("""
            <audio autoplay>
                <source src="https://www.soundjay.com/human/sounds/applause-01.mp3" type="audio/mpeg">
            </audio>
        """, unsafe_allow_html=True)
        st.snow()

# -------------------------
# ADMIN PANEL
# -------------------------
elif view == "Admin Panel":
    st.header("🔒 Admin Panel")
    password = st.text_input("Enter admin password", type="password")

    if password == ADMIN_PASSWORD:
        st.success("Access granted ✅")
        st.subheader("Guest List")
        st.dataframe(rsvps)

        st.download_button("📥 Download RSVP list as CSV", rsvps.to_csv(index=False), file_name="rsvps.csv")

    elif password:
        st.error("Incorrect password. Try again.")

# -------------------------
# FOOTER
# -------------------------
with st.expander("ℹ️ About this app"):
    st.write("Built with ❤️ using Streamlit. Hosting free on Streamlit Community Cloud.")
