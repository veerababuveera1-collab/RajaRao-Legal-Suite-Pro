import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="RajaRao Legal Suite Pro v3.0", 
    page_icon="⚖️", 
    layout="wide"
)

# --- 2. LOGIN AUTHENTICATION SYSTEM ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='color: #d4af37; font-size: 3rem;'>🏛️ Legal Portal Access</h1>
            <p style='color: #888;'>Authorized Personnel Only</p>
        </div>
    """, unsafe_allow_html=True)
    
    # సెంటర్ అలైన్మెంట్ కోసం కాలమ్స్
    _, col, _ = st.columns([1, 1, 1])
    with col:
        with st.form("Login Form"):
            user = st.text_input("Username")
            pw = st.text_input("Password", type="password")
            submit = st.form_submit_button("Secure Login")
            
            if submit:
                # మీ యూజర్ నేమ్ మరియు పాస్‌వర్డ్ ఇక్కడ సెట్ చేసుకోండి
                if user == "advocate" and pw == "legal2026":
                    st.session_state.logged_in = True
                    st.success("Access Granted! Loading Vault...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid Credentials. Access Denied.")

# --- 3. MAIN APPLICATION LOGIC (Only if logged in) ---
if not st.session_state.logged_in:
    login()
else:
    # --- UI STYLING & DATA FETCHING ---
    st.markdown("""
        <style>
        .stApp { background: radial-gradient(circle at top right, #1e293b, #020617); color: #f8fafc; }
        .gold-title {
            background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            font-weight: 900; text-align: center; font-size: 3.5rem; margin-bottom: 0px;
        }
        .legal-card {
            background: rgba(255, 255, 255, 0.05); border-left: 5px solid #d4af37;
            padding: 20px; border-radius: 12px; margin-bottom: 20px;
        }
        .bns-badge { background: #d4af37; color: black; padding: 2px 10px; border-radius: 15px; font-weight: bold; }
        </style>
        """, unsafe_allow_html=True)

    # --- CLOUD DATA FETCH ---
    SHEET_ID = "1l2p3L1VeP3Hm2uiaYasq2NeZ2Dp-RPx2ZwEHeq1nJXM"
    CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

    @st.cache_data(ttl=60)
    def fetch_cloud_data():
        try:
            data = pd.read_csv(CSV_URL)
            data.columns = data.columns.str.strip()
            return data
        except:
            return pd.DataFrame()

    # --- SIDEBAR & LOGOUT ---
    with st.sidebar:
        st.markdown("<h1 style='color:#d4af37;'>🏛️ RAJARAO PRO</h1>", unsafe_allow_html=True)
        st.write(f"Logged in as: **Advocate**")
        menu = st.radio("Navigation:", ["📊 Dashboard", "📡 Court Tracker", "🤖 Nyaya AI (BNS)", "📂 Secure Vault"])
        st.divider()
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
        st.caption(f"System Active: {datetime.now().strftime('%H:%M:%S')}")

    # BNS LIBRARY
    bns_library = {
        "103": {"crime": "Murder (హత్య)", "ipc": "IPC 302", "punishment": "Death or Life", "notes": "Punishment for murder."},
        "111": {"crime": "Organized Crime", "ipc": "New", "punishment": "Life or Death", "notes": "Covers syndicates."},
        "304": {"crime": "Snatching", "ipc": "New", "punishment": "Up to 3 Years", "notes": "Chain snatching focus."},
        "351": {"crime": "Defamation", "ipc": "IPC 499", "punishment": "2 Years / Comm Service", "notes": "Community service added."}
    }

    # --- MODULES ---
    if menu == "📊 Dashboard":
        st.markdown("<div class='gold-title'>Practice Intelligence</div>", unsafe_allow_html=True)
        df = fetch_cloud_data()
        if not df.empty:
            c1, c2, c3 = st.columns(3)
            c1.metric("Live Cases", len(df))
            c2.metric("Knowledge Base", f"{len(bns_library)} Secs")
            c3.metric("Status", "Encrypted")
            st.dataframe(df, use_container_width=True, hide_index=True)

    elif menu == "📡 Court Tracker":
        st.subheader("📡 Real-time Tracking")
        case_id = st.text_input("Enter Case ID (Ex: WP 124/2026)")
        if st.button("Query Now"):
            df = fetch_cloud_data()
            match = df[df['Case_ID'].str.upper() == case_id.upper()] if not df.empty else pd.DataFrame()
            if not match.empty:
                res = match.iloc[0]
                st.markdown(f"<div class='legal-card'><h3>{res['Case_ID']}</h3><p>Next Hearing: <b style='color:red;'>{res['Next_Hearing']}</b></p></div>", unsafe_allow_html=True)

    elif menu == "🤖 Nyaya AI (BNS)":
        st.markdown("<div class='gold-title'>Nyaya AI Explorer</div>", unsafe_allow_html=True)
        query = st.text_input("Enter BNS Section (Ex: 103, 304, 351)")
        if query in bns_library:
            d = bns_library[query]
            st.markdown(f"<div class='legal-card'><span class='bns-badge'>BNS {query}</span><h2>{d['crime']}</h2><p><b>Old Law:</b> {d['ipc']}</p><p><b>Note:</b> {d['notes']}</p></div>", unsafe_allow_html=True)

    elif menu == "📂 Secure Vault":
        st.subheader("📂 Encryption Vault")
        up = st.file_uploader("Upload PDF", type=['pdf'])
        if up: st.success("Document Encrypted.")

    st.markdown("---")
    st.caption("© 2026 Advocate RajaRao | Enterprise Legal Suite")
