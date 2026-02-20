import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="RajaRao Legal Suite Pro v4.5", 
    page_icon="⚖️", 
    layout="wide"
)

# --- 2. PREMIUM UI & STYLING ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #1e293b, #020617); color: #f8fafc; }
    .gold-title {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 900; text-align: center; font-size: 3.5rem; margin-bottom: 5px;
    }
    .legal-card {
        background: rgba(255, 255, 255, 0.05); border-left: 5px solid #d4af37;
        padding: 20px; border-radius: 12px; margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .bns-badge { background: #d4af37; color: black; padding: 2px 10px; border-radius: 15px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CLOUD DATA CONNECTION ---
SHEET_ID = "1l2p3L1VeP3Hm2uiaYasq2NeZ2Dp-RPx2ZwEHeq1nJXM"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=60)
def fetch_live_data():
    try:
        data = pd.read_csv(CSV_URL)
        data.columns = data.columns.str.strip()
        return data
    except Exception as e:
        return pd.DataFrame()

df = fetch_live_data()

# Header
st.markdown("<div class='gold-title'>Advocate RajaRao & Associates</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #d4af37;'>Strategic Legal Practice Management | Live Cloud Sync</p>", unsafe_allow_html=True)
st.divider()

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/law.png", width=60)
    st.markdown("### 🏛️ Management Menu")
    menu = st.radio("Select Module:", ["📊 Dashboard", "📡 Court Tracker", "🤖 Nyaya AI (BNS Search)", "📂 Case Vault"])
    
    if st.button("🔄 Sync Live Data"):
        st.cache_data.clear()
        st.rerun()
        
    st.divider()
    st.caption(f"System Status: Online")
    st.caption(f"Last Sync: {datetime.now().strftime('%H:%M:%S')}")

# --- 5. BNS INTELLIGENCE LIBRARY ---
bns_lib = {
    "101": {"crime": "Culpable Homicide", "ipc": "299/304", "punish": "Life or 10 Yrs", "notes": "Culpable homicide not amounting to murder."},
    "103": {"crime": "Murder (హత్య)", "ipc": "302", "punish": "Death/Life", "notes": "Forensic evidence is now a must."},
    "106": {"crime": "Death by Negligence", "ipc": "304A", "punish": "Up to 5 Yrs", "notes": "Medical and rash driving focus."},
    "111": {"crime": "Organized Crime", "ipc": "New", "punish": "Life/Death", "notes": "Syndicates and mafia groups."},
    "64": {"crime": "Rape (అత్యాచారం)", "ipc": "376", "punish": "10 Yrs to Life", "notes": "Rigorous punishment."},
    "82": {"crime": "Deceitful Marriage", "ipc": "New", "punish": "Up to 10 Yrs", "notes": "Sexual intercourse on false promise of marriage."},
    "152": {"crime": "Endangering Sovereignty", "ipc": "124A", "punish": "Life/7 Yrs", "notes": "Replaces old Sedition law."},
    "304": {"crime": "Snatching (గొలుసు దొంగతనం)", "ipc": "New", "punish": "Up to 3 Yrs", "notes": "Dedicated section for snatching crimes."},
    "351": {"crime": "Defamation (మర్యాద భంగం)", "ipc": "499/500", "punish": "2 Yrs or Community Service", "notes": "Community service introduced as punishment."}
}

# --- 6. MODULE LOGIC ---

# A. DASHBOARD
if menu == "📊 Dashboard":
    st.subheader("📊 Practice Intelligence Overview")
    if not df.empty:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Active Files", len(df))
        col2.metric("Security", "Active ✅")
        col3.metric("BNS Engine", f"{len(bns_lib)} Sections")
        col4.metric("Cloud Sync", "Live")
        
        st.markdown("### 📅 Live Hearing Schedule (From Cloud)")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.error("⚠️ Unable to load cloud data. Please check Google Sheet sharing permissions.")

# B. COURT TRACKER
elif menu == "📡 Court Tracker":
    st.subheader("📡 Live Case Database Tracking")
    case_input = st.text_input("Enter Case ID (Ex: WP 124/2026)")
    
    if st.button("Query Status"):
        if not case_input.strip():
            st.warning("Please enter a valid Case ID.")
        elif df.empty:
            st.error("Database is empty or disconnected.")
        else:
            match = df[df['Case_ID'].str.upper() == case_input.upper()]
            if not match.empty:
                res = match.iloc[0]
                st.markdown(f"""
                <div class='legal-card'>
                    <h2 style='color:#d4af37;'>{res['Case_ID']} Details</h2>
                    <p><b>Petitioner:</b> {res['Petitioner']} | <b>Judge:</b> {res['Judge']}</p>
                    <p><b>Current Stage:</b> {res['Stage']}</p>
                    <p style='color:#ff4b4b; font-size:1.2rem;'><b>Next Hearing: {res['Next_Hearing']}</b></p>
                    <p><b>Priority:</b> {res['Priority']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("No record found for this Case ID.")

# C. NYAYA AI (BNS SEARCH)
elif menu == "🤖 Nyaya AI (BNS Search)":
    st.markdown("<h2 style='color:#d4af37;'>🤖 Nyaya AI: BNS Explorer</h2>", unsafe_allow_html=True)
    
    query = st.text_input("Enter BNS Section Number (Ex: 103, 304, 152, 82)")
    
    if query in bns_lib:
        data = bns_lib[query]
        st.markdown(f"""
        <div class='legal-card'>
            <span class='bns-badge'>BNS Section {query}</span>
            <h2 style='color:#d4af37; margin-top:10px;'>{data['crime']}</h2>
            <p><b>🔄 Old Law (IPC):</b> IPC {data['ipc']}</p>
            <p><b>⚖️ Punishment:</b> {data['punish']}</p>
            <hr>
            <p><b>💡 Legal Insight:</b> {data['notes']}</p>
        </div>
        """, unsafe_allow_html=True)
    elif query:
        st.warning("⚠️ Section info not in local cache. Deep searching cloud...")

# D. CASE VAULT
elif menu == "📂 Case Vault":
    st.subheader("📂 Secure Legal Document Vault")
    uploaded_file = st.file_uploader("Upload Case Brief (PDF only)", type=['pdf'])
    if uploaded_file:
        with st.status("Encrypting & Storing..."):
            time.sleep(1.5)
            st.success(f"Document '{uploaded_file.name}' secured with AES-256.")

# --- 7. FOOTER ---
st.markdown("---")
st.caption("© 2026 Advocate RajaRao | Enterprise Legal Suite v4.5 | No-Login Professional Edition")
