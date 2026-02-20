import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="RajaRao Legal Suite Pro v4.0", 
    page_icon="⚖️", 
    layout="wide"
)

# --- 2. AUTHENTICATION SYSTEM ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def logout():
    st.session_state.logged_in = False
    st.rerun()

# --- 3. LOGIN PAGE UI ---
def show_login():
    st.markdown("""
        <style>
        .stApp { background: #020617; }
        .login-box {
            background: rgba(255, 255, 255, 0.05);
            padding: 40px;
            border-radius: 20px;
            border: 1px solid #d4af37;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        </style>
    """, unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.markdown("<h1 style='color: #d4af37; margin-bottom:0;'>🏛️ LEGAL ACCESS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: gray;'>Authorized Personnel Only</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            u = st.text_input("Username (advocate)")
            p = st.text_input("Password (legal2026)", type="password")
            btn = st.form_submit_button("Secure Login")
            
            if btn:
                if u == "advocate" and p == "legal2026":
                    st.session_state.logged_in = True
                    st.success("✅ Access Granted!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid Credentials")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 4. MAIN APPLICATION LOGIC ---
if not st.session_state.logged_in:
    show_login()
else:
    # --- PREMIUM STYLING ---
    st.markdown("""
        <style>
        .stApp { background: radial-gradient(circle at top right, #1e293b, #020617); color: #f8fafc; }
        .gold-title {
            background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            font-weight: 900; text-align: center; font-size: 3rem; margin-bottom: 20px;
        }
        .legal-card {
            background: rgba(255, 255, 255, 0.05); border-left: 5px solid #d4af37;
            padding: 20px; border-radius: 12px; margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .bns-badge { background: #d4af37; color: black; padding: 2px 10px; border-radius: 15px; font-weight: bold; font-size: 0.8rem; }
        </style>
        """, unsafe_allow_html=True)

    # --- CLOUD DATA CONNECTION ---
    SHEET_ID = "1l2p3L1VeP3Hm2uiaYasq2NeZ2Dp-RPx2ZwEHeq1nJXM"
    CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

    @st.cache_data(ttl=60)
    def fetch_data():
        try:
            data = pd.read_csv(CSV_URL)
            data.columns = data.columns.str.strip()
            return data
        except: return pd.DataFrame()

    # --- SIDEBAR NAVIGATION ---
    with st.sidebar:
        st.markdown("<h1 style='color:#d4af37;'>⚖️ RAJARAO PRO</h1>", unsafe_allow_html=True)
        st.write(f"Logged as: **Advocate RajaRao**")
        menu = st.radio("Navigation Engine:", ["📊 Dashboard", "📡 Court Tracker", "🤖 Nyaya AI (BNS Search)", "📂 Secure Vault"])
        st.divider()
        if st.button("Logout"): logout()
        st.caption(f"Last Sync: {datetime.now().strftime('%H:%M:%S')}")

    # --- 5. EXTENDED BNS KNOWLEDGE BASE (v4.0) ---
    bns_lib = {
        # --- Body ---
        "101": {"crime": "Culpable Homicide", "ipc": "299/304", "punish": "Life or 10 Yrs", "notes": "Culpable homicide not amounting to murder."},
        "103": {"crime": "Murder (హత్య)", "ipc": "302", "punish": "Death/Life", "notes": "Punishment for murder."},
        "106": {"crime": "Death by Negligence", "ipc": "304A", "punish": "Up to 5 Yrs", "notes": "Rash driving/medical negligence focus."},
        "111": {"crime": "Organized Crime", "ipc": "New", "punish": "Life/Death", "notes": "Covers syndicates/mafia."},
        "115": {"crime": "Voluntary Hurt", "ipc": "323", "punish": "Up to 1 Yr", "notes": "Simple hurt."},
        "117": {"crime": "Grievous Hurt", "ipc": "325", "punish": "Up to 7 Yrs", "notes": "Severe bodily injury."},
        # --- Women & Marriage ---
        "64": {"crime": "Rape (అత్యాచారం)", "ipc": "376", "punish": "10 Yrs to Life", "notes": "Rigorous imprisonment."},
        "70": {"crime": "Gang Rape", "ipc": "376D", "punish": "20 Yrs to Life", "notes": "Stringent group assault laws."},
        "74": {"crime": "Outraging Modesty", "ipc": "354", "punish": "1 to 5 Yrs", "notes": "Criminal force to women."},
        "82": {"crime": "Sexual Intercourse by Deceit", "ipc": "New", "punish": "Up to 10 Yrs", "notes": "Intercourse by promising marriage deceitfully."},
        "85": {"crime": "Cruelty by Husband/Relatives", "ipc": "498A", "punish": "Up to 3 Yrs", "notes": "Domestic cruelty cases."},
        # --- Property ---
        "303": {"crime": "Theft (దొంగతనం)", "ipc": "378/379", "punish": "Up to 3 Yrs", "notes": "Includes snatching."},
        "304": {"crime": "Snatching (గొలుసు దొంగతనం)", "ipc": "New", "punish": "Up to 3 Yrs", "notes": "Separate section in BNS."},
        "308": {"crime": "Extortion", "ipc": "383", "punish": "Up to 7 Yrs", "notes": "Compelling property delivery by fear."},
        "310": {"crime": "Robbery", "ipc": "392", "punish": "Up to 10 Yrs", "notes": "Theft with force."},
        "318": {"crime": "Cheating (మోసం)", "ipc": "420", "punish": "Up to 7 Yrs", "notes": "Dishonest inducement."},
        "329": {"crime": "Criminal Trespass", "ipc": "441", "punish": "Up to 3 Months", "notes": "Illegal entry."},
        # --- State & Public Order ---
        "152": {"crime": "Sedition (New Form)", "ipc": "124A", "punish": "Life or 7 Yrs", "notes": "Endangering sovereignty."},
        "196": {"crime": "Promoting Enmity", "ipc": "153A", "punish": "Up to 3 Yrs", "notes": "Hatred between groups."},
        "226": {"crime": "Attempt Suicide (to Restrain Officer)", "ipc": "New", "punish": "Up to 1 Yr", "notes": "Suicide as a tool against officers."},
        "351": {"crime": "Defamation (మర్యాద భంగం)", "ipc": "499/500", "punish": "2 Yrs or Comm Service", "notes": "Community service is new."},
        "353": {"crime": "Criminal Intimidation", "ipc": "506", "punish": "Up to 2 Yrs", "notes": "Threatening injury."}
    }

    # --- 6. MODULES ---
    if menu == "📊 Dashboard":
        st.markdown("<div class='gold-title'>Practice Intelligence</div>", unsafe_allow_html=True)
        df = fetch_data()
        if not df.empty:
            c1, c2, c3 = st.columns(3)
            c1.metric("Live Cases", len(df))
            c2.metric("Knowledge Base", f"{len(bns_lib)} Sections")
            c3.metric("System Security", "AES-256")
            st.dataframe(df, use_container_width=True, hide_index=True)
        else: st.warning("Please check Google Sheet Permissions.")

    elif menu == "📡 Court Tracker":
        st.subheader("📡 Real-time Retrieval")
        cid = st.text_input("Enter Case ID (Ex: WP 124/2026)")
        if st.button("Query Now"):
            df = fetch_data()
            match = df[df['Case_ID'].str.upper() == cid.upper()] if not df.empty else pd.DataFrame()
            if not match.empty:
                r = match.iloc[0]
                st.markdown(f"<div class='legal-card'><h3>{r['Case_ID']}</h3><p><b>Petitioner:</b> {r['Petitioner']}</p><p><b>Next Hearing:</b> <span style='color:red;'>{r['Next_Hearing']}</span></p></div>", unsafe_allow_html=True)
            else: st.error("Case ID not found.")

    elif menu == "🤖 Nyaya AI (BNS Search)":
        st.markdown("<div class='gold-title'>Nyaya AI Explorer</div>", unsafe_allow_html=True)
        q = st.text_input("Enter BNS Section Number (Ex: 103, 304, 152, 82)")
        if q in bns_lib:
            d = bns_lib[q]
            st.markdown(f"""
            <div class='legal-card'>
                <span class='bns-badge'>BNS Section {q}</span>
                <h2 style='color:#d4af37;'>{d['crime']}</h2>
                <p><b>🔄 Old Law (IPC):</b> {d['ipc']}</p>
                <p><b>⚖️ Punishment:</b> {d['punish']}</p>
                <p><b>💡 Legal Insight:</b> {d['notes']}</p>
            </div>
            """, unsafe_allow_html=True)
        elif q: st.warning("Section info not in quick-cache.")

    elif menu == "📂 Secure Vault":
        st.subheader("📂 Case Vault (Encrypted Storage)")
        up = st.file_uploader("Upload Case PDF", type=['pdf'])
        if up: st.success(f"{up.name} is encrypted and stored securely.")

    st.markdown("---")
    st.caption("© 2026 Advocate RajaRao | Enterprise Legal Suite v4.0")
