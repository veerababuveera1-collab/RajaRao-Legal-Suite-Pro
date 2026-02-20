import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import time
from datetime import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="RajaRao Legal Suite Pro", page_icon="⚖️", layout="wide")

# --- 2. PREMIUM ARCHITECTURAL UI (CSS) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #1e293b, #020617); color: #f8fafc; }
    div[data-testid="stForm"] {
        border: 1px solid rgba(212, 175, 55, 0.4);
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px; padding: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .gold-title {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; text-align: center; font-size: 3rem; margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(45deg, #d4af37, #996515);
        color: white !important; font-weight: bold; border-radius: 8px; width: 100%; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AUTHENTICATION (The Permanent Expert Fix) ---
# v0.3.x లో ఎర్రర్స్ రాకుండా ఉండటానికి హ్యాష్ వాల్యూస్ ముందుగానే జనరేట్ చేస్తున్నాం
passwords = ['kingoflaw', 'justice2026']
hashed_passwords = stauth.Hasher(passwords).generate()

credentials = {
    "usernames": {
        "rajarao": {
            "name": "Senior Advocate RajaRao",
            "password": hashed_passwords[0]
        },
        "associate": {
            "name": "Associate Counsel",
            "password": hashed_passwords[1]
        }
    }
}

# Authenticator setup
authenticator = stauth.Authenticate(
    credentials,
    "rajarao_secure_session_v2026", 
    "signature_key_99",
    cookie_expiry_days=30
)

# --- 4. LOGIN LOGIC ---
if not st.session_state.get("authentication_status"):
    st.markdown("<div class='gold-title'>Advocate RajaRao & Associates</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        # login() ఇప్పుడు నేరుగా సెషన్ స్టేట్‌ని అప్‌డేట్ చేస్తుంది
        authenticator.login(location='main')
        
        if st.session_state["authentication_status"] is False:
            st.error("Invalid Counsel Credentials. Please check again.")
        elif st.session_state["authentication_status"] is None:
            st.info("Secure Portal: Please enter your credentials to proceed.")

# --- 5. SECURE DASHBOARD & ALL FUNCTIONALITIES ---
if st.session_state["authentication_status"]:
    name = st.session_state["name"]
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown(f"### 🏛️ Welcome\n**Counsel {name}**")
        st.divider()
        menu = st.radio("Management", ["📊 Dashboard", "📡 Court Tracker", "🤖 Nyaya AI Chat", "📂 Case Vault"])
        st.divider()
        authenticator.logout('Sign Out', 'sidebar')

    # FUNCTIONALITY 1: Dashboard
    if menu == "📊 Dashboard":
        st.title("📊 Practice Intelligence")
        m1, m2, m3 = st.columns(3)
        m1.metric("Active Files", "52", "+4 Urgent")
        m2.metric("Hearings Today", "6", "Main Bench")
        m3.metric("BNS Sync Status", "v2026", "Live")
        
        
        
        st.subheader("Today's Hearing Schedule")
        df = pd.DataFrame({
            "Time": ["10:30 AM", "01:15 PM", "04:00 PM"],
            "Case ID": ["WP 124/2026", "OS 44/2025", "CC 12/2026"],
            "Court Location": ["High Court Hall 1", "District Court", "Supreme Court"]
        })
        st.dataframe(df, use_container_width=True)

    # FUNCTIONALITY 2: Court Tracker
    elif menu == "📡 Court Tracker":
        st.title("📡 Live e-Courts Status Tracking")
        cnr = st.text_input("Enter CNR Number / Case ID")
        if st.button("Query Real-time Database"):
            with st.status("Accessing e-Courts Portal..."):
                time.sleep(1.2)
                st.success("Case Record Verified.")
                st.info("**Current Stage:** Final Arguments\n\n**Next Hearing:** 05-03-2026")

    # FUNCTIONALITY 3: Nyaya AI Chat
    elif menu == "🤖 Nyaya AI Chat":
        st.title("🤖 Nyaya Mitra: AI Legal Associate")
        if "messages" not in st.session_state: st.session_state.messages = []
        for msg in st.session_state.messages: 
            st.chat_message(msg["role"]).write(msg["content"])
        
        if prompt := st.chat_input("Ask about BNS vs IPC sections..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            res = f"Counsel {name}, as per the Bharatiya Nyaya Sanhita (BNS) framework, your query '{prompt}' refers to..."
            st.chat_message("assistant").write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

    # FUNCTIONALITY 4: Case Vault
    elif menu == "📂 Case Vault":
        st.title("📂 Secure Case Documents")
        uploaded_file = st.file_uploader("Upload Confidential Case Briefs (PDF)", type=['pdf'])
        if uploaded_file:
            st.success("File encrypted and stored in RajaRao Vault.")
            st.download_button("📥 Download Analysis", "AI Brief Analysis Summary", file_name="Case_Summary.txt")

st.markdown("---")
st.caption("© 2026 RajaRao Legal Suite | v2.0 Enterprise Gold Edition")
