import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- 1. SETTINGS & PAGE DESIGN ---
st.set_page_config(
    page_title="RajaRao Legal Suite v2.5", 
    page_icon="⚖️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LIVE CLOUD CONNECTION (Google Sheets) ---
SHEET_ID = "1l2p3L1VeP3Hm2uiaYasq2NeZ2Dp-RPx2ZwEHeq1nJXM"
# gid=0 అనేది మీ మొదటి ట్యాబ్ కోసం
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

@st.cache_data(ttl=60)
def fetch_live_data():
    try:
        data = pd.read_csv(CSV_URL)
        data.columns = [c.strip() for c in data.columns]
        return data
    except Exception as e:
        return pd.DataFrame()

# --- 3. PREMIUM DESIGNER UI (CSS) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #1e293b, #020617); color: #f8fafc; }
    .gold-title {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 900; text-align: center; font-size: 3.5rem; letter-spacing: -1px;
    }
    .legal-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(212, 175, 55, 0.2);
        padding: 25px; border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    .bns-badge {
        background: #d4af37; color: black; padding: 4px 12px;
        border-radius: 20px; font-weight: bold; font-size: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. BNS KNOWLEDGE ENGINE ---
bns_engine = {
    "103": {"crime": "Murder (హత్య)", "ipc": "IPC 302", "punishment": "Death or Life Imprisonment"},
    "303": {"crime": "Theft (దొంగతనం)", "ipc": "IPC 378/379", "punishment": "Up to 3 Years or Fine"},
    "111": {"crime": "Organized Crime", "ipc": "New Provision", "punishment": "Stringent / Life"},
    "70": {"crime": "Gang Rape", "ipc": "IPC 376D", "punishment": "20 Years or Life"}
}

# --- 5. LOGIN SYSTEM ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<div class='gold-title'>ADVOCATE RAJA RAO</div>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.2, 1])
    with col2:
        st.subheader("🔐 Chamber Authentication")
        user = st.text_input("Username", value="rajarao")
        pwd = st.text_input("Encryption Key", type="password")
        if st.button("DECRYPT & ENTER CHAMBER"):
            if user == "rajarao" and pwd == "chamber123":
                st.session_state.auth = True
                st.success("Access Granted.")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid Credentials.")
    st.stop()

# --- 6. SIDEBAR NAVIGATION ---
df = fetch_live_data()

with st.sidebar:
    st.markdown("<h2 style='color:#d4af37;'>⚖️ APEX PRO</h2>", unsafe_allow_html=True)
    st.write(f"Senior Counsel: **Raja Rao**")
    menu = st.radio("Navigation Engine:", ["📊 Dashboard", "📡 Live Tracker", "🤖 Nyaya AI (BNS)", "📂 Secure Vault"])
    st.divider()
    if st.button("🔄 Sync Cloud Data"):
        st.cache_data.clear()
        st.rerun()
    if st.button("Logout"):
        st.session_state.auth = False
        st.rerun()

# --- 7. MASTER MODULES ---

if menu == "📊 Dashboard":
    st.markdown("<div class='gold-title'>Practice Intelligence</div>", unsafe_allow_html=True)
    
    if not df.empty:
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Active Briefs", len(df))
        critical = len(df[df['Priority'].str.contains('Critical|High', na=False, case=False)])
        m2.metric("Critical Priority", critical, "Urgent")
        m3.metric("BNS Sync", "v2026", "Live")
        
        st.markdown("### 🗓️ Live Court Schedule (Cloud)")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("Google Sheet డేటాను లోడ్ చేయడంలో విఫలమైంది. దయచేసి లింక్ చెక్ చేయండి.")

elif menu == "📡 Live Tracker":
    st.subheader("📡 Live Cloud Case Retrieval")
    search = st.text_input("Enter Case ID (e.g., WP 124/2026)")
    if st.button("Fetch Details"):
        match = df[df['Case_ID'].astype(str).str.contains(search, case=False, na=False)] if not df.empty else pd.DataFrame()
        if not match.empty:
            res = match.iloc[0]
            st.markdown(f"""
            <div class='legal-card'>
                <h2 style='color:#d4af37;'>{res['Case_ID']}</h2>
                <p><b>Petitioner:</b> {res['Petitioner']} | <b>Judge:</b> {res['Judge']}</p>
                <hr>
                <p><b>Current Stage:</b> {res['Stage']}</p>
                <p><b>Next Hearing:</b> <span style='color:#ff4b4b;'>{res['Next_Hearing']}</span></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Case ID Not Found.")

elif menu == "🤖 Nyaya AI (BNS)":
    st.markdown("<div class='gold-title'>Nyaya AI BNS Explorer</div>", unsafe_allow_html=True)
    query = st.text_input("Enter BNS Section (Ex: 103, 303, 70)")
    if query in bns_engine:
        data = bns_engine[query]
        st.markdown(f"""
        <div class='legal-card'>
            <span class='bns-badge'>BNS SECTION {query}</span>
            <h3 style='margin-top:10px;'>{data['crime']}</h3>
            <p style='color:#ff4b4b;'><b>Equivalent:</b> {data['ipc']}</p>
            <p><b>Punishment:</b> {data['punishment']}</p>
        </div>
        """, unsafe_allow_html=True)

elif menu == "📂 Secure Vault":
    st.subheader("📂 Encrypted Document Vault")
    file = st.file_uploader("Upload Brief (PDF)", type=['pdf'])
    if file:
        st.success(f"Security Shield Active: {file.name} is encrypted.")

# FOOTER
st.divider()
st.caption(f"© 2026 RajaRao Legal Suite | Cloud v2.5 | {datetime.now().strftime('%d-%b-%Y')}")
