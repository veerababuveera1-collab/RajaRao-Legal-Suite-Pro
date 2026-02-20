import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import time
from datetime import datetime

# --- 1. ARCHITECTURAL PERSISTENCE (SQLite) ---
def init_db():
    conn = sqlite3.connect('rajarao_senior_vault.db', check_same_thread=False)
    cursor = conn.cursor()
    # Case Ledger with Strategy and Financials
    cursor.execute('''CREATE TABLE IF NOT EXISTS cases 
        (id INTEGER PRIMARY KEY, case_id TEXT, petitioner TEXT, respondent TEXT, 
        court TEXT, section_bns TEXT, strategy_notes TEXT, 
        total_fee REAL, paid_fee REAL)''')
    # Court Cause List
    cursor.execute('''CREATE TABLE IF NOT EXISTS hearings 
        (id INTEGER PRIMARY KEY, case_id TEXT, hearing_date DATE, purpose TEXT)''')
    # Research Library for Juniors
    cursor.execute('''CREATE TABLE IF NOT EXISTS research 
        (id INTEGER PRIMARY KEY, title TEXT, citation TEXT, summary TEXT)''')
    conn.commit()
    return conn

db_conn = init_db()

# --- 2. BNS-IPC MASTER TRANSLATOR (2026 Edition) ---
bns_map = pd.DataFrame({
    "Offence": ["Murder", "Attempt to Murder", "Cheating", "Theft", "Defamation", "Unlawful Assembly", "Conspiracy"],
    "IPC (Old)": ["302", "307", "420", "378", "499", "141", "120B"],
    "BNS (New)": ["101", "109", "318", "303", "356", "189", "61"]
})

# --- 3. PREMIUM SENIOR COUNSEL UI (CSS) ---
st.set_page_config(page_title="RajaRao Senior Apex", page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .gold-text {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 900; text-align: center; font-size: 3rem;
    }
    .chamber-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid #1e293b; padding: 20px; border-radius: 15px;
    }
    .strategy-vault {
        background: rgba(191, 149, 63, 0.05); border-left: 5px solid #BF953F;
        padding: 15px; margin: 10px 0; font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR (Command Menu) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>⚖️</h1>", unsafe_allow_html=True)
    menu = st.radio("Navigation", 
                    ["🏛️ Dashboard", "🔍 Conflict Search", "📅 Board Position", "📖 BNS Bridge", "🧠 Strategy & Billing", "📚 Research Vault"])
    st.divider()
    st.caption("Advocate RajaRao & Associates\nSenior Counsel Edition v6.5")

# --- 5. FUNCTIONAL MODULES ---

# A. DASHBOARD
if menu == "🏛️ Dashboard":
    st.markdown("<div class='gold-text'>Chamber Command</div>", unsafe_allow_html=True)
    
    # Financial KPI
    fin = db_conn.execute("SELECT SUM(total_fee), SUM(paid_fee) FROM cases").fetchone()
    billed, paid = (fin[0] or 0), (fin[1] or 0)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Active Briefs", db_conn.execute("SELECT COUNT(*) FROM cases").fetchone()[0])
    c2.metric("Hearings Today", db_conn.execute("SELECT COUNT(*) FROM hearings WHERE hearing_date=date('now')").fetchone()[0])
    c3.metric("Billed (₹)", f"{billed/100000:.1f}L")
    c4.metric("Collected (₹)", f"{paid/100000:.1f}L")

    st.markdown("### 📊 Caseload Analytics")
    df_chart = pd.read_sql_query("SELECT court, COUNT(*) as count FROM cases GROUP BY court", db_conn)
    if not df_chart.empty:
        fig = px.bar(df_chart, x='court', y='count', color='count', color_continuous_scale='Oryel')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)

# B. CONFLICT SEARCH (Ethical Firewall)
elif menu == "🔍 Conflict Search":
    st.subheader("🔍 Due Diligence: Conflict of Interest Search")
    with st.form("conflict_form"):
        p_name = st.text_input("Prospective Petitioner")
        r_name = st.text_input("Prospective Respondent")
        c_id = st.text_input("Case Reference")
        if st.form_submit_button("Run Search"):
            # Logic: Has the new Respondent ever been our Client (Petitioner) before?
            conflict = pd.read_sql_query(f"SELECT case_id, petitioner FROM cases WHERE petitioner LIKE '%{r_name}%'", db_conn)
            if not conflict.empty and r_name != "":
                st.error(f"🚨 CONFLICT DETECTED: You previously represented {r_name} in Case {conflict['case_id'].iloc[0]}.")
            else:
                st.success("✅ No direct conflict found in chamber history.")
        
        if st.form_submit_button("Finalize Onboarding"):
            db_conn.execute("INSERT INTO cases (case_id, petitioner, respondent, court) VALUES (?,?,?,?)", (c_id, p_name, r_name, "Unassigned"))
            db_conn.commit()

# C. BOARD POSITION
elif menu == "📅 Board Position":
    st.subheader("📅 Judicial Board Position")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("#### Schedule")
        cases = pd.read_sql_query("SELECT case_id FROM cases", db_conn)
        sel_c = st.selectbox("Brief", cases['case_id'])
        h_dt = st.date_input("Date")
        h_prp = st.text_input("Purpose")
        if st.button("Add to Board"):
            db_conn.execute("INSERT INTO hearings (case_id, hearing_date, purpose) VALUES (?,?,?)", (sel_c, h_dt, h_prp))
            db_conn.commit()
    with col2:
        st.markdown("#### Cause List")
        res = pd.read_sql_query("SELECT * FROM hearings ORDER BY hearing_date ASC", db_conn)
        st.table(res)

# D. BNS BRIDGE
elif menu == "📖 BNS Bridge":
    st.subheader("📖 2026 Statute Translator")
    
    st.write("Reference for transitioning from IPC 1860 to Bharatiya Nyaya Sanhita 2023.")
    st.dataframe(bns_map, use_container_width=True, hide_index=True)

# E. STRATEGY & BILLING
elif menu == "🧠 Strategy & Billing":
    st.subheader("🧠 Senior Counsel Chamber Secrets")
    cases = pd.read_sql_query("SELECT case_id FROM cases", db_conn)
    if not cases.empty:
        sel = st.selectbox("Select Case", cases['case_id'])
        
        st.markdown("#### Strategic Pivots")
        note = st.text_area("Confidential Strategy (Judge temperament, Witness vulnerabilities...)", height=150)
        if st.button("Save Strategy"):
            db_conn.execute("UPDATE cases SET strategy_notes=? WHERE case_id=?", (note, sel))
            db_conn.commit()
            st.toast("Strategy Archived.")

        st.divider()
        st.markdown("#### 🧾 Professional Fee Statement (GST 2026)")
        c1, c2 = st.columns(2)
        base_fee = c1.number_input("Base Fee (₹)", min_value=0.0)
        gst_mode = c2.selectbox("GST Mechanism", ["Forward Charge (B2B)", "Reverse Charge (RCM)"])
        gst_val = base_fee * 0.18 if "Forward" in gst_mode else 0
        st.info(f"Grand Total: ₹{base_fee + gst_val:,.2f} (Includes GST: ₹{gst_val:,.2f})")
        if st.button("Sync to Ledger"):
            db_conn.execute("UPDATE cases SET total_fee=?, paid_fee=? WHERE case_id=?", (base_fee+gst_val, 0, sel))
            db_conn.commit()

# F. RESEARCH VAULT
elif menu == "📚 Research Vault":
    st.subheader("📚 Junior's Research Submission")
    with st.form("research"):
        title = st.text_input("Legal Proposition")
        cit = st.text_input("Citation (AIR / SCC)")
        summ = st.text_area("Ratio Decidendi")
        if st.form_submit_button("Submit to Senior Counsel"):
            db_conn.execute("INSERT INTO research (title, citation, summary) VALUES (?,?,?)", (title, cit, summ))
            db_conn.commit()
    
    st.markdown("---")
    res_lib = pd.read_sql_query("SELECT * FROM research", db_conn)
    st.dataframe(res_lib, use_container_width=True)

# --- 6. FOOTER ---
st.markdown("---")
st.caption("Adv. RajaRao Senior Suite | End-to-End Enterprise Control | BNS Framework 2026")
