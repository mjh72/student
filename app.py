import streamlit as st
import pandas as pd
import datetime
import smtplib
from email.message import EmailMessage
import gspread
from google.oauth2 import service_account
import plotly.express as px
from icalendar import Calendar, Event

# Sidkonfiguration
st.set_page_config(page_title="Studentfirande 🎓", page_icon="🎉", layout="centered")

# Lägg till bakgrundsfärg och knappstil
st.markdown("""
    <style>
    body {
        background-color: #FFF8E7;
    }
    .stButton > button {
        background-color: #FFD700;
        color: black;
        font-size: 20px;
        padding: 10px 24px;
        border-radius: 10px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# KONFIGURATION
ADMIN_PASSWORD = "gradparty2025"
GUEST_PASSWORD = "party2025"
PARTY_DATE = datetime.datetime(2025, 6, 12, 17, 0)
PARTY_END_DATE = datetime.datetime(2025, 6, 12, 23, 0)
ADMIN_EMAILS = ["mikael.held@gmail.com", "kim.held@gmail.com"]
SENDER_EMAIL = st.secrets["email"]["address"]
SENDER_PASSWORD = st.secrets["email"]["password"]
IMAGE_FILE = "studentmottagning.png"
ARROW_IMAGE = "arrow.png"

# GOOGLE SHEETS-KOPPLING
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
)
client = gspread.authorize(credentials)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1nTmF8-5iKdCqsYZbO4iuSZ8c6txftnd1kiKMOsZemDo/edit#gid=0").sheet1

# E-POSTFUNKTIONER
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

# FANCY EMAIL FÖR RSVP
def send_fancy_email(to_email, subject, guest_name):
    msg = EmailMessage()
    html_content = f"""
    <html>
    <body style='font-family: Arial, sans-serif; color: #333;'>
      <h2>🎓 Tack för din OSA, {guest_name}!</h2>
      <p>Vi ser fram emot att fira Leopoldine och Zacharias med dig!</p>
      <p><b>Datum:</b> 12 juni 2025<br>
         <b>Tid:</b> 17:00 - 23:00<br>
         <b>Plats:</b> Filmgatan 30, Solna
      </p>
      <p>Du kommer att få mer information närmare dagen. 🎉</p>
      <p>Hälsningar,<br><b>Familjen Held</b></p>
    </body>
    </html>
    """
    msg.add_alternative(html_content, subtype='html')
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
        str(new_rsvp["Utspring"]),
        str(new_rsvp["Mottagning"]),
        str(new_rsvp["Middag"]),
        new_rsvp["Food Allergies"]
    ])

# GENERERA ICS
def generate_ics():
    cal = Calendar()
    event = Event()
    event.add('summary', 'Studentfirande för Leopoldine & Zacharias')
    event.add('dtstart', PARTY_DATE)
    event.add('dtend', PARTY_END_DATE)
    event.add('location', 'Filmgatan 30, Solna')
    event.add('description', 'Välkommen att fira Leopoldine och Zacharias!')
    cal.add_component(event)
    return cal.to_ical()

# FRONTEND
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
<b>Vad:</b> 🎓 Utspring, Mottagning och Middag!
</div>
""", unsafe_allow_html=True)

ics = generate_ics()
st.download_button("📅 Ladda ner kalenderfil (.ics)", data=ics, file_name="studentfirande.ics", mime="text/calendar")

st.markdown("""
<div style='text-align: center; margin-top: 20px;'>
<a href="https://maps.google.com/?q=Filmgatan+30,+Solna" target="_blank">🗺️ Visa festplats på karta</a>
</div>
""", unsafe_allow_html=True)

# GÄSTLOGIN OCH RSVP
if "guest_authenticated" not in st.session_state:
    st.session_state.guest_authenticated = False

if not st.session_state.guest_authenticated:
    st.header("🎟️ Välkommen! Boka dina platser här!")
    st.success("Ange gästlösenordet för att OSA till festen! 🎉")
    guest_password = st.text_input("Gästlösenord", type="password")
    if guest_password == GUEST_PASSWORD:
        st.session_state.guest_authenticated = True
    elif guest_password:
        st.error("Fel lösenord. Försök igen.")

if st.session_state.guest_authenticated:
    st.header("🎉 OSA-Formulär")
    with st.form("OSA"):
        name = st.text_input("Ditt namn")
        email = st.text_input("Din e-postadress")
        party_size = st.number_input("Hur många personer i ert sällskap?", min_value=1, step=1)
        utspring = st.checkbox("Kommer du till Utspringet?")
        mottagning = st.checkbox("Kommer du till Mottagningen?")
        middag = st.checkbox("Kommer du äta Middag?")
        food_allergies = st.text_input("Matallergier eller specialkost?")
        submit_rsvp = st.form_submit_button("🎟️ Skicka OSA")

        if submit_rsvp:
            new_rsvp = {
                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Name": name,
                "Email": email,
                "Party Size": party_size,
                "Utspring": utspring,
                "Mottagning": mottagning,
                "Middag": middag,
                "Food Allergies": food_allergies
            }
            save_rsvp(new_rsvp)
            st.success("🎉 Tack för din OSA!")
            st.balloons()
            send_fancy_email(email, "Bekräftelse på din OSA", name)
            for admin in ADMIN_EMAILS:
                send_email(admin, "Ny OSA mottagen", f"Ny OSA från {name} ({email})")

            st.markdown("""
            <div style='text-align: center; font-size: 24px; color: #4BB543; margin-top: 30px;'>
            ✅ Din plats är bokad! Vi ser fram emot att fira med dig! 🎉
            </div>
            """, unsafe_allow_html=True)

# ADMINPANEL
admin_view = st.sidebar.radio("Admin-alternativ", ["Ingen", "Adminpanel"])
if admin_view == "Adminpanel":
    st.header("🔒 Adminpanel")
    password = st.text_input("Ange adminlösenord", type="password")
    if password == ADMIN_PASSWORD:
        st.success("Åtkomst beviljad ✅")
        rsvps = load_rsvps()
        st.dataframe(rsvps)

        if "Party Size" in rsvps.columns:
            total_guests = rsvps["Party Size"].sum()
            st.markdown(f"<h2 style='text-align: center; color: #6A0DAD;'>👥 Totalt anmälda: {total_guests} personer!</h2>", unsafe_allow_html=True)

        st.subheader("📊 OSA-Statistik")
        if all(col in rsvps.columns for col in ["Utspring", "Mottagning", "Middag"]):
            utspring_attending = rsvps[rsvps["Utspring"] == True]["Party Size"].sum()
            mottagning_attending = rsvps[rsvps["Mottagning"] == True]["Party Size"].sum()
            middag_attending = rsvps[rsvps["Middag"] == True]["Party Size"].sum()

            stats_df = pd.DataFrame({
                "Event": ["Utspring", "Mottagning", "Middag"],
                "Antal": [utspring_attending, mottagning_attending, middag_attending]
            })

            fig = px.pie(stats_df, names="Event", values="Antal", hole=0.4, title="Deltagande per event")
            st.plotly_chart(fig)

        st.download_button("📥 Ladda ner OSA-lista", rsvps.to_csv(index=False), file_name="osa_lista.csv")
    elif password:
        st.error("Fel lösenord. Försök igen.")