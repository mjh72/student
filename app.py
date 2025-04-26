import streamlit as st
import pandas as pd
import datetime

# -------------------------
# CONFIGURATION
# -------------------------
ADMIN_PASSWORD = "gradparty2025"
CSV_FILE = "rsvps.csv"

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
# APP LAYOUT
# -------------------------
st.set_page_config(page_title="Graduation Party 🎓", page_icon="🎉", layout="centered")

st.title("🎓 You're Invited to the Graduation Celebration!")
st.write("""
Welcome to the celebration of a big milestone!

**Please RSVP below** and let us know which events you'll join:
- 📚 School Graduation Ceremony
- 🍽️ Dinner
- 🏡 Open House Gathering

Also, let us know if you have any food allergies.
""")

view = st.sidebar.radio("Select view", ["Guest RSVP", "Admin Panel"])

# -------------------------
# GUEST RSVP FORM
# -------------------------
if view == "Guest RSVP":
    st.header("📋 RSVP Form")
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
                st.success("Thank you for your RSVP!")
                st.balloons()
            else:
                st.error("Please fill out at least your name and email!")

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

        st.download_button("Download RSVP list as CSV", rsvps.to_csv(index=False), file_name="rsvps.csv")

    elif password:
        st.error("Incorrect password. Try again.")

# -------------------------
# FOOTER
# -------------------------
with st.expander("ℹ️ About this app"):
    st.write("Built with ❤️ using Streamlit. Hosting free on Streamlit Community Cloud.")
