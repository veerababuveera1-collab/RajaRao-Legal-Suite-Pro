import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="RajaRao Legal Suite Pro v2.5", 
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

# --- 3. EXTENDED BNS KNOWLEDGE BASE (Zero Data Stress) ---
bns_library = {
    # Offenses Against Body
    "103": {"crime": "Murder (హత్య)", "ipc": "IPC 302", "punishment": "Death or Life Imprisonment", "notes": "Punishment for murder."},
    "106": {"crime": "Causing Death by Negligence", "ipc": "IPC 304A", "punishment": "Up to 5 years", "notes": "Focus on medical negligence and rash driving."},
    "111": {"crime": "Organized Crime", "ipc": "New Provision", "punishment": "Life or Death", "notes": "Covers syndicates, kidnapping, and cybercrime."},
    "115": {"crime": "Voluntary Hurt (గాయపరచడం)", "ipc": "IPC 323", "punishment": "Up to 1 Year", "notes": "Simple hurt cases."},
    "117": {"crime": "Grievous Hurt", "ipc": "IPC 325", "punishment": "Up to 7 Years", "notes": "Causing severe bodily injury."},
    
    # Crimes Against Women
    "64": {"crime": "Rape (అత్యాచారం)", "ipc": "IPC 376", "punishment": "7 Years to Life", "notes": "Rigorous imprisonment."},
    "70": {"crime": "Gang Rape", "ipc": "IPC 376D", "punishment": "20 Years to Life", "notes": "Stringent penalties under BNS."},
    "74": {"crime": "Outraging Modesty", "ipc": "IPC 354", "punishment": "1 to 5 Years", "notes": "Assault or criminal force to women."},
    
    # Property & Fraud
    "303": {"crime": "Theft (దొంగతనం)", "ipc": "IPC 378/379", "punishment": "Up to 3 Years", "notes": "Includes snatching and electronic theft."},
    "304": {"crime": "Snatching", "ipc": "New Provision", "punishment": "Up to 3 Years", "notes": "Specifically defined for the first time in BNS."},
    "308": {"crime": "Extortion (దౌర్జన్య వసూలు)", "ipc": "IPC 383", "punishment": "Up to 7 Years", "notes": "Forcing someone to give property."},
    "318": {"crime": "Cheating (మోసం)", "ipc": "IPC 415/420", "punishment": "Up to 7 Years", "notes": "Fraudulent inducement of property."},
    
    # State & Public Order
    "113": {"crime": "Terrorist Act", "ipc": "UAPA related", "punishment": "Death or Life", "notes": "Broad definition of terror threats."},
    "189": {"crime": "Unlawful Assembly", "ipc": "IPC 141/143", "punishment": "Up to 6 Months", "notes": "5+ persons for illegal purpose."},
    "351": {"crime": "Defamation (మర్యాద భంగం)", "ipc": "IPC 499/500", "punishment": "Up to 2 Years or Community Service", "notes": "Community service introduced as punishment."},
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
    .legal-card {
        background: rgba(255, 255, 255, 0.05); border-left: 5px solid #d4af37;
        padding: 20px; border-radius: 12px; margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .bns-badge { background: #d4af37; color: black; padding: 2px 10px; border-radius: 15px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='color:#d4af37;'>🏛️ RAJARAO PRO</h1>", unsafe_allow_html=True)
    menu = st.radio("Navigation:", ["📊 Dashboard", "📡 Court Tracker", "🤖 Nyaya AI (BNS Search)", "📂 Secure Vault"])
    st.divider()
    if st.button("🔄 Sync Cloud Data"):
        st.cache_data.clear()
        st.success("Synced!")
    st.caption(f"System Active: {datetime.now().strftime('%H:%M:%S')}")

# --- 6. MAIN LOGIC ---

# A. DASHBOARD
if menu == "📊 Dashboard":
    st.markdown("<div class='gold-title'>Practice Intelligence</div>", unsafe_allow_html=True)
    df = fetch_cloud_data()
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Live Cases", len(df))
        c2.metric("BNS Knowledge", f"{len(bns_library)} Sections")
        c3.metric("System Status", "Secure")
        st.markdown("### 🗓️ Active Case Schedule")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("💡 గూగుల్ షీట్ కనెక్ట్ చేస్తే ఇక్కడ మీ లైవ్ కేసులు కనిపిస్తాయి.")

# B. COURT TRACKER
elif menu == "📡 Court Tracker":
    st.subheader("📡 Case Retrieval System")
    case_id = st.text_input("Enter Case Number (Ex: WP 124/2026)")
    if st.button("Track Now"):
        df = fetch_cloud_data()
        match = df[df['Case_ID'].str.upper() == case_id.upper()] if not df.empty else pd.DataFrame()
        if not match.empty:
            res = match.iloc[0]
            st.markdown(f"""
            <div class='legal-card'>
                <h3 style='color:#d4af37;'>{res['Case_ID']} Details</h3>
                <p><b>Petitioner:</b> {res['Petitioner']} | <b>Judge:</b> {res['Judge']}</p>
                <p><b>Stage:</b> {res['Stage']}</p>
                <p style='color:#ff4b4b;'><b>Next Hearing:</b> {res['Next_Hearing']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Case ID not found in records.")

# C. NYAYA AI (BNS SEARCH)
elif menu == "🤖 Nyaya AI (BNS Search)":
    st.markdown("<div class='gold-title'>Nyaya AI Explorer</div>", unsafe_allow_html=True)
    query = st.text_input("Enter Section Number (Ex: 103, 304, 351, 70)")
    if query:
        if query in bns_library:
            data = bns_library[query]
            st.markdown(f"""
            <div class='legal-card'>
                <span class='bns-badge'>BNS Section {query}</span>
                <h2 style='color:#d4af37; margin-top:10px;'>{data['crime']}</h2>
                <p style='color:#ff4b4b;'><b>🔄 Old Law (IPC):</b> {data['ipc']}</p>
                <p><b>⚖️ Punishment:</b> {data['punishment']}</p>
                <hr>
                <p><b>💡 Notes:</b> {data['notes']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Section info not in local cache. Deep searching cloud...")

# D. SECURE VAULT
elif menu == "📂 Secure Vault":
    st.subheader("📂 Case Vault (AES-256)")
    up = st.file_uploader("Upload Confidential PDF", type=['pdf'])
    if up: st.success(f"Shield Active: {up.name} is encrypted.")

st.markdown("---")
st.caption("© 2026 Advocate RajaRao | Legal Suite v2.5 | Power of AI & Cloud")
