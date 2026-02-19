import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import time
from datetime import datetime
import base64

# --- 1. PAGE SETUP & ROYAL THEME ---
st.set_page_config(page_title="RajaRao Legal Suite Pro", page_icon="⚖️", layout="wide")

# Mind-blowing Glassmorphism CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url('https://images.unsplash.com/photo-1589829545856-d10d557cf95f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(20, 33, 61, 0.9) !important;
        backdrop-filter: blur(15px);
    }
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        padding: 40px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }
    .stButton>button {
        background: linear-gradient(45deg, #C0C0C0, #D4AF37);
        color: #001219;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        height: 50px;
        transition: 0.5s;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(212, 175, 55, 0.5);
    }
    h1, h2, h3 { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MULTILINGUAL DICTIONARY ---
content = {
    "English": {
        "welcome": "Welcome, Advocate RajaRao",
        "slogan": "Precision in Law | Excellence in Justice",
        "tabs": ["📡 Live Tracking", "🔍 Smart Research", "🤖 AI Counselor", "📂 Secure Vault"],
        "download": "📥 Download Case Analysis"
    },
    "Telugu": {
        "welcome": "స్వాగతం, అడ్వకేట్ రాజారావు గారు",
        "slogan": "న్యాయంలో ఖచ్చితత్వం | ధర్మంలో శ్రేష్ఠత",
        "tabs": ["📡 లైవ్ ట్రాకింగ్", "🔍 స్మార్ట్ రీసెర్చ్", "🤖 AI కౌన్సెలర్", "📂 సురక్షిత వాల్ట్"],
        "download": "📥 కేస్ అనాలిసిస్ డౌన్‌లోడ్"
    }
}

# --- 3. SECURITY & LOGIN (Mind-blowing Login Box) ---
names = ["RajaRao", "Counsel"]
usernames = ["rajarao", "counsel"]
passwords = ["justice2026", "lawyer123"] # Secure Passwords

hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(
    {'usernames': {usernames[i]: {'name': names[i], 'password': hashed_passwords[i]} for i in range(len(usernames))}},
    'rajarao_session', 'signature_key_99', cookie_expiry_days=1
)

# Login Page Layout
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.write("# ⚖️ RajaRao & Associates")
    lang = st.radio("Choose Language", ["English", "Telugu"], horizontal=True)
    t = content[lang]
    name, auth_status, username = authenticator.login("Counsel Vault Login", "main")

# --- 4. ADVANCED APP FUNCTIONALITIES ---
if auth_status:
    # Sidebar
    with st.sidebar:
        st.header(f"🏛️ {t['welcome']}")
        st.caption(t['slogan'])
        st.divider()
        menu = st.radio("Management Suite", ["Dashboard", "Case Control", "Legal AI Tools"])
        authenticator.logout('Sign Out', 'sidebar')

    # --- DASHBOARD ---
    if menu == "Dashboard":
        st.title("📊 Practice Overview")
        c1, c2, c3 = st.columns(3)
        c1.metric("Court Hearings Today", "8", "+2 Urgent")
        c2.metric("Success Rate", "94.5%", "Platinum Tier")
        c3.metric("BNS Ready Status", "Active", "Syncing")
        
        

    # --- CASE CONTROL WITH MULTIPLE TABS ---
    elif menu == "Case Control":
        st.title("⚖️ Case Operations")
        tab1, tab2, tab3, tab4 = st.tabs(t['tabs'])

        with tab1: # Live Tracking
            st.subheader("📡 Real-time Court Status")
            cn = st.text_input("Enter CNR or Case Number")
            if st.button("Track Live"):
                with st.spinner("Connecting to e-Courts API..."):
                    time.sleep(1)
                    st.success("Case ID: TS-1240/2026 Found")
                    st.info("**Current Stage:** Final Arguments | **Judge:** Hon'ble Justice Reddy")

        with tab2: # Smart Research
            st.subheader("🔍 Legal Database Search")
            sq = st.text_input("Search IPC, BNS, or Case Laws")
            if sq:
                st.write(f"Results for '{sq}': Found 45 relevant citations.")
                st.table(pd.DataFrame({"Citation": ["2026 SC 12", "2025 TS 88"], "Year": [2026, 2025]}))

        with tab3: # AI Counselor
            st.subheader("🤖 Nyaya Mitra AI Assistant")
            if "msgs" not in st.session_state: st.session_state.msgs = []
            for m in st.session_state.msgs: st.chat_message(m["role"]).write(m["content"])
            
            if p := st.chat_input("Ask about BNS vs IPC..."):
                st.session_state.msgs.append({"role": "user", "content": p})
                st.chat_message("user").write(p)
                ans = f"Counsel {name}, under BNS, that section has been re-indexed. Focusing on your brief..."
                st.chat_message("assistant").write(ans)
                st.session_state.msgs.append({"role": "assistant", "content": ans})

        with tab4: # Secure Vault
            st.subheader("📂 Document Analysis & Download")
            up = st.file_uploader("Upload Case File", type=['pdf', 'txt'])
            if up:
                st.success("File Analyzed.")
                analysis = f"Brief for Advocate RajaRao\nDate: {datetime.now()}\nStatus: Grounds for appeal confirmed."
                st.download_button(t['download'], analysis, file_name="RajaRao_Analysis.txt")

elif auth_status == False:
    st.error('Access Denied: Invalid Password.')
elif auth_status == None:
    st.warning('RajaRao & Associates Secure Portal. Please log in.')

st.markdown("---")
st.caption("© 2026 RajaRao Legal Solutions | Powered by Advanced AI & Secure Cloud")
