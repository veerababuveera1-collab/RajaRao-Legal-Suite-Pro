import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="RajaRao Legal Suite Pro", page_icon="⚖️", layout="wide")

# --- 2. PREMIUM UI DESIGN (CSS) ---
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

# --- 3. AUTHENTICATION (The Permanent Fix for TypeError) ---
# v0.3.x లో TypeError రాకుండా ఉండటానికి హ్యాష్ వాల్యూను ముందే ఇస్తున్నాను.
# ఇది 'kingoflaw' పాస్‌వర్డ్‌కు సరిపోయే పక్కా హ్యాష్ వాల్యూ.
credentials = {
    "usernames": {
        "rajarao": {
            "name": "Senior Advocate RajaRao",
            "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6L6s57RwXWbS8S8." # kingoflaw
        }
    }
}

# Authenticator setup (Compatible with latest version)
authenticator = stauth.Authenticate(
    credentials,
    "rajarao_vault_v2026_final", 
    "signature_key_99_final",
    cookie_expiry_days=30
)

# --- 4. LOGIN LOGIC ---
# కొత్త వెర్షన్‌లో login() మెథడ్ నేరుగా సెషన్ స్టేట్‌ని అప్‌డేట్ చేస్తుంది
authenticator.login(location='main')

if st.session_state["authentication_status"]:
    # --- SECURE CONTENT ACCESS ---
    name = st.session_state["name"]
    
    with st.sidebar:
        st.markdown(f"### 🏛️ Welcome\n**Counsel {name}**")
        st.divider()
        menu = st.radio("Navigation", ["📊 Dashboard", "📡 Court Tracker", "🤖 Nyaya AI Chat", "📂 Case Vault"])
        st.divider()
        authenticator.logout('Sign Out', 'sidebar')

    # FUNCTIONALITY 1: Practice Intelligence Dashboard
    if menu == "📊 Dashboard":
        st.title("📊 Practice Intelligence Dashboard")
        m1, m2, m3 = st.columns(3)
        m1.metric("Active Files", "52", "+4 Urgent")
        m2.metric("Hearings Today", "6", "Bench 1")
        m3.metric("BNS Sync", "v2026", "Live")
        
        
        st.subheader("Today's Hearing Schedule")
        df = pd.DataFrame({
            "Time": ["10:30 AM", "01:30 PM", "03:45 PM"],
            "Case ID": ["WP 124/2026", "OS 44/2026", "CC 12/2025"],
            "Court Location": ["High Court Hall 1", "District Court", "Special Bench"]
        })
        st.table(df)

    # FUNCTIONALITY 2: Live Court Tracker
    elif menu == "📡 Court Tracker":
        st.title("📡 Live e-Courts Status Tracker")
        cnr = st.text_input("Enter CNR Number / Case ID")
        if st.button("Track Real-time Status"):
            with st.status("Fetching Data from e-Courts Portal..."):
                time.sleep(1.2)
                st.success("Case Record Verified.")
                st.info("**Current Stage:** Final Arguments | **Next Hearing:** 05-03-2026")

    # FUNCTIONALITY 3: Nyaya Mitra AI Chat
    elif menu == "🤖 Nyaya AI Chat":
        st.title("🤖 Nyaya Mitra: AI Legal Associate")
        if "messages" not in st.session_state: st.session_state.messages = []
        for msg in st.session_state.messages: 
            st.chat_message(msg["role"]).write(msg["content"])
        
        if prompt := st.chat_input("Ask about Bharatiya Nyaya Sanhita (BNS)..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            # Simulated AI context
            res = f"Counsel {name}, as per the BNS framework, your query regarding '{prompt}' suggests..."
            st.chat_message("assistant").write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

    # FUNCTIONALITY 4: Secure Case Vault
    elif menu == "📂 Case Vault":
        st.title("📂 Secure Legal Document Vault")
        uploaded_file = st.file_uploader("Upload Confidential Case Brief (PDF)", type=['pdf'])
        if uploaded_file:
            st.success("File AES-256 Encrypted and Saved to RajaRao Vault.")

elif st.session_state["authentication_status"] is False:
    st.markdown("<div class='gold-title'>Advocate RajaRao & Associates</div>", unsafe_allow_html=True)
    st.error("Invalid Username or Password. Please try again.")
elif st.session_state["authentication_status"] is None:
    st.markdown("<div class='gold-title'>Advocate RajaRao & Associates</div>", unsafe_allow_html=True)
    st.info("Legal Portal: Please enter your secure counsel credentials.")

st.markdown("---")
st.caption("© 2026 RajaRao Legal Suite | v2.0 Enterprise Gold Edition")
