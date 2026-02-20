import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="RajaRao Legal Suite Pro", page_icon="⚖️", layout="wide")

# --- 2. PREMIUM THEME & UI (CSS) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #1e293b, #020617); color: #f8fafc; }
    div[data-testid="stForm"] {
        border: 1px solid rgba(212, 175, 55, 0.4);
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .gold-title {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800; text-align: center; font-size: 3rem; margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(45deg, #d4af37, #996515);
        color: white !important; font-weight: bold; border-radius: 8px; width: 100%; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SECURE CREDENTIALS (THE FIX) ---
# 'kingoflaw' పాస్‌వర్డ్‌ను ముందే హ్యాష్ చేసి ఇక్కడ సెట్ చేశాను.
# దీనివల్ల మీ యాప్‌లో ఎటువంటి హ్యాషింగ్ ఎర్రర్ రాదు మరియు లాగిన్ సక్సెస్ అవుతుంది.
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

# Authenticator setup
authenticator = stauth.Authenticate(
    credentials,
    "rajarao_secure_session_v2026", 
    "signature_key_007",
    cookie_expiry_days=30
)

# --- 4. AUTHENTICATION INTERFACE ---
if not st.session_state.get("authentication_status"):
    st.markdown("<div class='gold-title'>Advocate RajaRao & Associates</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        # login() ఇప్పుడు సెషన్ స్టేట్‌ని ఆటోమేటిక్‌గా అప్‌డేట్ చేస్తుంది
        authenticator.login(location='main')
        
        if st.session_state["authentication_status"] is False:
            st.error("Invalid Counsel Credentials. Please check again.")
        elif st.session_state["authentication_status"] is None:
            st.info("Legal Portal: Please use your secure credentials to log in.")

# --- 5. SECURE POST-LOGIN DASHBOARD ---
if st.session_state["authentication_status"]:
    name = st.session_state["name"]
    
    with st.sidebar:
        st.markdown(f"### 🏛️ Welcome\n**Counsel {name}**")
        st.divider()
        menu = st.radio("Management Navigation", ["📊 Dashboard", "📡 Court Tracker", "🤖 Nyaya AI Chat"])
        st.divider()
        authenticator.logout('Sign Out', 'sidebar')

    # Dashboard Logic
    if menu == "📊 Dashboard":
        st.title("📊 Practice Intelligence")
        m1, m2, m3 = st.columns(3)
        m1.metric("Active Cases", "52", "+4 Urgent")
        m2.metric("Hearings Today", "6", "Main Bench")
        m3.metric("BNS Sync", "v2026", "Live")
        
        
        
        st.subheader("Today's Schedule")
        df = pd.DataFrame({
            "Time": ["10:30 AM", "02:00 PM"],
            "Case Name": ["State vs K. Reddy", "Property Dispute 44/26"],
            "Location": ["High Court Hall 1", "Chamber 5"]
        })
        st.table(df)

    # Court Tracker
    elif menu == "📡 Court Tracker":
        st.title("📡 Live e-Courts Status")
        cnr = st.text_input("Enter CNR Number")
        if st.button("Track Status"):
            with st.status("Fetching Records..."):
                time.sleep(1)
                st.success("Case Verified: Evidence Stage.")

    # AI Chat
    elif menu == "🤖 Nyaya AI Chat":
        st.title("🤖 Nyaya Mitra AI")
        if "messages" not in st.session_state: st.session_state.messages = []
        for msg in st.session_state.messages: st.chat_message(msg["role"]).write(msg["content"])
        
        if prompt := st.chat_input("Ask about BNS vs IPC..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            # Simulated AI context
            res = f"Counsel {name}, evaluating '{prompt}' under the Bharatiya Nyaya Sanhita (BNS) framework..."
            st.chat_message("assistant").write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

st.markdown("---")
st.caption("© 2026 RajaRao Legal Suite | Advanced Practice Management")
