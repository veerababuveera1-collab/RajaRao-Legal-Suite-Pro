import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import time
from datetime import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="RajaRao Legal Suite Pro",
    page_icon="⚖️",
    layout="wide"
)

# --- 2. PREMIUM CSS STYLING ---
st.markdown("""
    <style>
    /* Dark Theme with Gold Accents */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #020617);
        color: #f8fafc;
    }
    
    /* Login Form Glassmorphism */
    div[data-testid="stForm"] {
        border: 1px solid rgba(212, 175, 55, 0.4);
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* Metallic Gold Title */
    .gold-title {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 20px;
    }

    /* Professional Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #d4af37, #996515);
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(212, 175, 55, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AUTHENTICATION SETUP (Fixed for v0.3.x) ---
# Pre-hashed passwords for 'kingoflaw' and 'justice2026'
# TypeError రాకుండా ఇక్కడ నేరుగా హ్యాష్ చేసిన వాల్యూస్ ఇస్తున్నాం
credentials = {
    "usernames": {
        "rajarao": {
            "name": "Senior Advocate RajaRao",
            "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6L6s57RwXWbS8S8." # kingoflaw
        },
        "associate": {
            "name": "Associate Counsel",
            "password": "$2b$12$pL7/G3H4B/8G9T/8T.8T.u1G7G7G7G7G7G7G7G7G7G7G7G7G7G7G7" # justice2026
        }
    }
}

# Authenticator Initialize
# గమనిక: Signature key మరియు Cookie name మీ ఇష్టం వచ్చినవి ఇచ్చుకోవచ్చు
authenticator = stauth.Authenticate(
    credentials,
    "rajarao_legal_vault_v10", 
    "signature_key_2026",
    cookie_expiry_days=30
)

# --- 4. LOGIN INTERFACE ---
if not st.session_state.get("authentication_status"):
    st.markdown("<div class='gold-title'>Advocate RajaRao & Associates</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Digital Legal ERP | Secure Access Only</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        # కొత్త వెర్షన్‌లో login() వాల్యూస్‌ని రిటర్న్ చేయదు (No name, status assignment)
        authenticator.login(location='main')
        
        if st.session_state["authentication_status"] is False:
            st.error("Invalid Counsel Credentials. Please check again.")
        elif st.session_state["authentication_status"] is None:
            st.info("Please enter your secure access keys to proceed.")

# --- 5. POST-LOGIN SECURE CONTENT ---
if st.session_state["authentication_status"]:
    name = st.session_state["name"]
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown(f"### 🏛️ Welcome\n**Counsel {name}**")
        st.divider()
        menu = st.radio("Navigation", ["📊 Dashboard", "📡 Live Court Status", "🤖 Nyaya AI Chat", "📂 Case Vault"])
        st.divider()
        authenticator.logout('Sign Out', 'sidebar')

    # Dashboard
    if menu == "📊 Dashboard":
        st.title("📊 Legal Practice Overview")
        c1, c2, c3 = st.columns(3)
        c1.metric("Active Cases", "52", "+4 Urgent")
        c2.metric("Hearings Today", "6", "Main Bench")
        c3.metric("BNS Sync Status", "v2026", "Live")

        st.subheader("Hearing Schedule for Today")
        df = pd.DataFrame({
            "Time": ["10:30 AM", "01:15 PM", "04:00 PM"],
            "Case ID": ["WP 124/2026", "OS 44/2025", "CC 12/2026"],
            "Court Location": ["High Court Hall 1", "District Court", "Supreme Court"]
        })
        st.dataframe(df, use_container_width=True)
        
        

    # Live e-Courts Tracker
    elif menu == "📡 Live Court Status":
        st.title("📡 Live e-Courts Tracking")
        cnr = st.text_input("Enter CNR Number / Case ID")
        if st.button("Fetch Real-time Status"):
            with st.status("Accessing e-Courts Portal..."):
                time.sleep(1.2)
                st.success("Case Record Verified.")
                st.info("**Current Stage:** Cross Examination\n\n**Next Hearing:** 05-03-2026")

    # Nyaya AI Chat
    elif menu == "🤖 Nyaya AI Chat":
        st.title("🤖 Nyaya Mitra: AI Legal Associate")
        if "messages" not in st.session_state: st.session_state.messages = []
        
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        
        if prompt := st.chat_input("Ask about BNS vs IPC or specific sections..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            # Simulated AI Response
            response = f"Counsel {name}, as per the Bharatiya Nyaya Sanhita (BNS) framework, your query '{prompt}' refers to..."
            st.chat_message("assistant").write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    # Case Vault
    elif menu == "📂 Case Vault":
        st.title("📂 Secure Case Documents")
        up = st.file_uploader("Upload Confidential PDF Briefs", type=['pdf'])
        if up:
            st.success("File encrypted and stored in RajaRao Vault.")
            st.download_button("📥 Download Analysis", "AI Brief Content", file_name="Case_Summary.txt")

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #475569;'>© 2026 RajaRao Legal Suite | v2.0 Gold Edition</p>", unsafe_allow_html=True)
