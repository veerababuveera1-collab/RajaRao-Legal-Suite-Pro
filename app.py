import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import time
from datetime import datetime

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('rajarao_chamber.db', check_same_thread=False)
    cursor = conn.cursor()
    # Main Case Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS cases 
        (id INTEGER PRIMARY KEY, case_id TEXT, petitioner TEXT, respondent TEXT, 
        court TEXT, section_bns TEXT, strategy_notes TEXT, 
        total_fee REAL, paid_fee REAL)''')
    # Court Calendar
    cursor.execute('''CREATE TABLE IF NOT EXISTS hearings 
        (id INTEGER PRIMARY KEY, case_id TEXT, hearing_date DATE, purpose TEXT)''')
    # Research Library
    cursor.execute('''CREATE TABLE IF NOT EXISTS research 
        (id INTEGER PRIMARY KEY, title TEXT, citation TEXT, summary TEXT)''')
    conn.commit()
    return conn

db_conn = init_db()

# --- BNS-IPC REFERENCE DATA ---
bns_map = pd.DataFrame({
    "Offence": ["Murder", "Attempt to Murder", "Cheating", "Theft", "Defamation", "Unlawful Assembly", "Conspiracy"],
    "IPC_Old": ["302", "307", "420", "378", "499", "141", "120B"],
    "BNS_New": ["101", "109", "318", "303", "356", "189", "61"]
})

# --- UI STYLING ---
st.set_page_config(page_title="RajaRao Senior Apex", page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .gold-text {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 900; text-align: center; font-size: 3rem;
    }
    .strategy-vault {
        background: rgba(191, 149, 63, 0.05); border-left: 5px solid #BF953F;
        padding: 15px; margin: 10px 0; font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>⚖️</h1>", unsafe_allow_html=True)
    menu = st.radio("Navigation", 
                    ["Dashboard", "Conflict Search", "Board Position", "BNS Bridge", "Strategy & Billing", "Research Vault"])
    st.divider()
    st.caption("Advocate RajaRao & Associates")

# --- MODULES ---

if menu == "Dashboard":
    st.markdown("<div class='gold-text'>Chamber Command</div>", unsafe_allow_html=True)
    
    fin = db_conn.execute("SELECT SUM(total_fee), SUM(paid_fee) FROM cases").fetchone()
    billed, paid = (fin[0] or 0), (fin[1] or 0)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Active Briefs", db_conn.execute("SELECT COUNT(*) FROM cases").fetchone()[0])
    c2.metric("Hearings Today", db_conn.execute("SELECT COUNT(*) FROM hearings WHERE hearing_date=date('now')").fetchone()[0])
    c3.metric("Billed", f"₹{billed:,.0f}")
    c4.metric("Collected", f"₹{paid:,.0f}")

    st.markdown("### Court Distribution")
    df_chart = pd.read_sql_query("SELECT court, COUNT(*) as count FROM cases GROUP BY court", db_conn)
    if not df_chart.empty:
        fig = px.bar(df_chart, x='court', y='count', color='count', color_continuous_scale='Oryel')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)

elif menu == "Conflict Search":
    st.subheader("Due Diligence: Conflict of Interest Search")
    with st.form("conflict_form"):
        p_name = st.text_input("Petitioner Name")
        r_name = st.text_input("Respondent Name")
        c_id = st.text_input("Case ID")
        crt = st.selectbox("Forum", ["Supreme Court", "High Court", "District Court", "Tribunal"])
        
        if st.form_submit_button("Run Search & Onboard"):
            conflict = pd.read_sql_query(f"SELECT case_id FROM cases WHERE petitioner LIKE '%{r_name}%'", db_conn)
            if not conflict.empty and r_name != "":
                st.error(f"Potential Conflict: representation of {r_name} found in Case {conflict['case_id'].iloc[0]}.")
            else:
                db_conn.execute("INSERT INTO cases (case_id, petitioner, respondent, court) VALUES (?,?,?,?)", (c_id, p_name, r_name, crt))
                db_conn.commit()
                st.success("Brief onboarded successfully.")

elif menu == "Board Position":
    st.subheader("Judicial Board Position")
    col1, col2 = st.columns([1, 2])
    with col1:
        cases = pd.read_sql_query("SELECT case_id FROM cases", db_conn)
        sel_c = st.selectbox("Brief", cases['case_id'] if not cases.empty else ["No Cases"])
        h_dt = st.date_input("Hearing Date")
        h_prp = st.text_input("Purpose")
        if st.button("Add to Board"):
            db_conn.execute("INSERT INTO hearings (case_id, hearing_date, purpose) VALUES (?,?,?)", (sel_c, h_dt, h_prp))
            db_conn.commit()
            st.rerun()
    with col2:
        res = pd.read_sql_query("SELECT * FROM hearings ORDER BY hearing_date ASC", db_conn)
        st.dataframe(res, use_container_width=True)

elif menu == "BNS Bridge":
    st.subheader("Statute Translator (IPC to BNS)")
    st.dataframe(bns_map, use_container_width=True, hide_index=True)
    

elif menu == "Strategy & Billing":
    st.subheader("Chamber Secrets & Financials")
    cases = pd.read_sql_query("SELECT case_id FROM cases", db_conn)
    if not cases.empty:
        sel = st.selectbox("Select Case", cases['case_id'])
        
        st.markdown("<div class='strategy-vault'>", unsafe_allow_html=True)
        note = st.text_area("Confidential Strategy Notes")
        if st.button("Save Strategy"):
            db_conn.execute("UPDATE cases SET strategy_notes=? WHERE case_id=?", (note, sel))
            db_conn.commit()
        st.markdown("</div>", unsafe_allow_html=True)

        st.divider()
        fee = st.number_input("Professional Fee (₹)", min_value=0.0)
        gst = fee * 0.18
        st.info(f"Total with GST: ₹{fee + gst:,.2f}")
        if st.button("Update Ledger"):
            db_conn.execute("UPDATE cases SET total_fee=? WHERE case_id=?", (fee + gst, sel))
            db_conn.commit()

elif menu == "Research Vault":
    st.subheader("Junior Research Repository")
    with st.form("res_vault"):
        title = st.text_input("Topic")
        cit = st.text_input("Citation")
        summ = st.text_area("Summary")
        if st.form_submit_button("Archive Research"):
            db_conn.execute("INSERT INTO research (title, citation, summary) VALUES (?,?,?)", (title, cit, summ))
            db_conn.commit()
    
    st.markdown("---")
    st.dataframe(pd.read_sql_query("SELECT * FROM research", db_conn), use_container_width=True)

st.markdown("---")
st.caption("Advocate RajaRao Senior Suite | End-to-End Enterprise Control")
