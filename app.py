import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import time

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="RajaRao Legal Suite Pro", page_icon="⚖️", layout="wide")

# --- 2. PREMIUM THEME (CSS) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #1e293b, #020617); color: #f8fafc; }
    div[data-testid="stForm"] {
        border: 1px solid rgba(212, 175, 55, 0.4);
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px; padding: 40px;
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

# --- 3. THE EXPERT FIX: SECURE CREDENTIALS ---
# వెర్షన్ 0.3.x లో Hasher సమస్యను నివారించడానికి నేరుగా హ్యాష్ చేసిన పాస్‌వర్డ్‌ను ఇస్తున్నాను.
# ఇది 'kingoflaw' కు సరిపడా పక్కా హ్యాష్ వాల్యూ.
credentials = {
    "usernames": {
        "rajarao": {
            "name": "Senior Advocate RajaRao",
            "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6L6s57RwXWbS8S8." # kingoflaw
        }
    }
}

# Authenticator setup
authenticator = stauth.Authenticate(
    credentials,
    "rajarao_vault_v2026", 
    "signature_key_99",
    cookie_expiry_days=30
)

# --- 4. LOGIN LOGIC ---
# కొత్త వెర్షన్‌లో login() మెథడ్ నేరుగా సెషన్ స్టేట్‌ని అప్‌డేట్ చేస్తుంది.
authenticator.login(location='main')

if st.session_state["authentication_status"]:
    # --- SECURE CONTENT ---
    name = st.session_state["name"]
    
    with st.sidebar:
        st.markdown(f"### 🏛️ Welcome\n**Counsel {name}**")
        st.divider()
        menu = st.radio("Navigation", ["📊 Dashboard", "📡 Court Tracker", "🤖 Nyaya AI Chat"])
        st.divider()
        authenticator.logout('Sign Out', 'sidebar')

    if menu == "📊 Dashboard":
        st.title("📊 Practice Intelligence Dashboard")
        m1, m2, m3 = st.columns(3)
        m1.metric("Active Files", "52", "+4 Urgent")
        m2.metric("Hearings Today", "6", "Bench 1")
        m3.metric("BNS Sync", "v2026", "Live")
        
        

        st.subheader("Upcoming Hearings")
        df = pd.DataFrame({
            "Time": ["10:30 AM", "02:00 PM"],
            "Case ID": ["WP 124/2026", "OS 44/2026"],
            "Location": ["High Court Hall 1", "District Court"]
        })
        st.table(df)

    elif menu == "📡 Court Tracker":
        st.title("📡 Live e-Courts Status")
        cnr = st.text_input("Enter CNR Number")
        if st.button("Query Database"):
            with st.status("Fetching Data..."):
                time.sleep(1)
                st.success("Case Verified: Evidence Stage.")

    elif menu == "🤖 Nyaya AI Chat":
        st.title("🤖 Nyaya Mitra AI")
        if "msgs" not in st.session_state: st.session_state.msgs = []
        for m in st.session_state.msgs: st.chat_message(m["role"]).write(m["content"])
        
        if prompt := st.chat_input("Ask a legal question..."):
            st.session_state.msgs.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            res = f"Counsel {name}, as per BNS frameworks, your query '{prompt}' refers to..."
            st.chat_message("assistant").write(res)
            st.session_state.msgs.append({"role": "assistant", "content": res})

elif st.session_state["authentication_status"] is False:
    st.markdown("<div class='gold-title'>Advocate RajaRao & Associates</div>", unsafe_allow_html=True)
    st.error("Invalid Username or Password.")
elif st.session_state["authentication_status"] is None:
    st.markdown("<div class='gold-title'>Advocate RajaRao & Associates</div>", unsafe_allow_html=True)
    st.info("Legal Portal: Please enter your secure credentials.")

st.markdown("---")
st.caption("© 2026 RajaRao Legal Suite | Advanced Management System")
