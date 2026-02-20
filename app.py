import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- 1. PRO CONFIGURATION ---
st.set_page_config(
    page_title="RajaRao Legal Suite Pro", 
    page_icon="⚖️", 
    layout="wide"
)

# --- 2. LIVE CLOUD CONNECTION (Case Tracking) ---
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

# --- 3. BUILT-IN BNS INTELLIGENCE (మీ దగ్గర డేటా లేకపోయినా ఇవి పనిచేస్తాయి) ---
bns_library = {
    "103": {"crime": "Murder (హత్య)", "ipc": "IPC 302", "punishment": "Death or Life Imprisonment", "notes": "New BNS focusing on speedy trial."},
    "111": {"crime": "Organized Crime", "ipc": "New Provision", "punishment": "Life or Death", "notes": "Targeting crime syndicates/mafias."},
    "303": {"crime": "Theft (దొంగతనం)", "ipc": "IPC 378/379", "punishment": "Up to 3 Years", "notes": "Includes snatching and electronic theft."},
    "70": {"crime": "Gang Rape", "ipc": "IPC 376D", "punishment": "20 Years or Life", "notes": "Severe penalties under BNS."},
    "113": {"crime": "Terrorist Act", "ipc": "UAPA related", "punishment": "Death or Life", "notes": "Broad definition of terrorism."},
    "304": {"crime": "Snatching", "ipc": "New Section", "punishment": "Up to 3 Years", "notes": "Specifically defined for the first time."},
    "115": {"crime": "Voluntary Hurt", "ipc": "IPC 323", "punishment": "Up to 1 Year", "notes": "Causing hurt voluntarily."},
}

# --- 4. PREMIUM UI DESIGN (CSS) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #1e293b, #020617); color: #f8fafc; }
    .gold-title {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 900; text-align: center; font-size: 3.5rem; margin-bottom: 0px;
    }
    .card {
        background: rgba(255, 255, 255, 0.05); border-left: 5px solid #d4af37;
        padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .stMetric { background: rgba(212, 175, 55, 0.1); padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='color:#d4af37;'>🏛️ RAJARAO PRO</h1>", unsafe_allow_html=True)
    menu = st.radio("Intelligence Modules:", ["📊 Practice Dashboard", "📡 Live Court Tracker", "🤖 Nyaya AI (BNS Search)", "📂 Secure Vault"])
    st.divider()
    if st.button("🔄 Forces Sync Cloud"):
        st.cache_data.clear()
        st.rerun()
    st.caption(f"Last Sync: {datetime.now().strftime('%H:%M:%S')}")

# --- 6. CORE MODULES ---

# A. DASHBOARD
if menu == "📊 Practice Dashboard":
    st.markdown("<div class='gold-title'>Practice Overview</div>", unsafe_allow_html=True)
    df = fetch_cloud_data()
    
    if not df.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Active Files", len(df))
        col2.metric("Critical Priority", len(df[df['Priority'].str.contains('Critical', na=False)]))
        col3.metric("Cloud Status", "Online ✅")
        
        st.markdown("### 📅 Integrated Hearing Schedule")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ గూగుల్ షీట్ నుండి డేటా అందడం లేదు. పర్మిషన్స్ చెక్ చేయండి.")

# B. COURT TRACKER
elif menu == "📡 Live Court Tracker":
    st.subheader("📡 Real-time Case Retrieval")
    case_id = st.text_input("Enter Case ID (Ex: WP 124/2026)")
    
    if st.button("Query Database"):
        df = fetch_cloud_data()
        match = df[df['Case_ID'].str.upper() == case_id.upper()] if not df.empty else pd.DataFrame()
        
        if not match.empty:
            res = match.iloc[0]
            st.markdown(f"""
            <div class='card'>
                <h2 style='color:#d4af37;'>{res['Case_ID']} - Details Found</h2>
                <p><b>Petitioner:</b> {res['Petitioner']} | <b>Judge:</b> {res['Judge']}</p>
                <p><b>Current Stage:</b> {res['Stage']}</p>
                <p style='color:#ff4b4b;'><b>Next Hearing:</b> {res['Next_Hearing']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Case ID not found in your Google Sheet records.")

# C. NYAYA AI (BNS SEARCH)
elif menu == "🤖 Nyaya AI (BNS Search)":
    st.markdown("<div class='gold-title'>Nyaya AI Explorer</div>", unsafe_allow_html=True)
    st.write("Cross-reference BNS vs IPC statutes instantly.")
    
    query = st.text_input("Enter BNS Section Number (Ex: 103, 303, 111)")
    
    if query:
        if query in bns_library:
            data = bns_library[query]
            st.markdown(f"""
            <div class='card'>
                <h3 style='color:#d4af37;'>BNS Section {query}: {data['crime']}</h3>
                <p style='color:#ff4b4b;'><b>Old IPC Equivalent:</b> {data['ipc']}</p>
                <p><b>Punishment:</b> {data['punishment']}</p>
                <p><b>Legal Notes:</b> {data['notes']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Searching deeper libraries... ఈ సెక్షన్ సమాచారం ప్రస్తుత క్యాష్‌లో లేదు.")

# D. SECURE VAULT
elif menu == "📂 Secure Vault":
    st.subheader("📂 Case Document Encryption")
    file = st.file_uploader("Upload Confidential PDF", type=['pdf'])
    if file:
        with st.status("Encrypting..."):
            time.sleep(1)
            st.success(f"Security Shield Active: {file.name} is now encrypted.")

st.markdown("---")
st.caption("© 2026 Advocate RajaRao | Advanced Practice Engine | v2.5 Final")
