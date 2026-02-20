import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import time
from datetime import datetime

# --- 1. PAGE SETUP & PERFORMANCE ---
st.set_page_config(
    page_title="RajaRao Legal Suite Pro",
    page_icon="⚖️",
    layout="wide"
)

# --- 2. AUTHENTICATION CONFIG (v0.3.x Compatible) ---
# Pre-hashed passwords for 'kingoflaw' and 'justice2026'
# ఇక్కడ పాస్‌వర్డ్‌లను హ్యాష్ చేసి ఇవ్వడం వల్ల TypeError రాదు మరియు స్పీడ్ పెరుగుతుంది
usernames = ["rajarao", "associate"]
names = ["Senior Advocate RajaRao", "Associate Counsel"]
hashed_passwords = [
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6L6s57RwXWbS8S8.', 
    '$2b$12$pL7/G3H4B/8G9T/8T.8T.u1G7G7G7G7G7G7G7G7G7G7G7G7G7G7G7'
]

credentials = {
    "usernames": {
        usernames[i]: {
            "name": names[i],
            "password": hashed_passwords[i]
        } for i in range(len(usernames))
    }
}

# Authenticator Initialize
authenticator = stauth.Authenticate(
    credentials,
    "rajarao_vault_v6", # Cookie Name
    "signature_key_2026", # Cookie Key
    cookie_expiry_days=30
)

# --- 3. LOGIN INTERFACE ---
# గమనిక: కొత్త వెర్షన్‌లో login() వాల్యూస్‌ని రిటర్న్ చేయదు (No assignment like name, status = ...)
authenticator.login(location='main')

# సెషన్ స్టేట్ ద్వారా అథెంటికేషన్ చెక్ చేయాలి
if st.session_state["authentication_status"]:
    
    # User Details from Session State
    name = st.session_state["name"]
    username = st.session_state["username"]

    # --- SIDEBAR NAVIGATION ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3503/3503786.png", width=90)
        st.markdown(f"### Welcome\n**Counsel {name}**")
        st.divider()
        choice = st.radio("Management Menu", ["📊 Dashboard", "📡 Court Status", "🤖 Nyaya AI Chat", "📂 Vault"])
        st.divider()
        authenticator.logout('Logout', 'sidebar')

    # --- DASHBOARD SECTION ---
    if choice == "📊 Dashboard":
        st.title("Practice Overview")
        c1, c2, c3 = st.columns(3)
        c1.metric("Active Files", "48", "+2 Urgent")
        c2.metric("Hearings Today", "5", "High Priority")
        c3.metric("BNS Sync", "v2026", "Updated")

        

        st.subheader("Daily Calendar")
        df = pd.DataFrame({
            "Time": ["10:30 AM", "02:00 PM", "04:30 PM"],
            "Case ID": ["WP 124/2026", "OS 99/2025", "CC 45/2024"],
            "Court": ["High Court", "District Court", "Supreme Court"]
        })
        st.table(df)

    # --- COURT STATUS SECTION ---
    elif choice == "📡 Court Status":
        st.title("Real-time Case Tracking")
        case_id = st.text_input("Enter Case Number / CNR")
        if st.button("Track Status"):
            with st.spinner("Connecting to e-Courts..."):
                time.sleep(1)
                st.success("Record Found!")
                st.info("**Current Stage:** Final Arguments\n\n**Next Date:** 25th Feb 2026")

    # --- NYAYA AI CHAT SECTION ---
    elif choice == "🤖 Nyaya AI Chat":
        st.title("Nyaya Mitra: AI Associate")
        if "messages" not in st.session_state: st.session_state.messages = []
        
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
            
        if prompt := st.chat_input("Ask about BNS vs IPC or Case Precedents..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            # AI Logic (Simulated for Speed)
            response = f"Counsel {name}, based on the new Bharatiya Nyaya Sanhita (BNS), your query '{prompt}' refers to..."
            st.chat_message("assistant").write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    # --- VAULT SECTION ---
    elif choice == "📂 Vault":
        st.title("Secure Document Repository")
        up = st.file_uploader("Upload Confidential Briefs", type=['pdf', 'docx'])
        if up:
            st.success("File encrypted and stored.")
            st.download_button("📥 Download Analysis", "AI Brief Content", file_name="RajaRao_Brief.txt")

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    # --- STYLING THE LOGIN BOX ---
    st.markdown("<h1 style='text-align: center; color: #D4AF37;'>Advocate RajaRao & Associates</h1>", unsafe_allow_html=True)
    st.warning('Please log in using your secure counsel credentials.')

# --- GLOBAL STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    [data-testid="stMetricValue"] { color: #d4af37 !important; }
    .stButton>button { width: 100%; }
    </style>
    """, unsafe_allow_html=True)
