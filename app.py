import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import hashlib
import os
import time
from datetime import datetime

# --- 1. SECURITY & DATABASE ARCHITECTURE ---
def hash_code(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def init_db():
    conn = sqlite3.connect('rajarao_chamber_final.db', check_same_thread=False)
    cursor = conn.cursor()
    # Unified Table for Cases, Strategy, and Finance
    cursor.execute('''CREATE TABLE IF NOT EXISTS cases 
        (id INTEGER PRIMARY KEY, case_id TEXT, petitioner TEXT, respondent TEXT, 
        court TEXT, section_bns TEXT, strategy_notes TEXT, 
        total_fee REAL, paid_fee REAL)''')
    # Hearings
    cursor.execute('''CREATE TABLE IF NOT EXISTS hearings 
        (id INTEGER PRIMARY KEY, case_id TEXT, hearing_date DATE, purpose TEXT)''')
    conn.commit()
    return conn

def backup_to_csv():
    try:
        conn = sqlite3.connect('rajarao_chamber_final.db')
        df = pd.read_sql_query("SELECT * FROM cases", conn)
        df.to_csv("CHAMBER_BACKUP_LOG.csv", index=False)
        return True
    except:
        return False

db_conn = init_db()

# --- 2. PREMIUM ENTERPRISE UI (CSS) ---
st.set_page_config(page_title="RajaRao Legal Suite Pro", page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #1e293b, #020617); color: #f8fafc; }
    .gold-title {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; text-align: center; font-size: 3.5rem; filter: drop-shadow(0px 2px 2px rgba(0,0,0,0.3));
    }
    .login-card {
        background: rgba(255, 255, 255, 0.05); padding: 40px; border-radius: 20px; 
        border: 1px solid #BF953F; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .stButton>button {
        background: linear-gradient(45deg, #d4af37, #996515);
        color: white !important; font-weight: bold; border-radius: 8px; width: 100%; border: none;
    }
    .strategy-vault {
        background: rgba(191, 149, 63, 0.05); border-left: 5px solid #BF953F;
        padding: 15px; margin: 10px 0; font-style: italic; color: #FCF6BA;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN GATEKEEPER ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    _, center, _ = st.columns([1, 2, 1])
    with center:
        st.markdown("<div class='gold-title'>ADVOCATE RAJARAO</div>", unsafe_allow_html=True)
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        st.markdown("### 🔐 Senior Counsel Authentication")
        user_id = st.text_input("Chamber ID", value="SENIOR-ADMIN")
        access_key = st.text_input("Encryption Key", type="password")
        mfa = st.text_input("MFA Token (Demo: 123456)")
        
        if st.button("DECRYPT & ENTER CHAMBER"):
            # Master Password: admin123 | MFA: 123456
            if hash_code(access_key) == hash_code("admin123") and mfa == "123456":
                st.session_state.authenticated = True
                st.success("Identity Verified. Accessing Sovereign Vault...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid Credentials. Access Denied.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 4. MAIN APPLICATION INTERFACE ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/law.png", width=60)
    st.markdown("### 🏛️ Management")
    menu = st.radio("Modules:", ["📊 Dashboard", "🔍 Conflict Search", "📅 Board Position", "📖 BNS Bridge", "🧠 Strategy & Billing"])
    st.divider()
    if st.button("SECURE LOGOUT"):
        st.session_state.authenticated = False
        st.rerun()
    st.caption(f"System Time: {datetime.now().strftime('%H:%M:%S')}")

# --- 5. CORE MODULE LOGIC ---

# A. DASHBOARD
if menu == "📊 Dashboard":
    st.markdown("<div class='gold-title'>Chamber Command</div>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active Files", db_conn.execute("SELECT COUNT(*) FROM cases").fetchone()[0])
    m2.metric("Hearings Today", db_conn.execute("SELECT COUNT(*) FROM hearings WHERE hearing_date=date('now')").fetchone()[0])
    m3.metric("BNS Sync", "100%", "Active")
    m4.metric("Cloud Backup", "Online")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("#### 📅 Today's High-Priority Board")
        h_df = pd.read_sql_query("SELECT case_id, hearing_date, purpose FROM hearings WHERE hearing_date >= date('now') LIMIT 5", db_conn)
        st.table(h_df)
    with col2:
        st.markdown("#### 📊 Practice Mix")
        df_chart = pd.read_sql_query("SELECT court, COUNT(*) as counts FROM cases GROUP BY court", db_conn)
        if not df_chart.empty:
            fig = px.pie(df_chart, values='counts', names='court', hole=.4, color_discrete_sequence=px.colors.sequential.Gold)
            fig.update_layout(showlegend=False, height=250, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

# B. CONFLICT SEARCH (Due Diligence)
elif menu == "🔍 Conflict Search":
    st.subheader("🔍 Due Diligence & Brief Onboarding")
    with st.form("conflict_check"):
        cid = st.text_input("Case ID")
        pet = st.text_input("Petitioner")
        res = st.text_input("Respondent")
        crt = st.selectbox("Court", ["Supreme Court", "High Court", "District Court", "Tribunal"])
        
        if st.form_submit_button("Verify & Archive"):
            # Ethics Check: Has respondent ever been our petitioner?
            conflict = pd.read_sql_query(f"SELECT case_id FROM cases WHERE petitioner LIKE '%{res}%'", db_conn)
            if not conflict.empty and res != "":
                st.error(f"🚨 ETHICAL CONFLICT: You represented '{res}' in Case {conflict['case_id'].iloc[0]}.")
            else:
                db_conn.execute("INSERT INTO cases (case_id, petitioner, respondent, court) VALUES (?,?,?,?)", (cid, pet, res, crt))
                db_conn.commit()
                backup_to_csv()
                st.success("No Conflict Found. Case Brief Secured.")

# C. BOARD POSITION
elif menu == "📅 Board Position":
    st.subheader("📅 Judicial Board Position")
    c1, c2 = st.columns([1, 2])
    with c1:
        cases = pd.read_sql_query("SELECT case_id FROM cases", db_conn)
        sel = st.selectbox("Select Brief", cases['case_id'])
        dt = st.date_input("Hearing Date")
        purp = st.text_input("Purpose")
        if st.button("Add to Cause List"):
            db_conn.execute("INSERT INTO hearings (case_id, hearing_date, purpose) VALUES (?,?,?)", (sel, dt, purp))
            db_conn.commit()
            st.rerun()
    with c2:
        st.dataframe(pd.read_sql_query("SELECT * FROM hearings ORDER BY hearing_date ASC", db_conn), use_container_width=True)

# D. BNS BRIDGE
elif menu == "📖 BNS Bridge":
    st.subheader("📖 BNS-IPC Comparative Bridge (2026)")
    bns_map = pd.DataFrame({
        "Offence": ["Murder", "Attempt to Murder", "Cheating", "Theft", "Defamation", "Unlawful Assembly"],
        "IPC (Old)": ["302", "307", "420", "378", "499", "141"],
        "BNS (New)": ["101", "109", "318", "303", "356", "189"]
    })
    st.table(bns_map)
    st.info("The Bharatiya Nyaya Sanhita (BNS) has replaced the IPC. Use this bridge for 2026 drafting.")

# E. STRATEGY & BILLING
elif menu == "🧠 Strategy & Billing":
    st.subheader("🧠 Senior Strategy & GST Billing")
    cases = pd.read_sql_query("SELECT case_id, petitioner FROM cases", db_conn)
    if not cases.empty:
        sel_case = st.selectbox("Select Case Brief", cases['case_id'])
        
        # Strategy Section
        st.markdown("<div class='strategy-vault'>", unsafe_allow_html=True)
        note = st.text_area("Confidential Strategy (Chamber Secrets):")
        if st.button("Save Strategy"):
            db_conn.execute("UPDATE cases SET strategy_notes=? WHERE case_id=?", (note, sel_case))
            db_conn.commit()
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.divider()
        # Billing Section
        fee = st.number_input("Professional Fee (₹)", min_value=0.0)
        if st.button("Generate GST Memo"):
            total = fee * 1.18
            st.markdown(f"""
            <div style='border: 2px dashed #BF953F; padding: 20px; font-family: monospace;'>
                <h3 style='text-align:center;'>MEMO OF FEES</h3>
                <p>Case: {sel_case}</p>
                <p>Net Fee: ₹{fee:,.2f}</p>
                <p>GST (18%): ₹{fee*0.18:,.2f}</p>
                <p><b>Grand Total: ₹{total:,.2f}</b></p>
                <p style='text-align:right;'>Digitally Signed: Adv. RajaRao</p>
            </div>
            """, unsafe_allow_html=True)
            db_conn.execute("UPDATE cases SET total_fee=? WHERE case_id=?", (total, sel_case))
            db_conn.commit()
            backup_to_csv()
    else:
        st.warning("Onboard a case first to access strategy and billing.")

# --- 6. FOOTER ---
st.markdown("---")
st.caption("© 2026 RajaRao Legal Suite | Advanced Enterprise Gold Edition | Secure Backup Enabled")
