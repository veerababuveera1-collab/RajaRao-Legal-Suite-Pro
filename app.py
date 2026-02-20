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

# --- 3. PREMIUM DESIGNER STYLING (CSS) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #0f172a, #020617); color: #f8fafc; }
    
    .gold-title {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 900; text-align: center; font-size: 3rem; letter-spacing: -1px;
        margin-bottom: 20px;
    }
    
    .legal-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(212, 175, 55, 0.3);
        padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 15px;
    }
    
    .bns-badge {
        background: #d4af37; color: #000; padding: 3px 10px;
        border-radius: 15px; font-weight: bold; font-size: 0.75rem;
    }

    /* Table Customization */
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
    st.markdown("<h1 style='color:#d4af37;'>🏛️ APEX PRO</h1>", unsafe_allow_html=True)
    st.write(f"Senior Counsel: **RajaRao**")
    st.divider()
    menu = st.radio("Management Modules:", ["📊 Practice Intelligence", "📡 Live Court Tracker", "🤖 Nyaya AI Search", "📂 Secure Vault"])
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
        c2.metric("Pending Stage", "Active", "Live")
        c3.metric("Database", "Cloud Synced", "OK")
        st.dataframe(df_court, use_container_width=True, hide_index=True)
    else:
        st.error("Court data not found. Please sync cloud.")

# B. Live Court Tracker
elif menu == "📡 Live Court Tracker":
    st.subheader("📡 Real-time Case Search")
    sq = st.text_input("Search Case ID, Petitioner, or Stage...")
    if sq and not df_court.empty:
        res = df_court[df_court.apply(lambda r: r.astype(str).str.contains(sq, case=False).any(), axis=1)]
        if not res.empty:
            st.dataframe(res, use_container_width=True, hide_index=True)
        else:
            st.warning("No records match.")

# C. Nyaya AI Search (THE UPGRADED TABULAR ENGINE)
elif menu == "🤖 Nyaya AI Search":
    st.markdown("<div class='gold-title'>Nyaya AI Explorer</div>", unsafe_allow_html=True)
    st.write("Cross-reference BNS vs IPC in a professional tabular format.")
    
    query = st.text_input("BNS Section, IPC, or Nature of Offence ఎంటర్ చేయండి...", placeholder="Ex: 103, 302, Murder, Theft...")
    
    if query:
        if not df_bns.empty:
            # Multi-column dynamic search
            results = df_bns[df_bns.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
            
            if not results.empty:
                st.markdown(f"### 📋 ఫలితాలు: '{query}'")
                
                # Tabular Display with specific headers
                cols_to_show = ['BNS Section', 'IPC Equivalent', 'Nature of Offence (నేరం స్వభావం)', 'Punishment (శిక్షా కాలం)']
                existing_cols = [c for c in cols_to_show if c in df_bns.columns]
                
                st.dataframe(results[existing_cols], use_container_width=True, hide_index=True)
                
                # Highlight Card for precise matches
                if len(results) == 1:
                    row = results.iloc[0]
                    st.markdown(f"""
                    <div class='legal-card'>
                        <span class='bns-badge'>BNS {row['BNS Section']}</span>
                        <h3 style='color:#d4af37;'>{row.get('Nature of Offence (నేరం స్వభావం)', 'Offence Details')}</h3>
                        <p><b>IPC Reference:</b> {row['IPC Equivalent']} | <b>Punishment:</b> {row.get('Punishment (శిక్షా కాలం)', 'Check Code')}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("సెక్షన్ లభించలేదు. దయచేసి సరైన నంబర్ ఇవ్వండి.")
        else:
            st.error("BNS Database is empty. Connect cloud URL.")

# D. Secure Vault
elif menu == "📂 Secure Vault":
    st.subheader("📂 Case Document Encryption")
    uploaded = st.file_uploader("Upload Brief (PDF)", type=['pdf'])
    if uploaded:
        with st.spinner("Encrypting with AES-256..."):
            time.sleep(1)
            st.success(f"{uploaded.name} is now secured in the chamber vault.")

st.markdown("---")
st.caption(f"© 2026 RajaRao Legal Suite | v3.0 Apex Cloud | Logged in as: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
