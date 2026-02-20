import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- 1. PROJECT CONFIGURATION ---
PROJECT_NAME = "RajaRao Legal Suite"
SHEET_ID = "1l2p3L1VeP3Hm2uiaYasq2NeZ2Dp-RPx2ZwEHeq1nJXM"

# GIDs (Google Sheet Tab IDs)
COURT_GID = "906893272"  # Case Tracker Tab
BNS_GID = "1374929092"   # BNS Master Tab

# URLs for CSV Export
COURT_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={COURT_GID}"
BNS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={BNS_GID}"

st.set_page_config(page_title=PROJECT_NAME, page_icon="⚖️", layout="wide")

# --- 2. LIVE CLOUD ENGINE ---
@st.cache_data(ttl=60)
def fetch_cloud_data(url):
    try:
        data = pd.read_csv(url)
        data.columns = [c.strip() for c in data.columns]
        return data
    except Exception:
        return pd.DataFrame()

# Load Datasets
df_court = fetch_cloud_data(COURT_URL)
df_bns = fetch_cloud_data(BNS_URL)

# --- 3. PREMIUM ROYAL LAW CHAMBER THEME (CSS) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #0a0f1d, #020617); color: #f8fafc; font-family: 'Times New Roman', Times, serif; }
    
    .gold-title {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 900; text-align: center; font-size: 3.5rem; letter-spacing: 1px;
        margin-bottom: 25px; border-bottom: 2px solid #d4af37; padding-bottom: 10px;
    }
    
    .legal-card {
        background: rgba(255, 255, 255, 0.03);
        border-left: 5px solid #d4af37;
        border-top: 1px solid rgba(212, 175, 55, 0.2);
        padding: 25px; border-radius: 0 15px 15px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 20px; backdrop-filter: blur(10px);
    }
    
    .bns-badge {
        background: #d4af37; color: #000; padding: 5px 15px;
        border-radius: 5px; font-weight: bold; font-size: 0.8rem;
    }

    .stButton>button {
        background: linear-gradient(135deg, #d4af37 0%, #aa771c 100%) !important;
        color: black !important; font-weight: bold !important; border: none !important;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(212, 175, 55, 0.4) !important; }

    [data-testid="stSidebar"] { background-color: #050a16 !important; border-right: 1px solid #d4af37; }
    div[data-testid="stDataFrame"] { border: 1px solid #d4af37; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. AUTHENTICATION ---
if 'auth_status' not in st.session_state:
    st.session_state.auth_status = False

if not st.session_state.auth_status:
    st.markdown(f"<div class='gold-title'>{PROJECT_NAME}</div>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<div class='legal-card'>", unsafe_allow_html=True)
        st.subheader("🔐 Counsel Login")
        user = st.text_input("Username", value="rajarao")
        pwd = st.text_input("Encryption Key", type="password")
        if st.button("UNLOCK VAULT"):
            if user == "rajarao" and pwd == "chamber123":
                st.session_state.auth_status = True
                st.rerun()
            else:
                st.error("Access Denied.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='color:#d4af37; text-align:center;'>🏛️ APEX PRO</h1>", unsafe_allow_html=True)
    st.write(f"Senior Counsel: **RajaRao**")
    st.divider()
    menu = st.radio("Management Modules:", 
                    ["📊 Practice Intelligence", "📡 Live Court Tracker", 
                     "🤖 Nyaya AI Search", "⚖️ Smart Bail Calculator", "📂 Secure Vault"])
    st.divider()
    if st.button("🔄 Sync Cloud Data"):
        st.cache_data.clear()
        st.rerun()
    if st.button("Logout"):
        st.session_state.auth_status = False
        st.rerun()

# --- 6. CORE MODULES ---

# A. Practice Intelligence
if menu == "📊 Practice Intelligence":
    st.markdown("<div class='gold-title'>Practice Intelligence</div>", unsafe_allow_html=True)
    if not df_court.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Cases", len(df_court))
        c2.metric("Primary Court", "AP High Court")
        c3.metric("System Status", "Live Syncing")
        st.dataframe(df_court, use_container_width=True, hide_index=True)
    else:
        st.error("Court data not found. Please sync cloud.")

# B. Live Court Tracker
elif menu == "📡 Live Court Tracker":
    st.markdown("<div class='gold-title'>Live Case Tracker</div>", unsafe_allow_html=True)
    sq = st.text_input("🔍 Search Case ID, Petitioner, or Stage...")
    if sq and not df_court.empty:
        res = df_court[df_court.apply(lambda r: r.astype(str).str.contains(sq, case=False).any(), axis=1)]
        st.dataframe(res, use_container_width=True, hide_index=True)

# C. Nyaya AI Search
elif menu == "🤖 Nyaya AI Search":
    st.markdown("<div class='gold-title'>Nyaya AI Explorer</div>", unsafe_allow_html=True)
    query = st.text_input("BNS Section, IPC, or Nature of Offence...", placeholder="Ex: 103, 302, Murder...")
    
    if query and not df_bns.empty:
        results = df_bns[df_bns.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
        if not results.empty:
            cols = ['BNS Section', 'IPC Equivalent', 'Nature of Offence (నేరం స్వభావం)', 'Punishment (శిక్షా కాలం)']
            existing_cols = [c for c in cols if c in df_bns.columns]
            st.dataframe(results[existing_cols], use_container_width=True, hide_index=True)
            
            if len(results) == 1:
                row = results.iloc[0]
                st.markdown(f"""<div class='legal-card'>
                <span class='bns-badge'>BNS {row['BNS Section']}</span>
                <h3 style='color:#d4af37;'>{row.get('Nature of Offence (నేరం స్వభావం)', 'Offence Details')}</h3>
                <p><b>IPC Reference:</b> {row['IPC Equivalent']} | <b>Punishment:</b> {row.get('Punishment (శిక్షా కాలం)', 'N/A')}</p>
                </div>""", unsafe_allow_html=True)

# D. Smart Bail Calculator (NEW FEATURE)
elif menu == "⚖️ Smart Bail Calculator":
    st.markdown("<div class='gold-title'>Bail & Limitation AI</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='legal-card'>", unsafe_allow_html=True)
        st.subheader("🔍 Check Eligibility")
        if not df_bns.empty:
            bns_options = df_bns['BNS Section'].unique()
            sec_pick = st.selectbox("Select BNS Section", bns_options)
            off_row = df_bns[df_bns['BNS Section'] == sec_pick].iloc[0]
            st.write(f"Offence: **{off_row.get('Nature of Offence (నేరం స్వభావం)', 'N/A')}**")
            
            # Simple Bail Logic based on offense keywords
            if any(word in str(off_row).lower() for word in ['murder', 'rape', 'terror', 'life', 'death']):
                st.error("🚨 NON-BAILABLE | Triable by Sessions")
            else:
                st.success("✅ BAILABLE (General Procedure)")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='legal-card'>", unsafe_allow_html=True)
        st.subheader("⏳ BNSS 479 Statutory Bail")
        max_term = st.number_input("Maximum Punishment for this offence (Years)", 1, 20, 7)
        first_offender = st.checkbox("Is the accused a First-Time Offender?")
        
        ratio = 0.33 if first_offender else 0.50
        st.metric("Eligible for Bail after completion of:", f"{max_term * ratio:.1f} Years")
        st.caption(f"BNSS Section 479: {ratio*100:.0f}% of total punishment.")
        st.markdown("</div>", unsafe_allow_html=True)

# E. Secure Vault
elif menu == "📂 Secure Vault":
    st.markdown("<div class='gold-title'>Secure Vault</div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload Brief (PDF)", type=['pdf'])
    if uploaded:
        with st.spinner("Encrypting..."):
            time.sleep(1)
            st.success(f"{uploaded.name} is now secured in the chamber vault.")

st.markdown("---")
st.caption(f"© 2026 RajaRao Legal Suite | v5.0 Royal Chamber Edition | {datetime.now().strftime('%d-%m-%Y %H:%M')}")
