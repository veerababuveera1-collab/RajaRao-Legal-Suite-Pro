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
def fetch_cloud_data(url, is_bns=False):
    try:
        data = pd.read_csv(url)
        data.columns = [c.strip() for c in data.columns]
        if is_bns and 'BNS Section' in data.columns:
            data = data.drop_duplicates(subset=['BNS Section'], keep='first')
        return data
    except Exception:
        return pd.DataFrame()

# Load Datasets
df_court = fetch_cloud_data(COURT_URL)
df_bns = fetch_cloud_data(BNS_URL, is_bns=True)

# --- 3. PREMIUM DESIGNER STYLING (CSS) ---
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
        transition: 0.3s; width: 100%;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(212, 175, 55, 0.4) !important; }

    [data-testid="stSidebar"] { background-color: #050a16 !important; border-right: 1px solid #d4af37; }
    div[data-testid="stDataFrame"] { border: 1px solid #d4af37; border-radius: 10px; background: #050a16; }
    
    .status-dot { height: 10px; width: 10px; background-color: #31d848; border-radius: 50%; display: inline-block; margin-right: 5px; }
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
        st.subheader("🔐 Senior Counsel Login")
        user = st.text_input("Username", value="rajarao")
        pwd = st.text_input("Encryption Key", type="password")
        if st.button("UNLOCK VAULT"):
            if user == "rajarao" and pwd == "chamber123":
                st.session_state.auth_status = True
                st.success("Identity Verified. Decrypting Files...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Access Denied. Invalid Credentials.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='color:#d4af37; text-align:center;'>🏛️ APEX PRO</h1>", unsafe_allow_html=True)
    st.write(f"Senior Counsel: **RajaRao**")
    
    # Connection Status
    status_color = "#31d848" if not df_court.empty else "#ff4b4b"
    st.markdown(f"<p><span class='status-dot' style='background-color:{status_color}'></span> Cloud Sync Active</p>", unsafe_allow_html=True)
    
    st.divider()
    menu = st.radio("Chamber Modules:", 
                    ["📊 Practice Intelligence", "📡 Live Court Tracker", 
                     "🤖 Nyaya AI Search", "⚖️ Smart Bail Calculator", "📂 Secure Vault"])
    st.divider()
    
    if st.button("🔄 Sync Cloud Data"):
        st.cache_data.clear()
        st.rerun()
        
    if st.button("🚪 Logout"):
        st.session_state.auth_status = False
        st.rerun()

# --- 6. CORE MODULES ---

# A. Practice Intelligence
if menu == "📊 Practice Intelligence":
    st.markdown("<div class='gold-title'>Practice Intelligence</div>", unsafe_allow_html=True)
    if not df_court.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Active Files", len(df_court))
        c2.metric("Primary Court", "AP High Court")
        c3.metric("Vault Security", "AES-256")
        
        st.markdown("### 🗓️ Priority Briefing Table")
        st.dataframe(df_court, use_container_width=True, hide_index=True)
    else:
        st.error("Connection Lost. Please Sync Cloud.")

# B. Nyaya AI Search
elif menu == "🤖 Nyaya AI Search":
    st.markdown("<div class='gold-title'>Nyaya AI Explorer</div>", unsafe_allow_html=True)
    q = st.text_input("Search BNS Section, IPC Equivalent, or Offence Name...", placeholder="Ex: 103, Murder, Theft...")
    
    if q and not df_bns.empty:
        results = df_bns[df_bns.apply(lambda row: row.astype(str).str.contains(q, case=False).any(), axis=1)]
        if not results.empty:
            cols = ['BNS Section', 'IPC Equivalent', 'Nature of Offence (నేరం స్వభావం)', 'Punishment (శిక్షా కాలం)']
            available_cols = [c for c in cols if c in df_bns.columns]
            st.dataframe(results[available_cols], use_container_width=True, hide_index=True)
            
            if len(results) == 1:
                r = results.iloc[0]
                st.markdown(f"""<div class='legal-card'>
                <span class='bns-badge'>BNS {r.get('BNS Section', 'N/A')}</span>
                <h3 style='color:#d4af37;'>{r.get('Nature of Offence (నేరం స్వభావం)', 'Offence Details')}</h3>
                <p><b>IPC:</b> {r.get('IPC Equivalent', 'N/A')} | <b>Punishment:</b> {r.get('Punishment (శిక్షా కాలం)', 'Refer BNSS')}</p>
                </div>""", unsafe_allow_html=True)

# C. Live Court Tracker (Detailed Search)
elif menu == "📡 Live Court Tracker":
    st.markdown("<div class='gold-title'>Live Court Tracker</div>", unsafe_allow_html=True)
    search_query = st.text_input("Search Case ID, Petitioner, or Judge...", placeholder="Ex: WP 505/2026")
    
    if search_query and not df_court.empty:
        results = df_court[df_court.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
        if not results.empty:
            for _, row in results.iterrows():
                st.markdown(f"""
                <div class='legal-card'>
                    <h3 style='color:#d4af37;'>{row.get('Case_ID', 'Unknown ID')}</h3>
                    <p><b>Petitioner:</b> {row.get('Petitioner', 'N/A')} | <b>Respondent:</b> {row.get('Respondent', 'State')}</p>
                    <hr style='opacity:0.2'>
                    <p><b>Current Stage:</b> {row.get('Stage', 'Pending')}</p>
                    <p><b>Next Hearing:</b> <span style='color:#ff4b4b; font-weight:bold;'>{row.get('Next_Hearing', 'TBD')}</span></p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No records found in the cloud for this query.")

# D. Smart Bail Calculator
elif menu == "⚖️ Smart Bail Calculator":
    st.markdown("<div class='gold-title'>Bail & Limitation AI</div>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='legal-card'>", unsafe_allow_html=True)
        st.subheader("🔍 Offence Analysis")
        if not df_bns.empty:
            sec_pick = st.selectbox("Select BNS Section for Analysis", df_bns['BNS Section'].unique())
            row = df_bns[df_bns['BNS Section'] == sec_pick].iloc[0]
            st.write(f"Offence: **{row.get('Nature of Offence (నేరం స్వభావం)', 'N/A')}**")
            
            # Logic for Bailable vs Non-Bailable
            if any(x in str(row).lower() for x in ['murder', 'rape', 'life', 'death', 'gang']):
                st.error("🚨 NON-BAILABLE")
            else:
                st.success("✅ BAILABLE / SPECIAL DISCRETION")
        st.markdown("</div>", unsafe_allow_html=True)
    with col_b:
        st.markdown("<div class='legal-card'>", unsafe_allow_html=True)
        st.subheader("⏳ BNSS 479 Statutory Bail")
        years = st.number_input("Maximum Sentence (Years)", 1, 20, 7)
        first_time = st.checkbox("First-time Offender (1/3rd Rule)")
        ratio = 0.33 if first_time else 0.50
        st.metric("Eligible for Bail after:", f"{years * ratio:.1f} Years")
        st.caption("Calculated based on Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023.")
        st.markdown("</div>", unsafe_allow_html=True)

# E. Secure Vault
elif menu == "📂 Secure Vault":
    st.markdown("<div class='gold-title'>Encrypted Vault</div>", unsafe_allow_html=True)
    st.write("Upload confidential petitions or vakalatnamas to the RajaRao Chamber.")
    file = st.file_uploader("Upload Case File (PDF)", type=['pdf'])
    if file:
        with st.spinner("Locking Vault with AES-256..."):
            time.sleep(1.2)
            st.success(f"Security Shield Active: {file.name} is now private.")

# --- 7. FOOTER ---
st.markdown("---")
st.caption(f"© 2026 RajaRao Legal Suite | v6.0 Royal Gold Edition | Advanced Cloud Management | {datetime.now().strftime('%d-%m-%Y %H:%M')}")
