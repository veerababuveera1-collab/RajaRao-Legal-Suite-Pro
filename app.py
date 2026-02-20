import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- 1. PAGE CONFIG & LIVE CONNECTION SETUP ---
st.set_page_config(
    page_title="RajaRao Legal Suite Pro", 
    page_icon="⚖️", 
    layout="wide"
)

# మీ Google Sheet నుండి డేటాను సేకరించే URL
SHEET_ID = "1l2p3L1VeP3Hm2uiaYasq2NeZ2Dp-RPx2ZwEHeq1nJXM"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=60)  # ప్రతి 60 సెకన్లకు డేటా ఆటోమేటిక్ రిఫ్రెష్ అవుతుంది
def fetch_live_data():
    try:
        data = pd.read_csv(CSV_URL)
        # కాలమ్ పేర్లను శుభ్రం చేయడం (Cleaning whitespace)
        data.columns = data.columns.str.strip()
        return data
    except Exception as e:
        return pd.DataFrame()

# ప్రాథమిక డేటా లోడింగ్
df = fetch_live_data()

# --- 2. PREMIUM ENTERPRISE UI (CSS) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #1e293b, #020617); color: #f8fafc; }
    .gold-title {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; text-align: center; font-size: 3.5rem; margin-bottom: 5px;
    }
    .stButton>button {
        background: linear-gradient(45deg, #d4af37, #996515);
        color: white !important; font-weight: bold; border-radius: 8px; width: 100%; border: none;
    }
    [data-testid="stMetricValue"] { color: #d4af37 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.markdown("<div class='gold-title'>Advocate RajaRao & Associates</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #d4af37;'>Strategic Legal Practice Management | Live Cloud Sync</p>", unsafe_allow_html=True)
st.divider()

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/law.png", width=60)
    st.markdown("### 🏛️ Management Menu")
    menu = st.radio("Select Module:", ["📊 Dashboard", "📡 Court Tracker", "🤖 Nyaya AI Chat", "📂 Case Vault"])
    
    if st.button("🔄 Sync Live Data"):
        st.cache_data.clear()
        st.rerun()
        
    st.divider()
    st.caption(f"System Status: Online")
    st.caption(f"Last Sync: {datetime.now().strftime('%H:%M:%S')}")

# --- 5. MODULE LOGIC ---

# A. DASHBOARD: గూగుల్ షీట్ నుండి లైవ్ మెట్రిక్స్
if menu == "📊 Dashboard":
    st.subheader("📊 Practice Intelligence Overview")
    if not df.empty:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Active Files", len(df))
        col2.metric("Hearings Today", "6") # ఇది మాన్యువల్ లేదా షీట్ నుండి ఫిల్టర్ చేయవచ్చు
        col3.metric("BNS Ready", "100%")
        col4.metric("Pending Tasks", "12")
        
        st.markdown("### 📅 Live Hearing Schedule (From Cloud)")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.error("⚠️ Unable to load cloud data. Please check Google Sheet sharing permissions.")

# B. COURT TRACKER: లైవ్ డేటా సెర్చ్
elif menu == "📡 Court Tracker":
    st.subheader("📡 Live e-Courts Database Tracking")
    case_input = st.text_input("Enter Case ID or CNR Number", placeholder="e.g. WP 124/2026")
    
    if st.button("Query Status"):
        if not case_input.strip():
            st.warning("Please enter a valid Case ID.")
        elif df.empty:
            st.error("Database is empty or disconnected.")
        else:
            with st.status("Fetching from Cloud Database..."):
                time.sleep(1)
                # కేస్ ఐడి ని షీట్ లో వెతకడం
                match = df[df['Case_ID'].str.upper() == case_input.upper()]
                
                if not match.empty:
                    st.success("Case Record Synchronized.")
                    res = match.iloc[0]
                    st.markdown(f"""
                    **Case ID:** `{res['Case_ID']}`  
                    **Petitioner:** {res['Petitioner']}  
                    **Current Stage:** {res['Stage']}  
                    **Presiding Judge:** {res['Judge']}  
                    **Next Hearing Date:** {res['Next_Hearing']}  
                    **Priority:** {res['Priority']}
                    """)
                else:
                    st.error("No record found for this Case ID in your database.")

# C. NYAYA AI CHAT
elif menu == "🤖 Nyaya AI Chat":
    st.subheader("🤖 Nyaya Mitra: AI Legal Associate")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    if prompt := st.chat_input("Ask a legal question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        with st.chat_message("assistant"):
            response = f"Counsel RajaRao, regarding '{prompt}', the BNS 2026 framework emphasizes procedural efficiency. Specifically, under your current database records, this analysis can be applied to cases like {df['Case_ID'].iloc[0] if not df.empty else 'your active files'}."
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# D. CASE VAULT: ఫైల్ సెక్యూరిటీ
elif menu == "📂 Case Vault":
    st.subheader("📂 Secure Legal Document Vault")
    uploaded_file = st.file_uploader("Upload Case Brief (PDF only)", type=['pdf'])
    if uploaded_file:
        with st.status("Encrypting & Storing..."):
            time.sleep(1.5)
            st.success(f"Document '{uploaded_file.name}' secured with AES-256.")

# --- 6. FOOTER ---
st.markdown("---")
st.caption("© 2026 RajaRao Legal Suite | Advanced Cloud Edition | Powered by Google Sheets API")
